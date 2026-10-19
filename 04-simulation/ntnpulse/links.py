"""Link budget and inter-satellite link topology."""
from __future__ import annotations

import numpy as np

from .config import (
    IMPL_EFFICIENCY, K_BOLTZMANN_DBW, LINK_LOSSES_DB, MAX_USER_RATE_BPS, MIN_SNR_DB,
    OPTICAL_ISL_MAX_KM, RF_ISL_MAX_KM, SAT_GT_DBK, SERVICE_BW_HZ, SERVICE_FREQ_MHZ,
    TERMINAL_EIRP_DBW,
)
from .geometry import WalkerConstellation, line_of_sight


def fspl_db(d_km, f_mhz=SERVICE_FREQ_MHZ):
    return 20 * np.log10(d_km) + 20 * np.log10(f_mhz) + 32.44


def uplink_snr_db(d_km):
    """Terminal -> satellite SNR on one NB-IoT carrier."""
    return (TERMINAL_EIRP_DBW - fspl_db(d_km) - LINK_LOSSES_DB + SAT_GT_DBK
            - K_BOLTZMANN_DBW - 10 * np.log10(SERVICE_BW_HZ))


def user_rate_bps(d_km):
    """Achievable per-user rate: derated Shannon, capped; 0 if the link closes below MIN_SNR_DB."""
    snr_db = uplink_snr_db(d_km)
    rate = IMPL_EFFICIENCY * SERVICE_BW_HZ * np.log2(1 + 10 ** (snr_db / 10))
    return np.where(snr_db >= MIN_SNR_DB, np.minimum(rate, MAX_USER_RATE_BPS), 0.0)


def isl_edges(w: WalkerConstellation, pos: np.ndarray):
    """ISL edges for one instant: (i, j, km, kind) with kind 'rf' or 'optical'.

    In-plane (RF): each satellite links to its in-plane neighbours if in range and above the atmosphere.
    Cross-plane (c.cross_isl): each equipped satellite links to the nearest equipped satellite in each
    adjacent plane. With link_seam off, the last plane is not linked back to the first.
    """
    c = w.c
    S, P = c.sats_per_plane, c.planes
    edges = []
    if S > 1:
        for k in range(c.size):
            nxt = w.plane[k] * S + (w.slot[k] + 1) % S
            if S == 2 and nxt < k:
                continue
            d = float(np.linalg.norm(pos[k] - pos[nxt]))
            if d <= RF_ISL_MAX_KM and line_of_sight(pos[k], pos[nxt]):
                edges.append((k, nxt, d, "rf"))
    if P > 1:
        opt = np.flatnonzero(w.optical)
        max_km = OPTICAL_ISL_MAX_KM if c.cross_isl == "optical" else RF_ISL_MAX_KM
        for p in range(P):
            q = (p + 1) % P
            if (P == 2 or not c.link_seam) and q < p:
                continue
            for k in opt[w.plane[opt] == p]:
                cand = opt[w.plane[opt] == q]
                dists = np.linalg.norm(pos[cand] - pos[k], axis=1)
                j = int(cand[np.argmin(dists)])
                d = float(dists.min())
                if d <= max_km and line_of_sight(pos[k], pos[j]):
                    edges.append((int(k), j, d, c.cross_isl))
    return edges
