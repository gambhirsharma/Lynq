"""Time-stepped digital twin: orbits -> visibility -> routing graph -> traffic, queues and delivery.

Each step (default 10 s) the topology is treated as frozen. Messages generated in a step are routed
against that topology; anything that cannot be delivered waits in a terminal queue (bent-pipe, or no
satellite in view) or an onboard queue (regenerative store-and-forward) and is retried every step.
"""
from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass, field

import networkx as nx
import numpy as np
import pandas as pd

from . import config as cfg
from .geometry import (
    WalkerConstellation, ecef_to_latlon, elevation_and_range, geodetic_to_ecef, great_circle_km,
    prop_delay_s,
)
from .links import isl_edges, user_rate_bps

ANY = "*"   # unconstrained routing, used to detect where policy changed the gateway
BASIN_CENTRE = (57.0, 3.0)


@dataclass(order=True)
class Message:
    sort_key: tuple
    id: int = field(compare=False)
    cls: cfg.TrafficClass = field(compare=False)
    size: int = field(compare=False)
    terminal: int = field(compare=False)
    jurisdiction: str = field(compare=False)
    t_gen: float = field(compare=False)
    t_uplink: float | None = field(default=None, compare=False)


class Simulation:
    def __init__(self, scenario: cfg.Scenario):
        self.sc = scenario
        self.rng = np.random.default_rng(scenario.seed)
        self.walker = WalkerConstellation(scenario.constellation)
        self.n_sats = scenario.constellation.size
        self.isl_on = scenario.mode == "regen_isl"
        self.regen = scenario.mode != "bent_pipe"

        self._place_terminals(scenario.terminals)
        self.gws = [g for g in cfg.GATEWAYS]
        self.gw_xyz = geodetic_to_ecef(np.array([g.lat for g in self.gws]), np.array([g.lon for g in self.gws]))
        self.gw_cloud_s = [
            cfg.GROUND_PROC_S + great_circle_km(g.lat, g.lon, *cfg.CLOUD_SITE) * cfg.FIBRE_ROUTE_FACTOR / cfg.FIBRE_KM_S
            for g in self.gws
        ]
        self.gw_open = [g.name not in scenario.blocked_gateways for g in self.gws]
        self.basin_xyz = geodetic_to_ecef(np.array([BASIN_CENTRE[0]]), np.array([BASIN_CENTRE[1]]))

        self.term_q: list[list[Message]] = [[] for _ in range(self.n_terms)]
        self.sat_q: list[list[Message]] = [[] for _ in range(self.n_sats)]
        self.sat_q_bytes = np.zeros(self.n_sats)
        self.records: list[dict] = []
        self.dropped: list[dict] = []
        self.series: list[dict] = []
        self.ids = itertools.count()
        self.prev_serving = np.full(self.n_terms, -1)
        self.handovers = 0
        self.generated = 0

    # --- setup -----------------------------------------------------------------
    def _place_terminals(self, n: int):
        shares = np.array([s[-1] for s in cfg.SECTORS])
        counts = np.floor(shares / shares.sum() * n).astype(int)
        counts[0] += n - counts.sum()
        lats, lons, juris, sector = [], [], [], []
        for (name, la0, la1, lo0, lo1, j, _), k in zip(cfg.SECTORS, counts):
            lats += list(self.rng.uniform(la0, la1, k))
            lons += list(self.rng.uniform(lo0, lo1, k))
            juris += [j] * k
            sector += [name] * k
        self.term_lat, self.term_lon = np.array(lats), np.array(lons)
        self.term_jur = np.array(juris)
        self.term_sector = np.array(sector)
        self.term_xyz = geodetic_to_ecef(self.term_lat, self.term_lon)
        self.n_terms = n

    # --- topology ----------------------------------------------------------------
    def topology(self, t: float):
        pos = self.walker.ecef(t)
        el_t, rng_t = elevation_and_range(self.term_xyz, pos)
        rate_t = user_rate_bps(rng_t)
        vis_t = (el_t >= cfg.TERMINAL_MIN_EL_DEG) & (rate_t > 0)
        el_g, rng_g = elevation_and_range(self.gw_xyz, pos)
        vis_g = el_g >= cfg.GATEWAY_MIN_EL_DEG

        # Directed, gateway -> satellite only: Dijkstra runs outward from the allowed gateways and can
        # never transit a gateway (that would be an unpoliced terrestrial hop).
        G = nx.DiGraph()
        G.add_nodes_from(range(self.n_sats))
        isl = isl_edges(self.walker, pos) if self.isl_on else []
        for i, j, km, kind in isl:
            w = prop_delay_s(km) + cfg.ISL_HOP_PROC_S
            G.add_edge(i, j, w=w, kind=kind)
            G.add_edge(j, i, w=w, kind=kind)
        for g in range(len(self.gws)):
            if not self.gw_open[g]:
                continue
            for s in np.flatnonzero(vis_g[g]):
                G.add_edge(f"gw{g}", int(s), w=prop_delay_s(rng_g[g, s]) + self.gw_cloud_s[g], kind="feeder")

        routes = {}
        groups = {j: [f"gw{g}" for g, gw in enumerate(self.gws) if gw.country in allowed and f"gw{g}" in G]
                  for j, allowed in cfg.JURISDICTION_RULES.items()}
        groups[ANY] = [n for n in G.nodes if isinstance(n, str)]
        for j, srcs in groups.items():
            routes[j] = nx.multi_source_dijkstra(G, set(srcs), weight="w") if srcs else ({}, {})
        return dict(pos=pos, el_t=el_t, rng_t=rng_t, rate_t=rate_t, vis_t=vis_t, vis_g=vis_g,
                    G=G, isl=isl, routes=routes)

    # --- capacity bookkeeping -------------------------------------------------------
    def _reset_budgets(self):
        dt = self.sc.step_s
        self.up_left = np.full(self.n_sats, cfg.SAT_SERVICE_CAPACITY_BPS * dt / 8)
        self.edge_used: dict[frozenset, float] = {}

    def _edge_cap(self, G, a, b):
        kind = G.edges[a, b]["kind"]
        bps = {"feeder": cfg.FEEDER_CAPACITY_BPS, "rf": cfg.RF_ISL_CAPACITY_BPS,
               "optical": cfg.OPTICAL_ISL_CAPACITY_BPS}[kind]
        return bps * self.sc.step_s / 8

    def _reserve_path(self, G, path, size) -> bool:
        edges = [frozenset((a, b)) for a, b in zip(path, path[1:])]
        for e, (a, b) in zip(edges, zip(path, path[1:])):
            if self.edge_used.get(e, 0.0) + size > self._edge_cap(G, a, b):
                return False
        for e in edges:
            self.edge_used[e] = self.edge_used.get(e, 0.0) + size
        return True

    # --- traffic ----------------------------------------------------------------------
    def _generate(self, t: float):
        if t > self.sc.duration_s - 2 * 3600:   # last 2 h only drain queues
            return
        dt = self.sc.step_s
        for c in cfg.TRAFFIC_CLASSES:
            k = self.rng.poisson(self.n_terms * dt / c.mean_interval_s * self.sc.load)
            for term in self.rng.integers(0, self.n_terms, k):
                lo, hi = c.size_bytes
                size = int(np.exp(self.rng.uniform(np.log(lo), np.log(hi))))
                mid = next(self.ids)
                m = Message((c.priority, t, mid), mid, c, size, int(term), str(self.term_jur[term]), t)
                heapq.heappush(self.term_q[term], m)
                self.generated += 1

    def _drop(self, m: Message, t: float, reason: str):
        self.dropped.append(dict(cls=m.cls.name, reason=reason, t_gen=m.t_gen, t=t, sector=self.term_sector[m.terminal]))

    def _deliver(self, m, t, topo, sat, net_s, kind):
        path = topo["routes"][m.jurisdiction][1][sat]       # gateway ... sat
        gw = int(path[0][2:])
        hops = len(path) - 2
        best_any = topo["routes"][ANY][1].get(sat)
        self.records.append(dict(
            id=m.id, cls=m.cls.name, size=m.size, sector=self.term_sector[m.terminal], jurisdiction=m.jurisdiction,
            t_gen=m.t_gen, t_uplink=m.t_uplink, t_deliver=t,
            wait_terminal_s=m.t_uplink - m.t_gen, wait_onboard_s=t - m.t_uplink,
            network_s=net_s, latency_s=(t - m.t_gen) + net_s,
            sat=sat, gateway=self.gws[gw].name, gw_country=self.gws[gw].country,
            isl_hops=hops, path=kind,
            compliant=self.gws[gw].country in cfg.JURISDICTION_RULES[m.jurisdiction],
            policy_redirect=best_any is not None and best_any[0] != path[0],
        ))

    # --- per-step processing -------------------------------------------------------------
    def _serve_terminals(self, t, topo):
        G, routes, vis_t = topo["G"], topo["routes"], topo["vis_t"]
        for term in range(self.n_terms):
            q = self.term_q[term]
            if not q or not vis_t[term].any():
                continue
            sats = np.flatnonzero(vis_t[term])
            dist, paths = routes[self.term_jur[term]]
            up_s = prop_delay_s(topo["rng_t"][term, sats])
            # prefer the satellite with the shortest end-to-end path; else just the closest one
            i = int(np.argmin([up_s[i] + dist.get(int(s), 1e6) for i, s in enumerate(sats)]))
            s = int(sats[i])
            has_path = s in dist
            keep = []
            while q:
                m = heapq.heappop(q)
                if t - m.t_gen > m.cls.ttl_s:
                    self._drop(m, t, "ttl")
                    continue
                if not self.regen and not has_path:
                    keep.append(m)          # bent-pipe: needs a gateway in the same footprint now
                    continue
                if self.up_left[s] < m.size:
                    keep.append(m)          # uplink congested this step
                    continue
                rate = topo["rate_t"][term, s]
                access_s = cfg.RACH_ACCESS_S + m.size * 8 / rate + up_s[i]
                self.up_left[s] -= m.size
                m.t_uplink = t
                if has_path and self._reserve_path(G, paths[s], m.size):
                    proc = cfg.GNB_PROC_S if self.regen else cfg.BENT_PIPE_GNB_PROC_S
                    kind = "isl" if len(paths[s]) > 2 else "direct"
                    self._deliver(m, t, topo, s, access_s + proc + dist[s], kind)
                elif not self.regen:
                    self.up_left[s] += m.size   # feeder full: terminal keeps it
                    m.t_uplink = None
                    keep.append(m)
                elif self.sat_q_bytes[s] + m.size > cfg.ONBOARD_BUFFER_BYTES:
                    self._drop(m, t, "buffer")
                else:
                    heapq.heappush(self.sat_q[s], m)
                    self.sat_q_bytes[s] += m.size
            for m in keep:
                heapq.heappush(q, m)

    def _serve_onboard(self, t, topo):
        G, routes = topo["G"], topo["routes"]
        for s in range(self.n_sats):
            q = self.sat_q[s]
            if not q:
                continue
            keep = []
            while q:
                m = heapq.heappop(q)
                if t - m.t_gen > m.cls.ttl_s:
                    self.sat_q_bytes[s] -= m.size
                    self._drop(m, t, "ttl")
                    continue
                dist, paths = routes[m.jurisdiction]
                if s in dist and self._reserve_path(G, paths[s], m.size):
                    self.sat_q_bytes[s] -= m.size
                    self._deliver(m, t, topo, s, cfg.GNB_PROC_S + dist[s], "store_forward")
                else:
                    keep.append(m)
            for m in keep:
                heapq.heappush(q, m)

    def _log_step(self, t, topo):
        vis_t = topo["vis_t"]
        el = np.where(vis_t, topo["el_t"], -90)
        serving = np.where(vis_t.any(axis=1), el.argmax(axis=1), -1)
        self.handovers += int(((serving != self.prev_serving) & (serving >= 0) & (self.prev_serving >= 0)).sum())
        self.prev_serving = serving
        el_b, _ = elevation_and_range(self.basin_xyz, topo["pos"])
        sats_with_gw = {n for g in topo["G"].nodes if isinstance(g, str) for n in topo["G"].neighbors(g)}
        self.series.append(dict(
            t=t,
            sats_over_basin=int((el_b[0] >= cfg.TERMINAL_MIN_EL_DEG).sum()),
            terminals_covered=float(vis_t.any(axis=1).mean()),
            sats_with_gateway=len(sats_with_gw),
            isl_links=len(topo["isl"]),
            onboard_queue_kb=float(self.sat_q_bytes.sum() / 1e3),
            terminal_queue_msgs=int(sum(len(q) for q in self.term_q)),
            delivered=len(self.records),
        ))

    def run(self, progress=None) -> "Result":
        steps = int(self.sc.duration_s / self.sc.step_s)
        for k in range(steps):
            t = k * self.sc.step_s
            topo = self.topology(t)
            self._reset_budgets()
            self._generate(t)
            if self.regen:
                self._serve_onboard(t, topo)    # stored traffic first: it is older
            self._serve_terminals(t, topo)
            self._log_step(t, topo)
            if progress and k % 200 == 0:
                progress(k / steps)
        pending = sum(len(q) for q in self.term_q) + sum(len(q) for q in self.sat_q)
        return Result(self, pending)

    # --- snapshot for the map ------------------------------------------------------------
    def snapshot(self, t: float) -> dict:
        topo = self.topology(t)
        lat, lon = ecef_to_latlon(topo["pos"])
        feeders = []
        for a, b, kind in topo["G"].edges(data="kind"):
            if kind == "feeder":
                gw, sat = (a, b) if isinstance(a, str) else (b, a)
                feeders.append((int(gw[2:]), sat))
        return dict(sat_lat=lat, sat_lon=lon, isl=topo["isl"], feeders=feeders,
                    plane=self.walker.plane, optical=self.walker.optical)


class Result:
    def __init__(self, sim: Simulation, pending: int):
        self.scenario = sim.sc
        self.records = pd.DataFrame(sim.records)
        self.dropped = pd.DataFrame(sim.dropped)
        self.series = pd.DataFrame(sim.series)
        self.generated = sim.generated
        self.pending = pending
        self.handovers = sim.handovers
        self.n_terms = sim.n_terms

    def by_class(self) -> pd.DataFrame:
        rows = []
        r, d = self.records, self.dropped
        for c in cfg.TRAFFIC_CLASSES:
            rc = r[r.cls == c.name] if len(r) else r
            nd = int((d.cls == c.name).sum()) if len(d) else 0
            n = len(rc)
            lat = rc.latency_s if n else pd.Series(dtype=float)
            rows.append(dict(
                cls=c.name, delivered=n, dropped=nd,
                p50_s=lat.median() if n else np.nan,
                p95_s=lat.quantile(0.95) if n else np.nan,
                max_s=lat.max() if n else np.nan,
                within_150ms=(lat < cfg.TRAFFIC_CLASSES[0].target_s).mean() if n else np.nan,
                within_250ms=(lat < cfg.MESH_TARGET_S).mean() if n else np.nan,
                within_90min=(lat <= cfg.SNF_TARGET_S).mean() if n else np.nan,
                via_isl=(rc.isl_hops > 0).mean() if n else np.nan,
                store_forward=(rc.path == "store_forward").mean() if n else np.nan,
            ))
        return pd.DataFrame(rows)

    def summary(self) -> dict:
        r, s, sc = self.records, self.series, self.scenario
        crit = r[r.cls == "critical"] if len(r) else r
        gaps = _gap_lengths(s.sats_over_basin.values == 0, sc.step_s)
        return dict(
            scenario=sc.label, sats=sc.constellation.size, mode=sc.mode,
            blocked=",".join(sorted(sc.blocked_gateways)) or "-", load=sc.load,
            generated=self.generated, delivered=len(r),
            delivery_ratio=len(r) / max(self.generated, 1),
            dropped=len(self.dropped), pending=self.pending,
            critical_p50_s=crit.latency_s.median() if len(crit) else np.nan,
            critical_p95_s=crit.latency_s.quantile(0.95) if len(crit) else np.nan,
            critical_within_250ms=(crit.latency_s < cfg.MESH_TARGET_S).mean() if len(crit) else np.nan,
            all_within_90min=(r.latency_s <= cfg.SNF_TARGET_S).mean() if len(r) else np.nan,
            basin_coverage=(s.sats_over_basin > 0).mean(),
            terminal_coverage=s.terminals_covered.mean(),
            max_gap_min=max(gaps, default=0) / 60,
            mean_gap_min=(np.mean(gaps) / 60) if gaps else 0.0,
            handovers_per_terminal_day=self.handovers / self.n_terms / (sc.duration_s / 86400),
            max_onboard_queue_kb=s.onboard_queue_kb.max(),
            routing_compliance=r.compliant.mean() if len(r) else np.nan,
            policy_redirects=r.policy_redirect.mean() if len(r) else np.nan,
        )


def _gap_lengths(mask: np.ndarray, step_s: float) -> list[float]:
    gaps, run = [], 0
    for v in mask:
        if v:
            run += 1
        elif run:
            gaps.append(run * step_s)
            run = 0
    if run:
        gaps.append(run * step_s)
    return gaps


def run(scenario: cfg.Scenario, progress=None) -> Result:
    return Simulation(scenario).run(progress)
