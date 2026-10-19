"""The extended ISL model must reproduce the 05 study when every shell flies the default optical +Grid."""
import pytest

from globalnet import config as cfg
from globalnet.model import evaluate


def _short(d):
    return evaluate(d, hours=2, step_s=120, grid_points=500).summary()


def test_explicit_optical_grid_equals_mode_string():
    base = cfg.PRESETS["polar-1200-120"]
    s = base.shells[0]
    explicit = cfg.Design("x", (cfg.Shell(s.planes, s.sats_per_plane, s.altitude_km, s.inclination_deg, s.pattern,
                                          s.phasing, cfg.ShellIsl()),))
    a, b = _short(base), _short(explicit)
    assert a["coverage_mean"] == pytest.approx(b["coverage_mean"])
    assert a["latency_p99_ms"] == pytest.approx(b["latency_p99_ms"], abs=0.1)


def test_preset_matches_05_results_table():
    # 05-global-coverage/README.md: polar-1200-120 at 24 h / 60 s / 2,000 points gives p50 78, p99 102 ms.
    # A shorter run must stay close to that.
    s = evaluate(cfg.PRESETS["polar-1200-120"], hours=3, step_s=60, grid_points=2000).summary()
    assert s["full_coverage"]
    assert s["latency_p50_ms"] == pytest.approx(78, abs=2)
    assert s["latency_p99_ms"] == pytest.approx(102, abs=3)
