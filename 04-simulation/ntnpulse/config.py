"""Physical constants, design-point assumptions and scenario definitions.

Every number here is an assumption from the research pack (01-research/04-TECHNICAL-deep-dive.md)
or the proposal (03-proposal/current/final.md). Change them here, not in the engine.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace

# --- Physics -----------------------------------------------------------------
RE_KM = 6371.0                # mean Earth radius
MU_KM3_S2 = 398600.4418       # Earth gravitational parameter
C_KM_S = 299_792.458          # speed of light
OMEGA_E = 7.2921159e-5        # Earth rotation rate, rad/s
FIBRE_KM_S = C_KM_S / 1.47    # light in fibre
FIBRE_ROUTE_FACTOR = 1.5      # real fibre routes vs great circle
K_BOLTZMANN_DBW = -228.6      # dBW/K/Hz
GRAZING_ALT_KM = 80.0         # ISL must clear the atmosphere by this much

# --- Link assumptions --------------------------------------------------------
SERVICE_FREQ_MHZ = 2000.0     # S-band MSS (NB-IoT NTN, band n256)
SERVICE_BW_HZ = 180e3         # one NB-IoT carrier
TERMINAL_EIRP_DBW = -7.0      # 23 dBm IoT terminal
SAT_GT_DBK = -5.0             # satellite receive G/T
LINK_LOSSES_DB = 3.0          # polarisation, atmosphere, pointing
IMPL_EFFICIENCY = 0.5         # fraction of Shannon actually achieved
MIN_SNR_DB = -10.0            # below this even NB-IoT repetitions fail
MAX_USER_RATE_BPS = 120e3     # NB-IoT NTN per-user ceiling

SAT_SERVICE_CAPACITY_BPS = 1.0e6   # aggregate uplink a satellite can schedule
FEEDER_CAPACITY_BPS = 20e6         # satellite -> gateway (X/Ka band)
RF_ISL_CAPACITY_BPS = 10e6         # intra-plane RF ISL
OPTICAL_ISL_CAPACITY_BPS = 1e9     # cross-plane optical ISL
RF_ISL_MAX_KM = 5000.0
OPTICAL_ISL_MAX_KM = 6000.0

# --- Processing delays (seconds) --------------------------------------------
RACH_ACCESS_S = 0.020         # NTN random access + grant (pre-compensated TA)
GNB_PROC_S = 0.005            # onboard gNB L1/L2/L3
ISL_HOP_PROC_S = 0.002        # per relay hop
GROUND_PROC_S = 0.010         # gateway + 5G Core UPF
BENT_PIPE_GNB_PROC_S = 0.010  # ground gNB for transparent payload
CLOUD_SITE = (50.11, 8.68)    # Frankfurt cloud region, end of every flow

TERMINAL_MIN_EL_DEG = 10.0
GATEWAY_MIN_EL_DEG = 5.0
ONBOARD_BUFFER_BYTES = 50e6

# --- Traffic classes (from the proposal: critical / regular / metadata) ------
@dataclass(frozen=True)
class TrafficClass:
    name: str
    priority: int             # lower = served first
    mean_interval_s: float    # per terminal
    size_bytes: tuple[int, int]
    ttl_s: float              # dropped if not delivered by then
    target_s: float           # service-tier deadline


TRAFFIC_CLASSES = (
    TrafficClass("critical", 0, 6 * 3600, (100, 400), 6 * 3600, 0.150),
    TrafficClass("metadata", 1, 30 * 60, (48, 96), 6 * 3600, 90 * 60),
    TrafficClass("regular", 2, 15 * 60, (1_000, 100_000), 12 * 3600, 90 * 60),
)
MESH_TARGET_S = 0.250         # mesh-relayed tier
SNF_TARGET_S = 90 * 60        # store-and-forward tier

# --- Ground segment ----------------------------------------------------------
@dataclass(frozen=True)
class Gateway:
    name: str
    country: str
    lat: float
    lon: float


GATEWAYS = (
    Gateway("Aberdeen", "UK", 57.15, -2.09),
    Gateway("Stavanger", "NO", 58.97, 5.73),
    Gateway("Svalbard", "NO", 78.23, 15.41),
    Gateway("Esbjerg", "DK", 55.47, 8.45),
    Gateway("Den Helder", "NL", 52.96, 4.76),
    Gateway("Bremen", "DE", 53.08, 8.80),
    Gateway("Betzdorf", "LU", 49.69, 6.35),
)

# Data-residency rule per terminal jurisdiction: which gateway countries may receive it.
EEA = frozenset({"NO", "DK", "NL", "DE", "LU"})
JURISDICTION_RULES = {
    "UK": frozenset({"UK"}),
    "NO": frozenset({"NO"}),
    "EEA": EEA,
    "INTL": frozenset({"UK"}) | EEA,   # international waters: no landing restriction
}

# Offshore sectors (lat_min, lat_max, lon_min, lon_max, jurisdiction, share of terminals)
SECTORS = (
    ("UK", 53.5, 61.0, -1.5, 2.0, "UK", 0.30),
    ("NO", 56.5, 61.0, 2.5, 5.0, "NO", 0.30),
    ("DK", 55.3, 57.5, 4.0, 7.5, "EEA", 0.15),
    ("NL/DE", 53.3, 55.3, 3.0, 7.5, "EEA", 0.15),
    ("Atlantic", 45.0, 55.0, -35.0, -20.0, "INTL", 0.10),
)

# --- Scenarios ---------------------------------------------------------------
MODES = ("bent_pipe", "regen", "regen_isl")
MODE_LABELS = {
    "bent_pipe": "Bent-pipe",
    "regen": "Regenerative, no ISL",
    "regen_isl": "Regenerative + ISL",
}


@dataclass(frozen=True)
class Constellation:
    name: str
    planes: int
    sats_per_plane: int
    altitude_km: float = 550.0
    inclination_deg: float = 97.6     # sun-synchronous, like OQ's rideshares
    raan_spread_deg: float = 180.0    # Walker star
    phasing: int = 1
    optical_every: int = 2            # every Nth satellite carries a cross-plane terminal
    cross_isl: str = "optical"        # cross-plane link technology: "optical" or "rf"
    link_seam: bool = True            # link the last plane back to the first (counter-rotating in a star)

    @property
    def size(self) -> int:
        return self.planes * self.sats_per_plane


CONSTELLATIONS = {
    # Recommended global design, 07-constellation-optimization/DESIGN-7x16.md:
    # 7x16 @ 700 km / 87 deg / Walker star / F0, RF crosslinks in-plane and to both neighbouring planes.
    112: Constellation("design-7x16", planes=7, sats_per_plane=16, altitude_km=700.0, inclination_deg=87.0,
                       phasing=0, optical_every=1, cross_isl="rf", link_seam=False),
    12: Constellation("today-12", planes=2, sats_per_plane=6),
    30: Constellation("planned-30", planes=3, sats_per_plane=10),
    60: Constellation("scale-60", planes=6, sats_per_plane=10),
}


@dataclass(frozen=True)
class Scenario:
    constellation: Constellation = CONSTELLATIONS[112]
    mode: str = "regen_isl"
    blocked_gateways: frozenset[str] = field(default_factory=frozenset)
    load: float = 1.0
    terminals: int = 300
    duration_s: float = 24 * 3600
    step_s: float = 10.0
    seed: int = 7

    def with_(self, **kw) -> "Scenario":
        return replace(self, **kw)

    @property
    def label(self) -> str:
        gw = "all GW" if not self.blocked_gateways else "-" + ",".join(sorted(self.blocked_gateways))
        return f"{self.constellation.size} sats | {MODE_LABELS[self.mode]} | {gw} | load x{self.load:g}"


# --- Fleet orchestration (KubeEdge-style software rollout) ----------------------
OTA_FEEDER_MBPS = 5.0         # share of the 20 Mbps forward feeder given to software updates
OTA_ISL_SHARE = 0.5           # share of an RF ISL a peer may use to pass the image on
K8S_GRACE_S = 40.0            # node-monitor-grace-period: missed heartbeats before a node is NotReady
K8S_EVICTION_S = 300.0        # default not-ready toleration before pods are evicted
STRATEGIES = ("waves", "all")
STRATEGY_LABELS = {"waves": "Canary, then waves", "all": "All at once"}


@dataclass(frozen=True)
class FleetScenario:
    """One over-the-air rollout of a new onboard workload (e.g. a gNB container) to the whole fleet."""
    constellation: Constellation = CONSTELLATIONS[30]
    isl: bool = True                  # control traffic and images may relay over the ISL mesh
    peer_sharing: bool = True         # satellites that have the image pass it to neighbours over ISL
    blocked_gateways: frozenset[str] = field(default_factory=frozenset)
    image_mb: float = 100.0           # layer delta to push, not the full image
    ota_mbps: float = OTA_FEEDER_MBPS
    strategy: str = "waves"
    wave_size: int = 3                # maxUnavailable: satellites restarting at the same time
    canary_soak_min: float = 30.0     # watch the canary this long before releasing the rest
    restart_s: float = 90.0           # gNB down while the new container starts
    avoid_basin: bool = True          # restart only while not serving the North Sea
    prestage: bool = True             # pre-pull the image everywhere before release (ImagePrePullJob)
    grace_s: float = K8S_GRACE_S
    eviction_s: float = K8S_EVICTION_S
    duration_s: float = 24 * 3600
    step_s: float = 10.0

    def with_(self, **kw) -> "FleetScenario":
        return replace(self, **kw)
