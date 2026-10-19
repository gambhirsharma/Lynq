"""Lifecycle cost of a constellation design: satellite mass and bus, propellant, lifetime, launch, planes, ops.

Every number is a parametric assumption in CostParams, calibrated to one point: the proposal's 90 satellites
at 550-600 km, 12U-16U, RF in-plane ISL, ~EUR 0.75 M all-in each (~EUR 68 M capex, ~EUR 13.5 M/yr replenishment,
01-research/08-OUR-PROPOSAL.md). The ranking of designs is more trustworthy than the absolute euros.

    TCO = sum over shells of  N x c_sat x builds          build + replacements over the horizon
                            + N x m_sat x launch_per_kg x builds
                            + planes x c_plane x builds    one orbital transfer vehicle (OTV) per plane per campaign
        + ground segment + ops x years (+ an ITU filing if any RF crosslink is flown)
    builds = ceil(horizon / lifetime(h))
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace

from globalnet import config as cfg

G0 = 9.80665e-3   # km/s^2


@dataclass(frozen=True)
class Bus:
    name: str
    max_mass_kg: float     # wet mass the structure and the rideshare slot allow
    power_w: float         # orbit-average power for payload + terminals
    dry_kg: float          # bus alone (structure, EPS, ADCS, OBC, TT&C)
    cost_meur: float


BUSES = (
    Bus("12U", 24.0, 100.0, 14.0, 0.30),
    Bus("16U", 32.0, 150.0, 18.0, 0.42),
    Bus("ESPA-150", 150.0, 600.0, 60.0, 1.20),
)


@dataclass(frozen=True)
class CostParams:
    horizon_yr: float = 10.0
    # Payload: narrowband regenerative gNB + S-band service antenna
    payload_kg: float = 4.0
    payload_w: float = 40.0
    payload_meur: float = 0.15
    # Electric propulsion: fixed system + propellant from the rocket equation
    prop_system_kg: float = 1.5
    prop_system_meur: float = 0.06
    isp_s: float = 1000.0
    life_yr: float = 5.0                  # design life 500-900 km
    radiation_life_loss_per_100km: float = 0.33   # above 900 km (inner Van Allen belt edge)
    rideshare_km: float = 525.0           # where a Transporter-class rideshare drops satellites
    deorbit_free_km: float = 600.0        # below this, natural decay meets the 5-year rule
    deorbit_perigee_km: float = 300.0
    # Launch and deployment
    launch_meur_per_kg: float = 0.006     # rideshare ~EUR 6k/kg
    plane_meur: float = 1.5               # one OTV per orbital plane per launch campaign
    otv_capacity_kg: float = 300.0
    # Terminals (scales the IslTech table, for sensitivity runs)
    rf_terminal_scale: float = 1.0
    optical_terminal_scale: float = 1.0
    # Ground and operations
    gateways: int = len(cfg.GATEWAYS)
    gateway_meur: float = 0.3
    gateway_ops_meur_yr: float = 0.1
    ops_fixed_meur_yr: float = 2.0
    ops_per_sat_meur_yr: float = 0.02     # conjunction screening, manoeuvres, licences
    itu_rf_isl_meur: float = 1.0          # coordination of an RF crosslink band; optical needs none

    def scaled(self, **kw) -> "CostParams":
        return replace(self, **kw)


def _v_circ(h_km: float) -> float:
    return math.sqrt(cfg.MU_KM3_S2 / (cfg.RE_KM + h_km))


def hohmann_dv_kms(h1_km: float, h2_km: float) -> float:
    r1, r2 = cfg.RE_KM + h1_km, cfg.RE_KM + h2_km
    a = (r1 + r2) / 2
    v1, v2 = _v_circ(h1_km), _v_circ(h2_km)
    return abs(math.sqrt(cfg.MU_KM3_S2 * (2 / r1 - 1 / a)) - v1) + abs(v2 - math.sqrt(cfg.MU_KM3_S2 * (2 / r2 - 1 / a)))


def deorbit_dv_kms(h_km: float, p: CostParams) -> float:
    """One burn to lower the perigee to deorbit_perigee_km; zero where natural decay is fast enough."""
    if h_km <= p.deorbit_free_km:
        return 0.0
    r, rp = cfg.RE_KM + h_km, cfg.RE_KM + p.deorbit_perigee_km
    a = (r + rp) / 2
    return _v_circ(h_km) - math.sqrt(cfg.MU_KM3_S2 * (2 / r - 1 / a))


def drag_dv_kms_per_yr(h_km: float) -> float:
    """Station-keeping against drag for a smallsat at mean solar activity: ~25 m/s/yr at 450 km, e-folding 60 km."""
    return 0.025 * math.exp(-(h_km - 450.0) / 60.0)


def lifetime_yr(h_km: float, p: CostParams) -> float:
    return p.life_yr - max(0.0, h_km - 900.0) / 100.0 * p.radiation_life_loss_per_100km


def terminals(design: cfg.Design) -> list[dict]:
    """Crosslink terminals carried per satellite, per shell: {'rf': n, 'optical': n} averaged over the shell."""
    out = []
    for s in design.shells:
        isl = design.shell_isl(s)
        t = {"rf": 0.0, "optical": 0.0}
        if isl.tech_in != "none" and s.sats_per_plane > 1:
            t[isl.tech_in] += 2
        if isl.tech_x != "none" and isl.cross > 0 and s.planes > 1:
            carriers = math.ceil(s.sats_per_plane / isl.relay_every) / s.sats_per_plane
            t[isl.tech_x] += isl.cross * carriers
        out.append(t)
    if design.inter_shell and len(design.shells) > 1:
        # each link needs a terminal at both ends: the smaller shell's satellites each make one link per pair
        for a in range(len(design.shells)):
            for b in range(a + 1, len(design.shells)):
                small = min(design.shells[a].size, design.shells[b].size)
                for k in (a, b):
                    out[k]["optical"] += small / design.shells[k].size
    return out


def satellite(shell: cfg.Shell, term: dict, p: CostParams) -> dict:
    """Mass, bus and unit cost of one satellite of a shell. bus=None when nothing fits."""
    rf, op = cfg.ISL_TECH["rf"], cfg.ISL_TECH["optical"]
    life = lifetime_yr(shell.altitude_km, p)
    dv = (hohmann_dv_kms(p.rideshare_km, shell.altitude_km) + drag_dv_kms_per_yr(shell.altitude_km) * life
          + deorbit_dv_kms(shell.altitude_km, p))
    kit_kg = p.payload_kg + term["rf"] * rf.mass_kg + term["optical"] * op.mass_kg + p.prop_system_kg
    power = p.payload_w + term["rf"] * rf.power_w + term["optical"] * op.power_w
    for bus in BUSES:
        dry = bus.dry_kg + kit_kg
        wet = dry * math.exp(dv / (p.isp_s * G0))
        if wet <= bus.max_mass_kg and power <= bus.power_w:
            break
    else:
        return dict(bus=None, mass_kg=math.nan, dv_ms=dv * 1e3, power_w=power, unit_meur=math.nan, life_yr=life)
    unit = (bus.cost_meur + p.payload_meur + p.prop_system_meur
            + term["rf"] * rf.cost_meur * p.rf_terminal_scale + term["optical"] * op.cost_meur * p.optical_terminal_scale)
    return dict(bus=bus.name, mass_kg=wet, dv_ms=dv * 1e3, power_w=power, unit_meur=unit, life_yr=life)


def tco(design: cfg.Design, p: CostParams = CostParams()) -> dict:
    """Total cost of ownership over the horizon, in M EUR, with a breakdown. feasible=False if a satellite fits no bus."""
    out = dict(capex_meur=0.0, build_meur=0.0, launch_meur=0.0, planes_meur=0.0, buses="")
    feasible, buses = True, []
    for shell, term in zip(design.shells, terminals(design)):
        sat = satellite(shell, term, p)
        if sat["bus"] is None:
            feasible = False
            buses.append("none")
            continue
        builds = math.ceil(p.horizon_yr / sat["life_yr"] - 1e-9)
        N = shell.size
        otvs_per_plane = math.ceil(shell.sats_per_plane * sat["mass_kg"] / p.otv_capacity_kg)
        build, launch = N * sat["unit_meur"], N * sat["mass_kg"] * p.launch_meur_per_kg
        planes = shell.planes * otvs_per_plane * p.plane_meur
        out["capex_meur"] += build + launch + planes
        out["build_meur"] += build * builds
        out["launch_meur"] += launch * builds
        out["planes_meur"] += planes * builds
        buses.append(f"{sat['bus']}/{sat['mass_kg']:.0f}kg/{sat['life_yr']:g}y")
    rf_used = any(t["rf"] > 0 for t in terminals(design))
    ground = p.gateways * (p.gateway_meur + p.gateway_ops_meur_yr * p.horizon_yr)
    ops = (p.ops_fixed_meur_yr + p.ops_per_sat_meur_yr * design.size) * p.horizon_yr + (p.itu_rf_isl_meur if rf_used else 0)
    out.update(ground_meur=ground, ops_meur=ops, buses=" + ".join(buses), feasible=feasible)
    out["tco_meur"] = out["build_meur"] + out["launch_meur"] + out["planes_meur"] + ground + ops if feasible else math.inf
    return out
