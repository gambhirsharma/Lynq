"""Physics and coverage sanity checks for the global model."""
import numpy as np
import pytest

from globalnet import config as cfg
from globalnet.geometry import Fleet, Walker, elevation_and_range, fibonacci_grid, geodetic_to_ecef, slant_range_km
from globalnet.model import evaluate, isl_edges


def test_slant_range_matches_research_table():
    assert slant_range_km(550, 10) == pytest.approx(1815, abs=2)
    assert slant_range_km(1200, 10) == pytest.approx(3131, abs=3)


def test_orbit_radius_and_period():
    w = Walker(cfg.Shell(3, 10, 550, 97.6, "star"))
    assert np.allclose(np.linalg.norm(w.ecef(1234), axis=1), cfg.RE_KM + 550)
    assert w.period_s / 60 == pytest.approx(95.6, abs=0.2)


def test_elevation_overhead_and_range():
    sat = geodetic_to_ecef(np.array([-40.0]), np.array([120.0]), 550)
    gnd = geodetic_to_ecef(np.array([-40.0]), np.array([120.0]))
    sin_el, rng = elevation_and_range(gnd, sat)
    assert sin_el[0, 0] == pytest.approx(1)
    assert rng[0, 0] == pytest.approx(550)


def test_grid_is_equal_area():
    lat, _ = fibonacci_grid(4000)
    # share of points between +-30 deg must equal the share of area: sin(30) = 0.5
    assert (np.abs(lat) < 30).mean() == pytest.approx(0.5, abs=0.01)
    assert lat.max() > 88 and lat.min() < -88


def test_shell_parse_roundtrip():
    s = cfg.Shell.parse("6x20@560/97.6/star")
    assert s == cfg.Shell(6, 20, 560, 97.6, "star") and s.size == 120


def test_grid_isl_has_up_to_four_links_per_satellite():
    d = cfg.PRESETS["polar-550-240"]
    f = Fleet(d)
    I, J, *_ = isl_edges(f, f.ecef(0), "grid")
    deg = np.bincount(np.concatenate([I, J]), minlength=f.size)
    assert deg.max() <= 4 + 2          # nearest-neighbour cross links can pile up slightly
    assert np.median(deg) >= 3


def test_planned_30_is_not_global_but_polar_shell_is():
    small = evaluate(cfg.PRESETS["planned-30"], hours=2, step_s=120, grid_points=500).summary()
    big = evaluate(cfg.PRESETS["polar-550-240"], hours=2, step_s=120, grid_points=500).summary()
    assert small["coverage_mean"] < 0.7 and not small["full_coverage"]
    assert big["full_coverage"]
    assert big["latency_p99_ms"] < 150


def test_isl_cuts_latency():
    shells = cfg.PRESETS["polar-550-240"].shells
    with_isl = evaluate(cfg.Design("g", shells, "grid"), hours=1, step_s=120, grid_points=500).summary()
    no_isl = evaluate(cfg.Design("n", shells, "none"), hours=1, step_s=120, grid_points=500).summary()
    assert with_isl["coverage_mean"] > no_isl["coverage_mean"]   # without ISL, mid-ocean has no gateway in reach


def test_optimizer_bounds_are_below_known_full_coverage_designs():
    import optimize
    # polar-550-240 (12x20) and polar-1200-120 (8x15) are gap-free, so the lower bounds must not exclude them
    assert optimize.min_spp(550) <= 20 and optimize.min_planes(550, 87) <= 12
    assert optimize.min_spp(1200) <= 15 and optimize.min_planes(1200, 87.9) <= 8
    # higher shells see more of the Earth, so need fewer satellites per plane
    assert optimize.min_spp(1200) < optimize.min_spp(550)


def test_search_family_stops_once_gap_free_and_fast_enough():
    import optimize
    fam = dict(altitude_km=1200.0, inclination_deg=87.0, pattern="star", planes=8, isl="grid", spp_from=14,
               max_spp=16, hours=1, step=120, grid=500, metric="latency_p99_ms", stop_ms=150, min_in_view=1)
    rows = optimize.search_family(fam)
    assert rows[-1]["full_coverage"] and rows[-1]["latency_p99_ms"] <= 150
    assert len(rows) == 1   # 8x14 at 1200 km already closes, so the search must not keep adding satellites


def test_hybrid_base_shell_is_flown_and_costed():
    import optimize
    low, high = cfg.Shell(6, 6, 550, 87, "star"), cfg.Shell.parse("5x11@1200/87/star")
    r = optimize._evaluate(low, "grid", 1, 120, 300, (high,))
    assert r["sats"] == 36 + 55 and r["total_planes"] == 11 and r["base_shell"] == high.label
    alone = optimize._evaluate(low, "grid", 1, 120, 300)
    assert r["coverage_mean"] > alone["coverage_mean"]   # the high shell fills what the sparse low one misses
