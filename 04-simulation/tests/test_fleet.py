"""Fleet orchestration twin: rollout ordering, limits and the value of the ISL control path."""
import pytest

from ntnpulse import config as cfg
from ntnpulse.fleet import run_rollout

BASE = cfg.FleetScenario(duration_s=12 * 3600, step_s=20.0)


@pytest.fixture(scope="module")
def runs():
    return {
        "isl": run_rollout(BASE),
        "no_isl": run_rollout(BASE.with_(isl=False, peer_sharing=False, duration_s=24 * 3600)),
        "today": run_rollout(BASE.with_(constellation=cfg.CONSTELLATIONS[12], isl=False, peer_sharing=False)),
    }


def test_never_more_than_wave_size_down(runs):
    for r in runs.values():
        assert r.series.restarting.max() <= BASE.wave_size


def test_ordering_image_then_applied_then_reported(runs):
    s = runs["isl"].sats
    assert s.reported_h.notna().all()
    assert (s.image_h <= s.applied_h).all() and (s.applied_h <= s.reported_h).all()


def test_canary_goes_first_and_alone(runs):
    s = runs["isl"].sats
    canary = s[s.wave == 0]
    assert len(canary) == 1
    assert canary.applied_h.iloc[0] < s[s.wave > 0].applied_h.min()


def test_isl_keeps_the_fleet_reachable_and_speeds_up_rollout(runs):
    isl, no_isl = runs["isl"].summary(), runs["no_isl"].summary()
    assert isl["reachable_mean"] > 0.95 > 0.5 > no_isl["reachable_mean"]
    assert isl["fleet_updated_h"] < no_isl["fleet_updated_h"]


def test_untuned_kubernetes_flaps_on_todays_fleet(runs):
    s = runs["today"].summary()
    assert s["notready_per_sat_day"] > 5
    assert s["max_gap_min"] > 60


def test_avoid_basin_means_no_service_outage(runs):
    assert runs["isl"].impact_s == 0


def test_peer_sharing_offloads_ground():
    r = run_rollout(BASE.with_(prestage=False))
    assert r.peer_bytes > 0
    assert r.ground_bytes + r.peer_bytes == pytest.approx(30 * BASE.image_mb * 1e6)
