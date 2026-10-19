"""Global coverage and latency for one constellation design.

Each time step the topology is frozen and, for every point of an equal-area grid over the whole Earth,
the model finds the lowest one-way latency from a terminal there to the internet:

    alarm latency = random access + transmission + uplink + onboard gNB
                  + ISL hops (distance / c + per-hop processing)
                  + feeder downlink + gateway/5G Core + fibre to the nearest PoP (+ GEO backhaul for polar sites)

A point is "served" in a step when it sees a satellite above the terminal mask with a closing link budget
and that satellite has a route (direct or over the ISL mesh) to an open gateway.
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra

from . import config as cfg
from .geometry import (
    Fleet, clear_of_earth, elevation_and_range, fibonacci_grid, geodetic_to_ecef, great_circle_km, prop_delay_s,
)


# --- Links -----------------------------------------------------------------------
def uplink_snr_db(d_km):
    fspl = 20 * np.log10(d_km) + 20 * np.log10(cfg.SERVICE_FREQ_MHZ) + 32.44
    return (cfg.TERMINAL_EIRP_DBW - fspl - cfg.LINK_LOSSES_DB + cfg.SAT_GT_DBK
            - cfg.K_BOLTZMANN_DBW - 10 * np.log10(cfg.SERVICE_BW_HZ))


def user_rate_bps(d_km):
    snr_db = uplink_snr_db(d_km)
    rate = cfg.IMPL_EFFICIENCY * cfg.SERVICE_BW_HZ * np.log2(1 + 10 ** (snr_db / 10))
    return np.where(snr_db >= cfg.MIN_SNR_DB, np.minimum(rate, cfg.MAX_USER_RATE_BPS), 0.0)


def link_rate_bps(tech: str, km):
    """Crosslink data rate at range km, 0 where the link does not close."""
    t = cfg.ISL_TECH[tech]
    if t.rate_bps:
        return np.where(km <= t.max_km, t.rate_bps, 0.0)
    fspl = 20 * np.log10(km) + 20 * np.log10(t.freq_ghz * 1e3) + 32.44
    snr_db = t.eirp_dbw - fspl - t.losses_db + t.gt_dbk - cfg.K_BOLTZMANN_DBW - 10 * np.log10(t.bw_hz)
    rate = cfg.IMPL_EFFICIENCY * t.bw_hz * np.log2(1 + 10 ** (snr_db / 10))
    return np.where((rate >= t.min_rate_bps) & (km <= t.max_km), rate, 0.0)


def _nearest(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Index into b of the nearest point to each row of a."""
    return np.linalg.norm(a[:, None, :] - b[None, :, :], axis=-1).argmin(axis=1)


def isl_edges(fleet: Fleet, pos: np.ndarray, design: cfg.Design | str):
    """(i, j, km, hop_s, acquire) arrays of the crosslinks that close at one instant.

    Per shell (cfg.ShellIsl): fore/aft in the plane, and to the nearest terminal-carrying satellite in the next
    plane (every satellite, or a relay subset; both sides = +Grid, one side on alternate satellites = brick).
    A Walker star has a seam between its last and first plane (counter-rotating), which is left unlinked.
    With design.inter_shell, each satellite of the smaller shell links optically to the nearest in the other.
    hop_s = distance / c + per-hop processing + alarm transmission time. acquire marks optical links whose
    partner can change (cross-plane, inter-shell): those pay the acquisition time when it does.
    A mode string ("grid", "inplane", "none") applies to every shell, as in the 05 study.
    """
    if isinstance(design, str):
        design = cfg.Design(fleet.d.name, fleet.d.shells, design)
    chunks = []   # (i, j, tech, partner can change)
    for w, off in zip(fleet.shells, fleet.offset):
        s, isl = w.s, design.shell_isl(w.s)
        P, S = s.planes, s.sats_per_plane
        k = np.arange(s.size)
        if isl.tech_in != "none" and S > 1:
            nxt = w.plane * S + (w.slot + 1) % S
            keep = ~((S == 2) & (nxt < k))
            chunks.append((off + k[keep], off + nxt[keep], isl.tech_in, False))
        if isl.tech_x != "none" and isl.cross > 0 and P > 1:
            carriers = np.flatnonzero(np.arange(S) % isl.relay_every == 0)
            p = pos[off:off + s.size].reshape(P, S, 3)[:, carriers]
            q = np.roll(p, -1, axis=0)                                   # plane p+1
            nearest = np.linalg.norm(p[:, :, None, :] - q[:, None, :, :], axis=-1).argmin(axis=2)
            planes = np.arange(P) if s.pattern == "delta" and P > 2 else np.arange(P - 1)
            for pl in planes:
                src = np.arange(len(carriers))
                if isl.cross == 1:   # brick: alternate carriers link to the next plane, the rest receive
                    src = src[(src + pl) % 2 == 0]
                i, j = off + pl * S + carriers[src], off + ((pl + 1) % P) * S + carriers[nearest[pl, src]]
                if isl.polar_off_deg < 90:
                    lat_i = np.degrees(np.arcsin(pos[i, 2] / np.linalg.norm(pos[i], axis=1)))
                    lat_j = np.degrees(np.arcsin(pos[j, 2] / np.linalg.norm(pos[j], axis=1)))
                    on = ~((np.abs(lat_i) > isl.polar_off_deg) & (np.abs(lat_j) > isl.polar_off_deg))
                    i, j = i[on], j[on]
                chunks.append((i, j, isl.tech_x, True))
    if design.inter_shell and len(fleet.shells) > 1:
        for a in range(len(fleet.shells)):
            for b in range(a + 1, len(fleet.shells)):
                (sa, oa), (sb, ob) = sorted([(fleet.shells[a].s.size, fleet.offset[a]),
                                             (fleet.shells[b].s.size, fleet.offset[b])])
                i = oa + np.arange(sa)
                chunks.append((i, ob + _nearest(pos[i], pos[ob:ob + sb]), "optical", True))
    if not chunks:
        e = np.array([], int)
        return e, e, np.array([]), np.array([]), np.array([], bool)
    I = np.concatenate([c[0] for c in chunks]).astype(int)
    J = np.concatenate([c[1] for c in chunks]).astype(int)
    km = np.linalg.norm(pos[I] - pos[J], axis=1)
    rate = np.concatenate([link_rate_bps(c[2], km[n:n + len(c[0])])
                           for c, n in zip(chunks, np.cumsum([0] + [len(c[0]) for c in chunks]))])
    acquire = np.concatenate([np.full(len(c[0]), c[3] and cfg.ISL_TECH[c[2]].acquisition_s > 0) for c in chunks])
    with np.errstate(divide="ignore", invalid="ignore"):   # coincident satellites (two identical shells)
        ok = (rate > 0) & clear_of_earth(pos[I], pos[J])
    with np.errstate(divide="ignore"):
        hop_s = prop_delay_s(km) + cfg.ISL_HOP_PROC_S + cfg.ALARM_BYTES * 8 / rate
    return I[ok], J[ok], km[ok], hop_s[ok], acquire[ok]


# --- Model ---------------------------------------------------------------------------
@dataclass
class Result:
    design: cfg.Design
    lat: np.ndarray            # (G,) grid
    lon: np.ndarray
    latency: np.ndarray        # (G, T) seconds, inf where not served
    in_view: np.ndarray        # (G, T) satellites usable by the terminal
    step_s: float
    isl_links: float           # mean ISL count per step

    def summary(self) -> dict:
        L, step = self.latency, self.step_s
        served = np.isfinite(L)
        cov = served.mean(axis=1)                       # per point, fraction of time served
        gaps = _longest_run(~served) * step / 60
        vals = L[served]
        q = (lambda p: float(np.quantile(vals, p))) if vals.size else (lambda p: np.nan)
        with warnings.catch_warnings():   # points never served have an all-NaN row
            warnings.simplefilter("ignore", RuntimeWarning)
            pt_p95 = np.where(cov > 0, np.nanquantile(np.where(served, L, np.nan), 0.95, axis=1), np.inf)
        out = dict(
            design=self.design.name, shells=self.design.label, isl=self.design.isl, sats=self.design.size,
            grid_points=len(self.lat),
            coverage_mean=float(cov.mean()),                 # equal-area grid: share of Earth x time served
            coverage_worst_point=float(cov.min()),
            full_coverage=bool(served.all()),
            area_always_served=float((cov == 1).mean()),
            max_gap_min=float(gaps.max()),
            worst_gap_lat=float(self.lat[gaps.argmax()]) if gaps.max() > 0 else np.nan,
            min_sats_in_view=int(self.in_view.min()),
            mean_sats_in_view=float(self.in_view.mean()),
            latency_p50_ms=q(0.5) * 1e3, latency_p95_ms=q(0.95) * 1e3, latency_p99_ms=q(0.99) * 1e3,
            latency_max_ms=(float(vals.max()) * 1e3) if vals.size else np.nan,
            worst_point_p95_ms=float(pt_p95.max()) * 1e3,
            mean_isl_links=self.isl_links,
        )
        for t in cfg.TIERS_S:   # counted over all place-time samples, so outages count as misses
            out[f"within_{int(t * 1e3)}ms"] = float((L < t).mean())
        return out

    def by_latitude(self, band_deg: float = 10.0):
        """Coverage and latency per latitude band, for spotting where a design is weak."""
        import pandas as pd
        served = np.isfinite(self.latency)
        rows = []
        for lo in np.arange(-90, 90, band_deg):
            m = (self.lat >= lo) & (self.lat < lo + band_deg)
            if not m.any():
                continue
            v = self.latency[m][served[m]]
            rows.append(dict(band=f"{lo:+.0f}..{lo + band_deg:+.0f}", coverage=served[m].mean(),
                             max_gap_min=float(_longest_run(~served[m]).max() * self.step_s / 60),
                             p50_ms=np.median(v) * 1e3 if v.size else np.nan,
                             p95_ms=np.quantile(v, 0.95) * 1e3 if v.size else np.nan))
        return pd.DataFrame(rows)


def evaluate(design: cfg.Design, hours: float = 24, step_s: float = 60, grid_points: int = 2000,
             blocked: frozenset[str] = frozenset(), failed: frozenset[int] = frozenset()) -> Result:
    """blocked: gateway names taken offline. failed: satellite indices (into the stacked fleet) that are dead."""
    fleet = Fleet(design)
    lat, lon = fibonacci_grid(grid_points)
    grid_xyz = geodetic_to_ecef(lat, lon)

    gws = [g for g in cfg.GATEWAYS if g.name not in blocked]
    gw_xyz = geodetic_to_ecef(np.array([g.lat for g in gws]), np.array([g.lon for g in gws]))
    # gateway -> nearest PoP over terrestrial fibre (+ GEO backhaul where there is no fibre)
    pop_lat, pop_lon = np.array([p.lat for p in cfg.POPS]), np.array([p.lon for p in cfg.POPS])
    gw_ground_s = np.array([
        cfg.GROUND_PROC_S + g.backhaul_s
        + great_circle_km(g.lat, g.lon, pop_lat, pop_lon).min() * cfg.FIBRE_ROUTE_FACTOR / cfg.FIBRE_KM_S
        for g in gws])

    sin_el_t = np.sin(np.radians(cfg.TERMINAL_MIN_EL_DEG))
    sin_el_g = np.sin(np.radians(cfg.GATEWAY_MIN_EL_DEG))
    access_s = cfg.RACH_ACCESS_S + cfg.GNB_PROC_S
    N = fleet.size
    steps = int(hours * 3600 / step_s)
    latency = np.full((grid_points, steps), np.inf, dtype=np.float32)
    in_view = np.zeros((grid_points, steps), dtype=np.int16)
    n_isl = 0
    dead = np.zeros(fleet.size, bool)
    dead[list(failed)] = True
    locked = np.array([], np.int64)   # optical partners held at the previous step (sorted pair keys)

    for k in range(steps):
        pos = fleet.ecef(k * step_s)

        # Satellite -> ground cost: best open gateway in view of each satellite.
        se_g, rng_g = elevation_and_range(gw_xyz, pos)
        down = np.where(se_g >= sin_el_g, prop_delay_s(rng_g) + gw_ground_s[:, None], np.inf).min(axis=0)
        down[dead] = np.inf

        # Super-source node N reaches every satellite through its feeder; Dijkstra spreads it over the mesh.
        I, J, _, w, acquire = isl_edges(fleet, pos, design)
        alive = ~(dead[I] | dead[J])
        I, J, w, acquire = I[alive], J[alive], w[alive], acquire[alive]
        if design.acquisition:   # a new optical partner is still being acquired during its first step
            key = np.minimum(I, J).astype(np.int64) * (N + 1) + np.maximum(I, J)
            new = acquire & ~np.isin(key, locked)
            locked = np.sort(key[acquire])
            I, J, w = I[~new], J[~new], w[~new]
        n_isl += len(I)
        has_gw = np.flatnonzero(np.isfinite(down))
        rows = np.concatenate([I, J, np.full(len(has_gw), N)])
        cols = np.concatenate([J, I, has_gw])
        G = coo_matrix((np.concatenate([w, w, down[has_gw]]), (rows, cols)), shape=(N + 1, N + 1)).tocsr()
        to_ground = dijkstra(G, directed=True, indices=N)[:N]

        # Terminal side: every usable satellite, pick the fastest end-to-end.
        se_t, rng_t = elevation_and_range(grid_xyz, pos)
        rate = user_rate_bps(rng_t)
        usable = (se_t >= sin_el_t) & (rate > 0) & ~dead[None, :]
        in_view[:, k] = usable.sum(axis=1)
        with np.errstate(divide="ignore"):
            up = cfg.ALARM_BYTES * 8 / rate + prop_delay_s(rng_t)
        total = np.where(usable, up + to_ground[None, :], np.inf).min(axis=1)
        latency[:, k] = total + access_s

    return Result(design, lat, lon, latency, in_view, step_s, n_isl / max(steps, 1))


def _longest_run(mask: np.ndarray) -> np.ndarray:
    """Longest run of True along axis 1, per row."""
    best = np.zeros(mask.shape[0], dtype=int)
    run = np.zeros(mask.shape[0], dtype=int)
    for col in mask.T:
        run = np.where(col, run + 1, 0)
        best = np.maximum(best, run)
    return best
