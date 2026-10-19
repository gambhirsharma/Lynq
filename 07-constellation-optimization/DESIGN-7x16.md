# Lynq 7-plane constellation: 112 satellites at 700 km

**Recommended global design:** `7x16 @ 700 km / 87° / Walker star / F0`, Ka-band radio crosslinks in-plane and
to both neighbouring planes (`[in:rf x:rfx2]`).

It is the cheapest design found that covers every point on Earth at every minute of a 24-hour day and delivers
99% of alarms within 100 ms.

Every number below carries a source tag so it can be checked:

| Tag | Where to verify |
|---|---|
| **[S]** | `.venv/bin/python design_detail.py 16` (this folder, ~2 min). Re-simulates this design with `globalnet/` and `costmodel.py`. |
| **[R]** | `results/report.md`, from `solve.py` (NSGA-II search over 3,064 designs, picks confirmed at 24 h / 60 s / 2,000 points). |
| **[A]** | An input assumption in `globalnet/config.py` or `costmodel.py`. Change it there and re-run to test sensitivity. |
| **[E]** | Our engineering estimate or suggestion, not computed by the model. |

## Headline figures

| Figure | Value | Source |
|---|---:|---|
| Satellites | 112 (7 planes × 16) | [S] |
| Coverage | 100% of Earth, every minute, longest gap 0 min | [S] |
| Typical alarm latency (p50) | 72 ms | [S] |
| Worst 1% of alarms (p99) | 98 ms | [S] |
| Build and launch (capex) | €134.2M | [S] |
| 10-year total cost (TCO) | €348.2M | [S] |

## 1. Orbit

| Parameter | Value | Source |
|---|---|---|
| Altitude | 700 km | design input |
| Inclination | 87° (near-polar) | design input |
| Pattern | Walker star, planes spread over 180° | design input |
| Planes | 7, every 25.7° | [S] |
| Satellites per plane | 16, every 22.5° along the orbit | [S] |
| Phasing | F = 0, same slot positions in every plane | design input |
| Orbital period | 98.6 min | [S] |
| Orbital speed | 7.51 km/s | [S] |
| Coverage radius per satellite | 1,942 km at 10° minimum elevation | [S], mask [A] |
| Longest pass over a terminal | ~9.6 min (overhead pass, Earth rotation ignored) | [S] |
| Satellites in view, average / minimum | 2.58 / 1 | [S] |

**Why this shape works:**
- **Global coverage:** polar planes all cross near the poles, so the poles get the most satellites and the equator gets the fewest.
- **Along the track:** 16 satellites per plane keep footprints overlapping.
- **Between tracks:** 7 planes close the gaps at the equator.

**The seam:** with planes spread over 180°, one side of the globe has plane 7 heading south next to plane 1
heading north. Across that seam the relative speed is too high to hold a crosslink, so the model leaves it
unlinked (`globalnet/model.py`, `isl_edges`).

## 2. Crosslinks

Each satellite carries 4 radio terminals:
- **Fore and aft:** to the satellites ahead and behind in the same plane.
- **Left and right:** to the nearest satellite in each neighbouring plane.

| Parameter | Value | Source |
|---|---|---|
| Technology | Ka-band radio, 23 GHz, 5 MHz bandwidth, 20 dBW EIRP, G/T 5 dB/K | [A] `ISL_TECH["rf"]` |
| Minimum usable rate | 1 Mbps (link counted down below this) | [A] |
| Terminal cost / mass / power | €0.05M / 1.5 kg / 15 W each | [A] |
| In-plane distance | 2,759 km, constant | [S] |
| Cross-plane distance | 165 / 1,800 / 2,947 km (min / median / max) | [S] |
| Data rate per link | 1.00–1.12 Mbps | [S] |
| Links up, average | 186 of 208 possible (11% down) | [S] |
| Delay per hop | light time + 2 ms processing + 1.6 ms to send 200 B at 1 Mbps | [A] `ISL_HOP_PROC_S`, `ALARM_BYTES` |

**How a message travels:**
- It goes down at the nearest ground station the satellite can see.
- Over open ocean there is none, so it hops along the crosslinks until it reaches a satellite above a gateway.
- In-plane links carry it north and south; cross-plane links carry it east and west.

**Why cross-plane links matter:** they buy latency, not coverage. Without them, the cheapest full-coverage design
is 96 satellites at 800 km with in-plane radio only, at a p99 of 110 ms [R].

**Why radio, not lasers:**
- **Cost:** in the search, radio wins at every laser terminal price tested, down to €0.02M per terminal [R].
- **Platform:** laser terminals are heavier (2 kg) and draw more power (25 W) [A], which pushes the satellite onto a bigger platform.
- **Acquisition:** lasers also need ~30 s to lock onto each new partner [A].
- **Data rate:** alarms are 200 B, so 1 Mbps is plenty.

### Risk: the radio links have almost no margin

| Link | Distance | Margin above 1 Mbps floor | Source |
|---|---:|---:|---|
| In-plane (7×16) | 2,759 km | 0.58 dB | [S] |
| Widest cross-plane, over the equator | 2,947 km | 0.00 dB | [S] |
| In-plane if 7×15 instead | 2,940 km | 0.02 dB | `design_detail.py 15` |

With the assumed budget, the radio range ends at about 2,950 km. About 11% of links are down at any moment,
mostly the widest cross-plane ones.

**Recommendation [E]:** design for about +3 dB per link, through a larger antenna or more transmit power. Re-run
with `ISL_TECH["rf"].eirp_dbw` raised by 3 to check the effect. This margin is also the main reason to prefer
16 satellites per plane over 15.

## 3. Satellite

| Parameter | Value | Source |
|---|---|---|
| Platform | 16U (limits: 32 kg, 150 W) | [S], bus table [A] |
| Wet mass | 30.1 kg | [S] |
| Power, orbit average | 100 W = 40 W payload + 4 × 15 W crosslinks | [S] |
| Payload | NB-IoT NTN gNB on board, S-band service antenna | [A] |
| Propulsion | Electric, Isp 1,000 s | [A] |
| Δv budget | 207 m/s: raise 525 km → 700 km, 5 years drag make-up, deorbit | [S] |
| Design life | 5 years | [A] |
| Unit cost | €0.83M | [S] |

Unit cost breakdown [S]:

| Item | € M |
|---|---:|
| 16U platform | 0.42 |
| gNB payload | 0.15 |
| 4 radio crosslink terminals | 0.20 |
| Electric propulsion | 0.06 |
| **Total** | **0.83** |

Above 600 km natural decay does not meet the 5-year deorbit rule, so a deorbit burn is budgeted [A]
(`deorbit_free_km`).

## 4. Performance

**What latency includes:** the one-way time for a 200-byte alarm from the terminal to the internet:
- random access, 20 ms
- uplink
- on-board gNB, 5 ms
- crosslink hops
- downlink
- gateway and core, 10 ms
- fibre to the nearest of 12 internet exchanges

The processing delays are assumptions [A]. The simulation runs 24 h at 60 s steps over 2,000 equal-area points.

| Measure | Value | Meaning | Source |
|---|---:|---|---|
| Coverage | 100% | Every point at every step | [S] |
| Longest gap | 0 min | | [S] |
| Median latency (p50) | 71.9 ms | A typical alarm | [S] |
| p95 | 91.0 ms | 1 in 20 alarms is slower | [S] |
| p99 | 98.3 ms | 1 in 100 alarms is slower | [S] |
| Slowest alarm of the day | 121.9 ms | Single worst sample | [S] |
| Worst place on Earth, p95 | 105.1 ms | Worst-served location on its bad moments | [S] |
| Alarms under 75 / 100 ms | 61.0% / 99.4% | | [S] |

### By latitude [S]

| Band | Coverage | Max gap | p50 ms | p95 ms |
|---|---:|---:|---:|---:|
| +75° to +90° | 100% | 0 | 72.2 | 79.1 |
| +60° to +75° | 100% | 0 | 69.8 | 79.0 |
| +45° to +60° | 100% | 0 | 66.0 | 77.5 |
| +30° to +45° | 100% | 0 | 65.8 | 78.5 |
| +15° to +30° | 100% | 0 | 70.7 | 85.8 |
| 0° to +15° | 100% | 0 | 75.1 | 92.5 |
| −15° to 0° | 100% | 0 | 77.0 | 95.6 |
| −30° to −15° | 100% | 0 | 72.6 | 95.4 |
| −45° to −30° | 100% | 0 | 71.5 | 92.0 |
| −60° to −45° | 100% | 0 | 75.3 | 89.6 |
| −75° to −60° | 100% | 0 | 79.3 | 90.3 |
| −90° to −75° | 100% | 0 | 82.6 | 88.5 |

**Fastest: Europe and North America** (30–60°N), because most gateways and internet exchanges are there.

**Slowest: near the South Pole.** The only ground stations in view there are Troll and McMurdo, which have a
280 ms geostationary backhaul [A]. So traffic from there hops north to Punta Arenas, South Africa or Australia
first. That routing is our reading [E]; the model picks the fastest path automatically.

## 5. Cost

Costs come from a parametric model calibrated to the proposal's €0.75M per satellite all-in
(`costmodel.py` docstring). Trust the ranking of designs more than the absolute euros.

### Initial deployment (capex) [S]

| Item | € M |
|---|---:|
| 112 satellites × €0.83M | 93.0 |
| Rideshare launch, 112 × 30.1 kg × €6,000/kg | 20.2 |
| Orbit transfer vehicles, 7 planes × 2 × €1.5M | 21.0 |
| **Total** | **134.2** |

Each plane needs 2 transfer vehicles because 16 × 30.1 kg = 482 kg exceeds one vehicle's 300 kg [A].

### 10-year total cost of ownership [S]

| Item | € M |
|---|---:|
| Satellites, 2 generations (5-year life) | 185.9 |
| Launch, 2 campaigns | 40.5 |
| Orbit transfer vehicles, 2 campaigns | 42.0 |
| Ground segment, 28 gateways (€0.3M each + €0.1M/yr) | 36.4 |
| Operations (€2M/yr + €20k/sat/yr + €1M ITU crosslink filing) | 43.4 |
| **Total** | **348.2** |

**Main cost risk:** launch per plane. In the sensitivity run on the 105-satellite variant, a dedicated €7.5M
launch per plane raised the 10-year cost from €333M to €501M, and the best design did not change [R].

## 6. Resilience [R]

| Event | Coverage | Worst place | Longest gap | p99 |
|---|---:|---:|---:|---:|
| Baseline | 100% | 100% | 0 min | 98.0 ms |
| 1 satellite fails (4 random draws) | 99.84% | 98.89% | 4 min | 98.8–99.1 ms |
| Svalbard gateway down | 100% | 100% | 0 min | 98.0 ms |
| Cross-plane links off above 70° latitude | 100% | 100% | 0 min | 98.1 ms |

**Weak point:** some places, at some moments, see only one satellite. When one fails, a strip under its track
loses service for up to 4 minutes per pass.

**Suggestion [E], not modelled:** fly one in-orbit spare per plane (7 in total, about €7M). A spare can drift
into a failed slot within a few weeks instead of waiting for a launch.

## 7. Alternatives

| Design | Sats | Crosslinks | p99 | 10-yr cost | Verdict | Source |
|---|---:|---|---:|---:|---|---|
| 6×16 at 800 km | 96 | Radio, in-plane only | 110 ms | €256M | Cheapest full coverage, misses 100 ms | [R] |
| 7×15 at 700 km | 105 | Radio, in-plane + 2 cross | 99.5 ms | €333M | 1-min gaps (0 in view at times), links at 0.02 dB | [S] `design_detail.py 15` |
| **7×16 at 700 km** | **112** | **Radio, in-plane + 2 cross** | **98.3 ms** | **€348M** | **Recommended** | [S] |
| 6×20 at 800 km | 120 | Laser | 99.7 ms | €473M | €125M more for the same service | [R] |
| 7×16 at 700 + 6×10 at 550 km | 172 | Radio + laser | 96.4 ms | €504M | Mixed altitudes cost more | [R] |
| 17×18 at 500 km | 306 | Laser, full grid | 84.8 ms | €1,211M | Survives a failure (2 in view), 3.5× the cost | [R] |

## 8. Limits of the model

- **Orbits:** circular, with no J2 perturbation or drag decay in the propagation (`globalnet/geometry.py`).
- **Grid resolution:** 2,000 grid points about 450 km apart, so very small, very short gaps can be missed. Raise `grid_points` in `design_detail.py` to tighten the check.
- **Traffic:** no traffic load, so crosslink capacity, queueing and congestion are not modelled.
- **Radio crosslink numbers [A]:** starting assumptions to check against data sheets. The design is sensitive to them because of the margin issue above.
- **Ground segment:** 28 gateways and 12 internet exchanges, with no sovereignty rules, rain fade or interference.

## How to verify

```bash
cd 07-constellation-optimization
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # once
.venv/bin/python design_detail.py 16      # every [S] number for the recommended design
.venv/bin/python design_detail.py 15      # the 105-satellite variant
.venv/bin/python -m pytest -q             # model tests
less results/report.md                    # every [R] number
```

To test an assumption [A], edit it in `globalnet/config.py` or `costmodel.py` and re-run `design_detail.py`.
For example, raise `eirp_dbw` of the RF crosslink by 3 dB and check the links-up count and p99.
