"""Cost model: calibrated to the proposal, and it moves the right way with altitude and terminals."""
import pytest

import costmodel as cm
from globalnet import config as cfg

RF_ONLY = cfg.ShellIsl("rf", "none", 0)


def _design(alt=550.0, isl=RF_ONLY, planes=9, spp=10):
    return cfg.Design("t", (cfg.Shell(planes, spp, alt, 97.6, "star", 1, isl),))


def test_proposal_calibration():
    # 01-research/08-OUR-PROPOSAL.md: 90 sats at ~EUR 0.75 M all-in, ~EUR 68 M capex, EUR 13.5 M/yr replenishment
    d = _design()
    sat = cm.satellite(d.shells[0], cm.terminals(d)[0], cm.CostParams())
    assert sat["bus"] == "12U"
    all_in = sat["unit_meur"] + sat["mass_kg"] * cm.CostParams().launch_meur_per_kg
    assert all_in == pytest.approx(0.75, abs=0.05)
    assert 90 * all_in == pytest.approx(68, abs=4)
    assert 90 * all_in / sat["life_yr"] == pytest.approx(13.5, abs=1)


def test_higher_shells_cost_more_per_satellite():
    per_sat = {h: cm.tco(_design(h))["tco_meur"] for h in (550, 800, 1200)}
    assert per_sat[550] < per_sat[800] < per_sat[1200]   # deorbit propellant, then shorter radiation-limited life


def test_optical_grid_costs_more_than_rf_inplane():
    assert cm.tco(_design(isl=cfg.ShellIsl()))["tco_meur"] > cm.tco(_design())["tco_meur"]


def test_terminal_count_follows_layout():
    d = cfg.Design("t", (cfg.Shell(12, 20, 550, 87, "star", 1, cfg.ShellIsl("rf", "optical", 2, 4)),))
    t = cm.terminals(d)[0]
    assert t["rf"] == 2 and t["optical"] == pytest.approx(2 * 5 / 20)


def test_overloaded_satellite_fits_no_bus():
    d = _design()
    big = dict(rf=0, optical=40)
    assert cm.satellite(d.shells[0], big, cm.CostParams())["bus"] is None


def test_hohmann_is_symmetric_and_zero_in_place():
    assert cm.hohmann_dv_kms(525, 525) == 0
    assert cm.hohmann_dv_kms(525, 1200) == pytest.approx(cm.hohmann_dv_kms(1200, 525))
