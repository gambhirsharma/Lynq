"""Assumptions for the global study: physics, link budget, delays, worldwide ground segment, shells, presets.

Same physics and link budget as 04-simulation/ntnpulse/config.py. What changes is the goal: every point on
Earth (oceans and poles included) must be served, with the lowest end-to-end latency, and the number of
satellites is an output of the study, not a fixed input. Change numbers here, not in the model.
"""
from __future__ import annotations

from dataclasses import dataclass

# --- Physics -----------------------------------------------------------------
RE_KM = 6371.0                # mean Earth radius
MU_KM3_S2 = 398600.4418       # Earth gravitational parameter
C_KM_S = 299_792.458          # speed of light
OMEGA_E = 7.2921159e-5        # Earth rotation rate, rad/s
FIBRE_KM_S = C_KM_S / 1.47    # light in fibre
FIBRE_ROUTE_FACTOR = 1.5      # real fibre routes vs great circle
K_BOLTZMANN_DBW = -228.6      # dBW/K/Hz
GRAZING_ALT_KM = 80.0         # ISL must clear the atmosphere by this much

# --- Service link (NB-IoT NTN, same budget as the North Sea twin) -------------
SERVICE_FREQ_MHZ = 2000.0
SERVICE_BW_HZ = 180e3
TERMINAL_EIRP_DBW = -7.0
SAT_GT_DBK = -5.0
LINK_LOSSES_DB = 3.0
IMPL_EFFICIENCY = 0.5
MIN_SNR_DB = -10.0
MAX_USER_RATE_BPS = 120e3
ALARM_BYTES = 200             # message used for the end-to-end latency figure

TERMINAL_MIN_EL_DEG = 10.0
GATEWAY_MIN_EL_DEG = 5.0

# --- ISL ---------------------------------------------------------------------
# Global low latency needs a full mesh, so every satellite carries 4 optical terminals ("+Grid"):
# fore/aft in its plane and left/right to the nearest satellite in each adjacent plane.
LASER_ISL_MAX_KM = 6000.0
ISL_MODES = ("grid", "inplane", "none")


@dataclass(frozen=True)
class IslTech:
    """One crosslink technology. Starting assumptions for 07-constellation-optimization: check against data sheets.

    Optical: fixed rate up to max_km. RF: rate from a link budget (Shannon x efficiency), the link is down where
    it falls below min_rate_bps, so RF range comes out of the budget (~3,000 km with these numbers).
    """
    name: str
    max_km: float
    rate_bps: float = 0.0          # optical: fixed rate
    acquisition_s: float = 0.0     # time to lock onto a new partner (optical pointing, acquisition and tracking)
    freq_ghz: float = 0.0          # RF budget
    bw_hz: float = 0.0
    eirp_dbw: float = 0.0
    gt_dbk: float = 0.0
    losses_db: float = 0.0
    min_rate_bps: float = 0.0
    cost_meur: float = 0.0         # per terminal, qualified, incl. integration
    mass_kg: float = 0.0
    power_w: float = 0.0


ISL_TECH = {
    # Ka-band smallsat crosslink: ~10 W into a small array (20 dBW EIRP), 5 MHz, 1 Mbps floor.
    "rf": IslTech("rf", max_km=5000.0, freq_ghz=23.0, bw_hz=5e6, eirp_dbw=20.0, gt_dbk=5.0, losses_db=2.5,
                  min_rate_bps=1e6, cost_meur=0.05, mass_kg=1.5, power_w=15.0),
    # Low-SWaP European laser terminal (Tesat SCOT20 / Mynaric CONDOR class). Range kept at the 05 study's 6,000 km.
    "optical": IslTech("optical", max_km=LASER_ISL_MAX_KM, rate_bps=100e6, acquisition_s=30.0,
                       cost_meur=0.20, mass_kg=2.0, power_w=25.0),
}
ISL_TECHS = ("none", "rf", "optical")


@dataclass(frozen=True)
class ShellIsl:
    """ISL layout of one shell.

    tech_in: fore/aft links in the plane. tech_x: links to adjacent planes. cross: cross-plane terminals per
    carrying satellite (2 = +Grid left/right, 1 = brick: alternate satellites link one side). relay_every:
    only every n-th satellite of a plane carries cross-plane terminals (a relay subset). polar_off_deg:
    cross-plane links drop when both ends are above this latitude.
    """
    tech_in: str = "optical"
    tech_x: str = "optical"
    cross: int = 2
    relay_every: int = 1
    polar_off_deg: float = 90.0

    @classmethod
    def from_mode(cls, mode: str) -> "ShellIsl":
        return {"grid": cls(), "inplane": cls(tech_x="none", cross=0),
                "none": cls(tech_in="none", tech_x="none", cross=0)}[mode]

    @property
    def label(self) -> str:
        x = f"{self.tech_x}x{self.cross}" + (f"/{self.relay_every}" if self.relay_every > 1 else "")
        off = f"/off{self.polar_off_deg:g}" if self.polar_off_deg < 90 else ""
        return f"in:{self.tech_in} x:{x if self.cross else 'none'}{off}"

# --- Processing delays (seconds) --------------------------------------------
RACH_ACCESS_S = 0.020         # NTN random access + grant
GNB_PROC_S = 0.005            # onboard gNB
ISL_HOP_PROC_S = 0.002        # per relay hop
GROUND_PROC_S = 0.010         # gateway + 5G Core UPF

# --- Latency tiers ------------------------------------------------------------
TIERS_S = (0.075, 0.100, 0.150)   # ~50 ms is fixed access + processing; 150 ms is the proposal's continuous tier


# --- Ground segment ----------------------------------------------------------
@dataclass(frozen=True)
class Site:
    name: str
    lat: float
    lon: float
    backhaul_s: float = 0.0   # extra one-way delay when the site has no fibre (GEO backhaul ~0.28 s)


# Internet exchange / cloud regions. Traffic counts as delivered when it reaches the one nearest the gateway.
POPS = (
    Site("Frankfurt", 50.11, 8.68), Site("London", 51.51, -0.13), Site("Virginia", 38.95, -77.45),
    Site("Oregon", 45.60, -121.18), Site("Sao Paulo", -23.55, -46.63), Site("Santiago", -33.45, -70.67),
    Site("Johannesburg", -26.20, 28.05), Site("Bahrain", 26.07, 50.56), Site("Mumbai", 19.08, 72.88),
    Site("Singapore", 1.35, 103.82), Site("Tokyo", 35.68, 139.69), Site("Sydney", -33.87, 151.21),
)

# Ground stations at existing teleport / TT&C sites, spread so ISL routes stay short everywhere.
GATEWAYS = (
    Site("Betzdorf", 49.69, 6.35), Site("Svalbard", 78.23, 15.41), Site("Kiruna", 67.86, 20.96),
    Site("Reykjavik", 64.15, -21.94), Site("Fairbanks", 64.84, -147.72), Site("Inuvik", 68.36, -133.72),
    Site("Oregon", 45.60, -121.18), Site("Virginia", 38.95, -77.45), Site("Hawaii", 19.01, -155.66),
    Site("Azores", 37.74, -25.68), Site("Canaries", 27.76, -15.63), Site("Ascension", -7.95, -14.36),
    Site("Sao Paulo", -23.55, -46.63), Site("Punta Arenas", -53.16, -70.91), Site("Hartebeesthoek", -25.89, 27.69),
    Site("Nairobi", -1.29, 36.82), Site("Dubai", 25.20, 55.27), Site("Mauritius", -20.16, 57.50),
    Site("Mumbai", 19.08, 72.88), Site("Singapore", 1.35, 103.82), Site("Tokyo", 35.68, 139.69),
    Site("Guam", 13.44, 144.79), Site("Perth", -29.05, 115.35), Site("Sydney", -33.87, 151.21),
    Site("Auckland", -36.85, 174.76), Site("Tahiti", -17.53, -149.57),
    Site("Troll", -72.01, 2.53, backhaul_s=0.28), Site("McMurdo", -77.85, 166.67, backhaul_s=0.28),
)


# --- Constellations ------------------------------------------------------------
PATTERNS = {"star": 180.0, "delta": 360.0}   # RAAN spread


@dataclass(frozen=True)
class Shell:
    planes: int
    sats_per_plane: int
    altitude_km: float = 550.0
    inclination_deg: float = 53.0
    pattern: str = "delta"
    phasing: int = 1
    isl: ShellIsl | None = None    # None: follow Design.isl

    @property
    def size(self) -> int:
        return self.planes * self.sats_per_plane

    @property
    def label(self) -> str:
        return f"{self.planes}x{self.sats_per_plane}@{self.altitude_km:g}km/{self.inclination_deg:g}deg/{self.pattern}"

    @classmethod
    def parse(cls, s: str) -> "Shell":
        """'PxS@ALT/INC/PATTERN', e.g. '6x20@560/97.6/star'."""
        layout, rest = s.split("@")
        p, n = layout.lower().split("x")
        alt, inc, pat = rest.replace("km", "").replace("deg", "").split("/")
        return cls(int(p), int(n), float(alt), float(inc), pat)


@dataclass(frozen=True)
class Design:
    name: str
    shells: tuple[Shell, ...]
    isl: str = "grid"
    inter_shell: bool = False      # optical links from each satellite of the smaller shell to the nearest in the other
    acquisition: bool = False      # optical links are down for the first step after they change partner

    @property
    def size(self) -> int:
        return sum(s.size for s in self.shells)

    def shell_isl(self, s: Shell) -> ShellIsl:
        return s.isl or ShellIsl.from_mode(self.isl)

    @property
    def label(self) -> str:
        return " + ".join(s.label for s in self.shells)


PRESETS = {
    # Today's plan, for reference: built for the North Sea, not the globe.
    "planned-30": Design("planned-30", (Shell(3, 10, 550, 97.6, "star"),)),
    # Iridium-style polar star: the classic minimum for global coverage, at our 10 deg mask and 780 km.
    "polar-66": Design("polar-66", (Shell(6, 11, 780, 86.4, "star"),)),
    "polar-72": Design("polar-72", (Shell(6, 12, 780, 86.4, "star"),)),
    # Higher shell: wider footprints, fewer satellites, longer slant ranges.
    "polar-1200-120": Design("polar-1200-120", (Shell(8, 15, 1200, 87.9, "star"),)),
    # Low polar shell at our current altitude, sized to close the ring and the cross-plane mesh.
    "polar-550-240": Design("polar-550-240", (Shell(12, 20, 550, 87.0, "star"),)),
    # Hybrid: inclined delta for the populated mid-latitudes + a polar shell for the poles.
    "hybrid-550-360": Design("hybrid-550-360", (Shell(15, 16, 550, 53.0, "delta"), Shell(6, 20, 560, 97.6, "star"))),
}
