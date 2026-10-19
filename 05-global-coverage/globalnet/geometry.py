"""Orbits, the global grid and visibility. Circular Keplerian orbits in a rotating Earth (no J2: fine for a day)."""
from __future__ import annotations

import numpy as np

from .config import C_KM_S, GRAZING_ALT_KM, MU_KM3_S2, OMEGA_E, PATTERNS, RE_KM, Design, Shell


def geodetic_to_ecef(lat_deg, lon_deg, alt_km=0.0):
    lat, lon = np.radians(lat_deg), np.radians(lon_deg)
    r = RE_KM + alt_km
    return np.stack([r * np.cos(lat) * np.cos(lon), r * np.cos(lat) * np.sin(lon), r * np.sin(lat)], axis=-1)


def fibonacci_grid(n: int):
    """n near-equal-area points over the whole sphere: (lat, lon) in degrees. Every point stands for the same area."""
    i = np.arange(n) + 0.5
    lat = np.degrees(np.arcsin(1 - 2 * i / n))
    lon = (np.degrees(np.pi * (1 + 5**0.5) * i) + 180) % 360 - 180
    return lat, lon


class Walker:
    """Walker i:T/P/F shell. Satellite k is in plane k // S, slot k % S."""

    def __init__(self, s: Shell):
        self.s = s
        self.r = RE_KM + s.altitude_km
        self.n = np.sqrt(MU_KM3_S2 / self.r**3)
        self.period_s = 2 * np.pi / self.n
        P, S = s.planes, s.sats_per_plane
        k = np.arange(s.size)
        self.plane, self.slot = k // S, k % S
        self.raan = np.radians(self.plane * PATTERNS[s.pattern] / P)
        self.u0 = 2 * np.pi * (self.slot / S + s.phasing * self.plane / s.size)
        self.inc = np.radians(s.inclination_deg)

    def ecef(self, t_s: float) -> np.ndarray:
        u = self.u0 + self.n * t_s
        x_orb, y_orb = self.r * np.cos(u), self.r * np.sin(u)
        ci, si = np.cos(self.inc), np.sin(self.inc)
        lon_node = self.raan - OMEGA_E * t_s
        cO, sO = np.cos(lon_node), np.sin(lon_node)
        return np.stack([cO * x_orb - sO * ci * y_orb, sO * x_orb + cO * ci * y_orb, si * y_orb], axis=-1)


class Fleet:
    """All shells of a design, stacked into one satellite index."""

    def __init__(self, d: Design):
        self.d = d
        self.shells = [Walker(s) for s in d.shells]
        self.offset = np.cumsum([0] + [s.size for s in d.shells])[:-1]
        self.size = d.size

    def ecef(self, t_s: float) -> np.ndarray:
        return np.concatenate([w.ecef(t_s) for w in self.shells])


def elevation_and_range(ground_xyz: np.ndarray, sat_xyz: np.ndarray):
    """sin(elevation) and slant range (km) for every ground x satellite pair, (G, N), via one matmul."""
    rg = np.linalg.norm(ground_xyz, axis=1)
    rs2 = np.einsum("nk,nk->n", sat_xyz, sat_xyz)
    gs = ground_xyz @ sat_xyz.T
    rng = np.sqrt(np.maximum(rs2[None, :] + rg[:, None] ** 2 - 2 * gs, 1e-9))
    sin_el = (gs / rg[:, None] - rg[:, None]) / rng
    return sin_el, rng


def slant_range_km(alt_km: float, el_deg: float) -> float:
    e = np.radians(el_deg)
    r = RE_KM + alt_km
    return float(np.sqrt(r**2 - (RE_KM * np.cos(e)) ** 2) - RE_KM * np.sin(e))


def clear_of_earth(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Row-wise: True if segment a-b stays above the atmosphere (min altitude > GRAZING_ALT_KM)."""
    d = b - a
    t = np.clip(-np.einsum("nk,nk->n", a, d) / np.einsum("nk,nk->n", d, d), 0.0, 1.0)
    return np.linalg.norm(a + t[:, None] * d, axis=1) > RE_KM + GRAZING_ALT_KM


def great_circle_km(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dl = np.radians(np.asarray(lon2) - np.asarray(lon1))
    cos_c = np.sin(p1) * np.sin(p2) + np.cos(p1) * np.cos(p2) * np.cos(dl)
    return RE_KM * np.arccos(np.clip(cos_c, -1, 1))


def prop_delay_s(km):
    return km / C_KM_S
