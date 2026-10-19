"""RF vs optical crosslinks, terminal counts, relay subsets, polar shutoff, inter-shell links, acquisition."""
import numpy as np
import pytest

from globalnet import config as cfg
from globalnet.geometry import Fleet
from globalnet.model import evaluate, isl_edges, link_rate_bps


def _edges(shells, **kw):
    d = cfg.Design("t", tuple(shells), **kw)
    f = Fleet(d)
    return f, isl_edges(f, f.ecef(0), d)


def test_rf_range_comes_from_the_link_budget():
    assert link_rate_bps("rf", np.array([1000.0]))[0] > 3e6
    assert link_rate_bps("rf", np.array([2500.0]))[0] > 1e6
    assert link_rate_bps("rf", np.array([4000.0]))[0] == 0      # below the 1 Mbps floor
    assert link_rate_bps("optical", np.array([5900.0]))[0] == 100e6


def test_rf_drops_sparse_links_optical_keeps_them():
    # 6x11 at 800 km: in-plane neighbours ~4,000 km apart, beyond RF, within optical
    opt = cfg.Shell(6, 11, 800, 87, "star", 1, cfg.ShellIsl("optical", "none", 0))
    rf = cfg.Shell(6, 11, 800, 87, "star", 1, cfg.ShellIsl("rf", "none", 0))
    assert len(_edges([opt])[1][0]) == 66
    assert len(_edges([rf])[1][0]) == 0


def test_rf_hop_is_slower_than_optical():
    opt = cfg.Shell(12, 20, 550, 87, "star", 1, cfg.ShellIsl("optical", "none", 0))
    rf = cfg.Shell(12, 20, 550, 87, "star", 1, cfg.ShellIsl("rf", "none", 0))
    assert _edges([rf])[1][3].mean() > _edges([opt])[1][3].mean() + 2e-4   # 200 B at a few Mbps


def test_brick_and_relay_subset_have_fewer_cross_links():
    s = lambda isl: cfg.Shell(12, 20, 550, 87, "star", 1, isl)
    n = lambda isl: int(_edges([s(isl)])[1][4].sum())    # cross-plane links are the ones flagged for acquisition
    grid, brick, relay = n(cfg.ShellIsl()), n(cfg.ShellIsl(cross=1)), n(cfg.ShellIsl(relay_every=4))
    assert brick == pytest.approx(grid / 2, rel=0.1)
    assert relay == pytest.approx(grid / 4, rel=0.1)


def test_polar_shutoff_removes_cross_links_near_the_poles():
    on = cfg.Shell(12, 20, 550, 87, "star", 1, cfg.ShellIsl())
    off = cfg.Shell(12, 20, 550, 87, "star", 1, cfg.ShellIsl(polar_off_deg=70))
    assert _edges([off])[1][4].sum() < _edges([on])[1][4].sum()


def test_inter_shell_links_connect_shells():
    low, high = cfg.Shell(6, 10, 550, 53, "delta"), cfg.Shell(5, 11, 1200, 87, "star")
    f, (I, J, *_) = _edges([low, high], inter_shell=True)
    crosses = ((I < 60) & (J >= 60)) | ((I >= 60) & (J < 60))
    assert crosses.sum() > 30
    _, (I0, J0, *_) = _edges([low, high])
    assert not (((I0 < 60) & (J0 >= 60)) | ((I0 >= 60) & (J0 < 60))).any()


def test_acquisition_and_failures_cost_coverage_or_latency():
    shells = cfg.PRESETS["polar-550-240"].shells
    base = evaluate(cfg.Design("a", shells), hours=1, step_s=120, grid_points=400).summary()
    acq = evaluate(cfg.Design("b", shells, acquisition=True), hours=1, step_s=120, grid_points=400).summary()
    assert acq["mean_isl_links"] < base["mean_isl_links"]
    dead = evaluate(cfg.Design("c", shells), hours=1, step_s=120, grid_points=400,
                    failed=frozenset(range(0, 240, 2))).summary()
    assert dead["coverage_mean"] < base["coverage_mean"]
