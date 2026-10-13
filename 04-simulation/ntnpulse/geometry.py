"""Orbits and visibility. Circular Keplerian orbits in a rotating Earth (no J2: fine for a day)."""
from __future__ import annotations

import numpy as np

from .config import C_KM_S, GRAZING_ALT_KM, MU_KM3_S2, OMEGA_E, RE_KM, Constellation


def geodetic_to_ecef(lat_deg, lon_deg, alt_km=0.0):
    lat, lon = np.radians(lat_deg), np.radians(lon_deg)
    r = RE_KM + alt_km
    return np.stack([r * np.cos(lat) * np.cos(lon), r * np.cos(lat) * np.sin(lon), r * np.sin(lat)], axis=-1)


def ecef_to_latlon(xyz):
    x, y, z = xyz[..., 0], xyz[..., 1], xyz[..., 2]
    return np.degrees(np.arctan2(z, np.hypot(x, y))), np.degrees(np.arctan2(y, x))


class WalkerConstellation:
    """Walker i:T/P/F. Satellite k is in plane k // S, slot k % S."""

    def __init__(self, c: Constellation):
        self.c = c
        self.r = RE_KM + c.altitude_km
        self.n = np.sqrt(MU_KM3_S2 / self.r**3)          # mean motion, rad/s
        self.period_s = 2 * np.pi / self.n
        P, S = c.planes, c.sats_per_plane
        k = np.arange(c.size)
        self.plane = k // S
        self.slot = k % S
        self.raan = np.radians(self.plane * c.raan_spread_deg / P)
        self.u0 = 2 * np.pi * (self.slot / S + c.phasing * self.plane / c.size)
        self.inc = np.radians(c.inclination_deg)
        self.optical = (self.slot % c.optical_every) == 0

    def ecef(self, t_s: float) -> np.ndarray:
        """(N, 3) satellite positions in km, Earth-fixed frame."""
        u = self.u0 + self.n * t_s
        x_orb, y_orb = self.r * np.cos(u), self.r * np.sin(u)
        ci, si = np.cos(self.inc), np.sin(self.inc)
        lon_node = self.raan - OMEGA_E * t_s       # ascending node in the rotating frame
        cO, sO = np.cos(lon_node), np.sin(lon_node)
        x = cO * x_orb - sO * ci * y_orb
        y = sO * x_orb + cO * ci * y_orb
        z = si * y_orb
        return np.stack([x, y, z], axis=-1)


def elevation_and_range(ground_xyz: np.ndarray, sat_xyz: np.ndarray):
    """Elevation (deg) and slant range (km) for every ground x satellite pair: (G, N) arrays."""
    d = sat_xyz[None, :, :] - ground_xyz[:, None, :]
    rng = np.linalg.norm(d, axis=-1)
    up = ground_xyz / np.linalg.norm(ground_xyz, axis=-1, keepdims=True)
    sin_el = np.einsum("gnk,gk->gn", d, up) / rng
    return np.degrees(np.arcsin(np.clip(sin_el, -1, 1))), rng


def slant_range_km(alt_km: float, el_deg: float) -> float:
    """Closed-form slant range at a given elevation (used to sanity-check the engine)."""
    e = np.radians(el_deg)
    r = RE_KM + alt_km
    return float(np.sqrt(r**2 - (RE_KM * np.cos(e)) ** 2) - RE_KM * np.sin(e))


def line_of_sight(a: np.ndarray, b: np.ndarray) -> bool:
    """True if segment a-b stays above the atmosphere (min altitude > GRAZING_ALT_KM)."""
    d = b - a
    t = np.clip(-np.dot(a, d) / np.dot(d, d), 0.0, 1.0)
    return np.linalg.norm(a + t * d) > RE_KM + GRAZING_ALT_KM


def great_circle_km(lat1, lon1, lat2, lon2) -> float:
    p1, p2 = np.radians([lat1, lat2])
    dl = np.radians(lon2 - lon1)
    cos_c = np.sin(p1) * np.sin(p2) + np.cos(p1) * np.cos(p2) * np.cos(dl)
    return float(RE_KM * np.arccos(np.clip(cos_c, -1, 1)))


def prop_delay_s(km) -> float:
    return km / C_KM_S
