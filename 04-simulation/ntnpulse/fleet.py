"""Fleet orchestration twin: the constellation run as a KubeEdge-style edge cluster.

The control plane (CloudCore) sits in the Frankfurt cloud. Every satellite runs an edge agent (EdgeCore)
that only hears from it while it has a path to an open gateway: directly, or over the ISL mesh. Each step
(default 10 s) the twin works out that reachability and then advances one software rollout:

1. **Reachability.** Direct = a gateway sees the satellite above 5 deg. With ISL, any satellite in the same
   mesh component as a direct one is reachable too. Gaps longer than the Kubernetes grace period would mark
   the node NotReady; gaps longer than grace + toleration would evict its pods.
2. **Image transfer.** Sources are gateway-visible satellites (``ota_mbps`` each) and, with peer sharing,
   satellites that already hold the image (a share of the RF ISL). Each satellite that still needs the image
   takes the nearest source in ISL hops; a source's rate is split between the satellites it feeds.
3. **Release.** The cloud releases a canary first, waits ``canary_soak_min`` after it reports healthy, then
   releases waves of ``wave_size`` (maxUnavailable). A satellite only learns it was released at its next contact.
4. **Restart.** A released satellite with the image restarts its workload (gNB down for ``restart_s``),
   optionally only while it is not serving the North Sea. It runs autonomously from then on and reports
   "updated" at its next contact. The next wave waits for those reports.
"""
from __future__ import annotations

from collections import deque

import numpy as np
import pandas as pd

from . import config as cfg
from .engine import BASIN_CENTRE, _gap_lengths
from .geometry import WalkerConstellation, elevation_and_range, geodetic_to_ecef
from .links import isl_edges


class FleetRollout:
    def __init__(self, sc: cfg.FleetScenario):
        self.sc = sc
        self.walker = WalkerConstellation(sc.constellation)
        self.n = sc.constellation.size
        gws = [g for g in cfg.GATEWAYS if g.name not in sc.blocked_gateways]
        self.gw_xyz = geodetic_to_ecef(np.array([g.lat for g in gws]), np.array([g.lon for g in gws]))
        self.basin_xyz = geodetic_to_ecef(np.array([BASIN_CENTRE[0]]), np.array([BASIN_CENTRE[1]]))
        self.waves = self._plan_waves()
        self.image_bytes = sc.image_mb * 1e6

    def _plan_waves(self) -> list[list[int]]:
        # Interleave planes so one wave never takes a whole plane (and its ISL ring) down at once.
        order = sorted(range(self.n), key=lambda k: (self.walker.slot[k], self.walker.plane[k]))
        if self.sc.strategy == "all":
            return [order]
        w = max(1, self.sc.wave_size)
        return [order[:1]] + [order[i:i + w] for i in range(1, self.n, w)]

    # --- per-step geometry -------------------------------------------------------------------
    def _adjacency(self, pos) -> list[list[int]]:
        adj = [[] for _ in range(self.n)]
        if self.sc.isl:
            for i, j, _, _ in isl_edges(self.walker, pos):
                adj[i].append(j)
                adj[j].append(i)
        return adj

    def _over_basin(self, pos) -> np.ndarray:
        el, _ = elevation_and_range(self.basin_xyz, pos)
        return el[0] >= cfg.TERMINAL_MIN_EL_DEG

    @staticmethod
    def _bfs(adj, sources) -> dict[int, int]:
        """Multi-source BFS: node -> the source that reaches it in the fewest hops."""
        owner = {s: s for s in sources}
        q = deque(sources)
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in owner:
                    owner[v] = owner[u]
                    q.append(v)
        return owner

    # --- run -----------------------------------------------------------------------------------
    def run(self) -> "FleetResult":
        sc, n, dt = self.sc, self.n, self.sc.step_s
        have = np.zeros(n)                       # image bytes onboard
        got_spec = np.zeros(n, bool)             # satellite has heard it is released
        restart_end = np.full(n, np.nan)
        t_image = np.full(n, np.nan)
        t_applied = np.full(n, np.nan)
        t_reported = np.full(n, np.nan)
        reach_hist = np.zeros((int(sc.duration_s / dt), n), bool)
        released = np.zeros(n, bool)
        wave_of = np.empty(n, int)
        for k, wave in enumerate(self.waves):
            wave_of[wave] = k
        t_release = [np.nan] * len(self.waves)
        t_release[0] = 0.0
        released[self.waves[0]] = True
        ground_bytes = peer_bytes = 0.0
        impact_s = 0.0
        series = []

        for step in range(reach_hist.shape[0]):
            t = step * dt
            pos = self.walker.ecef(t)
            el_g, _ = elevation_and_range(self.gw_xyz, pos)
            direct = (el_g >= cfg.GATEWAY_MIN_EL_DEG).any(axis=0)
            adj = self._adjacency(pos)
            reach = np.zeros(n, bool)
            reach[list(self._bfs(adj, list(np.flatnonzero(direct))))] = True
            reach_hist[step] = reach
            over_basin = self._over_basin(pos)

            # cloud -> edge: new specs arrive, finished satellites report back
            got_spec |= released & reach
            newly = reach & ~np.isnan(t_applied) & np.isnan(t_reported)
            t_reported[newly] = t

            # image transfer
            need = (have < self.image_bytes) & (got_spec | sc.prestage)
            if need.any():
                seeds = [int(s) for s in np.flatnonzero(have >= self.image_bytes)] if sc.peer_sharing else []
                anchors = [int(s) for s in np.flatnonzero(direct)]
                owner = self._bfs(adj, anchors + [s for s in seeds if s not in anchors])
                fed = {}
                for s in np.flatnonzero(need):
                    if s in owner:
                        fed.setdefault(owner[s], []).append(int(s))
                isl_bps = cfg.RF_ISL_CAPACITY_BPS * cfg.OTA_ISL_SHARE
                for src, sats in fed.items():
                    src_bps = sc.ota_mbps * 1e6 if direct[src] else isl_bps
                    for s in sats:
                        bps = src_bps / len(sats) if s == src else min(src_bps / len(sats), isl_bps)
                        got = min(bps * dt / 8, self.image_bytes - have[s])
                        have[s] += got
                        if direct[src]:
                            ground_bytes += got
                        else:
                            peer_bytes += got
                        if have[s] >= self.image_bytes:
                            t_image[s] = t

            # restarts: finish running ones, then start new ones within maxUnavailable
            restarting = ~np.isnan(restart_end) & np.isnan(t_applied)
            done_now = restarting & (restart_end <= t)
            t_applied[done_now] = t
            restarting &= ~done_now
            slots = (n if sc.strategy == "all" else max(1, sc.wave_size)) - int(restarting.sum())
            ready = got_spec & (have >= self.image_bytes) & np.isnan(restart_end)
            if sc.avoid_basin:   # must be clear of the basin for the whole restart
                ready &= ~over_basin & ~self._over_basin(self.walker.ecef(t + sc.restart_s))
            for s in np.flatnonzero(ready)[:max(slots, 0)]:
                restart_end[s] = t + sc.restart_s
                restarting[s] = True
            impact_s += float((restarting & over_basin).sum() * dt)

            # release the next wave once the current one has reported in (plus soak after the canary)
            k = int(released.sum() and wave_of[np.flatnonzero(released)].max())
            if k + 1 < len(self.waves) and not np.isnan(t_reported[self.waves[k]]).any():
                soak = sc.canary_soak_min * 60 if k == 0 and sc.strategy == "waves" else 0.0
                if t >= np.nanmax(t_reported[self.waves[k]]) + soak:
                    released[self.waves[k + 1]] = True
                    t_release[k + 1] = t

            series.append(dict(
                t=t, reachable=int(reach.sum()), direct=int(direct.sum()),
                image_complete=int((have >= self.image_bytes).sum()),
                released=int(released.sum()), restarting=int(restarting.sum()),
                applied=int((~np.isnan(t_applied)).sum()), reported=int((~np.isnan(t_reported)).sum()),
            ))

        return FleetResult(self, reach_hist, t_image, t_applied, t_reported, wave_of, t_release,
                           ground_bytes, peer_bytes, impact_s, pd.DataFrame(series))


class FleetResult:
    def __init__(self, ro: FleetRollout, reach_hist, t_image, t_applied, t_reported, wave_of, t_release,
                 ground_bytes, peer_bytes, impact_s, series):
        self.scenario = ro.sc
        self.series = series
        self.t_release = t_release
        self.ground_bytes, self.peer_bytes, self.impact_s = ground_bytes, peer_bytes, impact_s
        sc, days = ro.sc, ro.sc.duration_s / 86400
        rows = []
        for s in range(ro.n):
            gaps = _gap_lengths(~reach_hist[:, s], sc.step_s)
            rows.append(dict(
                sat=s, plane=int(ro.walker.plane[s]), wave=int(wave_of[s]),
                reachable=reach_hist[:, s].mean(),
                max_gap_min=max(gaps, default=0) / 60,
                notready_per_day=sum(g > sc.grace_s for g in gaps) / days,
                evictions_per_day=sum(g > sc.grace_s + sc.eviction_s for g in gaps) / days,
                image_h=t_image[s] / 3600, applied_h=t_applied[s] / 3600, reported_h=t_reported[s] / 3600,
            ))
        self.sats = pd.DataFrame(rows)

    def summary(self) -> dict:
        s, sc = self.sats, self.scenario
        n_done = int(s.reported_h.notna().sum())
        return dict(
            sats=len(s), isl=sc.isl, peer_sharing=sc.peer_sharing, strategy=sc.strategy,
            reachable_mean=s.reachable.mean(),
            always_reachable=(s.reachable == 1).mean(),
            max_gap_min=s.max_gap_min.max(),
            max_down=int(self.series.restarting.max()),
            notready_per_sat_day=s.notready_per_day.mean(),
            evictions_per_sat_day=s.evictions_per_day.mean(),
            image_all_h=s.image_h.max() if s.image_h.notna().all() else np.nan,
            applied_p50_h=s.applied_h.median(),
            fleet_updated_h=s.reported_h.max() if n_done == len(s) else np.nan,
            updated=n_done,
            ground_mb=self.ground_bytes / 1e6, peer_mb=self.peer_bytes / 1e6,
            basin_outage_s=self.impact_s,
        )


def run_rollout(sc: cfg.FleetScenario) -> FleetResult:
    return FleetRollout(sc).run()
