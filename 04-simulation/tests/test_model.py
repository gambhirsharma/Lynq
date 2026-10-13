"""Sanity checks against the closed-form numbers in 01-research/04-TECHNICAL-deep-dive.md."""
import numpy as np
import pytest

from ntnpulse import config as cfg
from ntnpulse.engine import run
from ntnpulse.geometry import (
    WalkerConstellation, elevation_and_range, geodetic_to_ecef, line_of_sight, slant_range_km,
)
from ntnpulse.links import fspl_db, isl_edges


def test_slant_range_matches_research_table():
    assert slant_range_km(550, 10) == pytest.approx(1815, abs=2)     # 6.05 ms one way
    assert slant_range_km(550, 30) == pytest.approx(993, abs=2)
    assert slant_range_km(1200, 10) == pytest.approx(3131, abs=3)


def test_orbit_radius_and_period():
    w = WalkerConstellation(cfg.CONSTELLATIONS[30])
    for t in (0, 1234, 5000):
        assert np.allclose(np.linalg.norm(w.ecef(t), axis=1), cfg.RE_KM + 550)
    assert w.period_s / 60 == pytest.approx(95.6, abs=0.2)


def test_elevation_overhead_is_90():
    sat = geodetic_to_ecef(np.array([57.0]), np.array([3.0]), 550)
    gnd = geodetic_to_ecef(np.array([57.0]), np.array([3.0]))
    el, rng = elevation_and_range(gnd, sat)
    assert el[0, 0] == pytest.approx(90)
    assert rng[0, 0] == pytest.approx(550)


def test_fspl():
    assert fspl_db(1815, 2000) == pytest.approx(163.6, abs=0.1)


def test_intra_plane_ring_needs_enough_satellites():
    # 6 per plane: neighbours 60 deg apart, Earth blocks the link. 10 per plane: ring closes (~4,280 km).
    w6 = WalkerConstellation(cfg.CONSTELLATIONS[12])
    assert not [e for e in isl_edges(w6, w6.ecef(0)) if e[3] == "rf"]
    w10 = WalkerConstellation(cfg.CONSTELLATIONS[30])
    rf = [e for e in isl_edges(w10, w10.ecef(0)) if e[3] == "rf"]
    assert len(rf) == 30
    assert rf[0][2] == pytest.approx(2 * (cfg.RE_KM + 550) * np.sin(np.pi / 10), rel=1e-6)


def test_line_of_sight():
    a = geodetic_to_ecef(np.array([0.0]), np.array([0.0]), 550)[0]
    assert not line_of_sight(a, -a)
    assert line_of_sight(a, geodetic_to_ecef(np.array([0.0]), np.array([10.0]), 550)[0])


@pytest.fixture(scope="module")
def short_runs():
    sc = cfg.Scenario(duration_s=4 * 3600, terminals=120, blocked_gateways=frozenset({"Stavanger"}))
    return {m: run(sc.with_(mode=m)) for m in cfg.MODES}


def test_routing_is_always_compliant(short_runs):
    for r in short_runs.values():
        assert r.records.compliant.all()


def test_bent_pipe_never_uses_isl_or_onboard_storage(short_runs):
    r = short_runs["bent_pipe"].records
    assert (r.isl_hops == 0).all()
    assert (r.path != "store_forward").all()


def test_isl_improves_norwegian_latency_when_stavanger_blocked(short_runs):
    def p50(m):
        r = short_runs[m].records
        return r[r.sector == "NO"].latency_s.median()
    assert p50("regen_isl") < p50("regen") <= p50("bent_pipe") * 1.5
    assert (short_runs["regen_isl"].records.isl_hops > 0).any()


def test_critical_latency_floor_is_physical(short_runs):
    crit = short_runs["regen_isl"].records.query("cls == 'critical'")
    assert crit.latency_s.min() > 2 * 550 / cfg.C_KM_S     # at least up + down at zenith
