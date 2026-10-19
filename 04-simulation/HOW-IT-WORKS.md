# How the simulation works

A walkthrough of the NTN-Pulse simulation engine: what it computes in each step, the formulas and assumptions behind it, and what every output metric means. For setup and results, see [README.md](README.md).

## The core idea

The simulation is **time-stepped**. It cuts 24 hours into 10-second steps (8,640 steps). In each step it treats the network as frozen: satellites move only about 75 km in 10 s. It then answers three questions:

1. Who can see whom right now?
2. What is the fastest *allowed* route from each satellite to the cloud?
3. Which waiting messages can go now, and which keep waiting?

```
for each 10 s step:
    1. move satellites           (geometry.py)
    2. work out visibility       (geometry.py + links.py)
    3. build the network graph   (engine.py: topology)
    4. find allowed routes       (engine.py: Dijkstra per jurisdiction)
    5. reset link capacities
    6. generate new messages     (engine.py: _generate)
    7. send stored messages      (engine.py: _serve_onboard)
    8. send terminal messages    (engine.py: _serve_terminals)
    9. record the state          (engine.py: _log_step)
```

All assumed numbers live in `ntnpulse/config.py`. The engine reads everything from there, so change values there, not in the code.

## Step 1: Orbits (`geometry.py`)

- **Constellation layout (Walker):** the planned fleet is 30 satellites = 3 orbital planes × 10 satellites. The planes are spread evenly around the Earth (over 180° for a "star" pattern, 360° for a "delta"), and satellites are spread evenly within each plane.
- **Each satellite's orbit:** a circle at 550 km. The period comes from physics: T = 2π√(r³/μ) = **95.6 minutes** (checked by a test).
- **Earth rotation:** positions are computed in an Earth-fixed frame, so ground tracks shift west on each orbit, as real ones do.
- **Simplification:** no Earth oblateness (J2) or drag. This is accurate enough over a day.

Presets in `config.py`:

| Preset | Layout | Inclination |
|---|---|---|
| `design-7x16` (default) | 7 planes × 16, 700 km, F0, RF cross-plane links, seam unlinked | 87° (Walker star) |
| `today-12` | 2 planes × 6 | 97.6° (sun-synchronous, like OQ's rideshares) |
| `planned-30` | 3 planes × 10 | 97.6° |
| `scale-60` | 6 planes × 10 | 97.6° |

The dashboard also offers a 30-satellite 65° Walker delta preset, and fully custom layouts.

## Step 2: Visibility and links

### Elevation

For every terminal (and gateway) against every satellite, the engine computes the angle above the horizon and the distance:

- Terminals need **≥10°** elevation. Gateways need **≥5°**, because their dishes can look lower.
- At 10° the distance to a 550 km satellite is **1,815 km**, matching the table in `01-research/04-TECHNICAL-deep-dive.md` (checked by a test).

### Link budget (`links.py`)

This decides whether a terminal can reach a satellite, and how fast:

```
path loss = 20·log10(distance km) + 20·log10(2000 MHz) + 32.44
SNR       = terminal power (−7 dBW) − path loss − 3 dB losses + satellite G/T (−5 dB/K) − noise (kTB, 180 kHz)
rate      = 0.5 × 180 kHz × log2(1 + SNR), capped at 120 kbps
```

| Distance | SNR | Rate | Time to send 200 B |
|---|---|---|---|
| 1,200 km | +1.0 dB | ~106 kbps | 15 ms |
| 1,815 km (10° edge) | −2.6 dB | ~57 kbps | 28 ms |

Overhead the rate hits the 120 kbps cap. Below −10 dB SNR the link fails, and the terminal can't use that satellite.

### Links between satellites

- **RF links (same plane):** each satellite tries to link to the next one in its plane. A link exists only if it is within 5,000 km **and** the straight line between them clears the atmosphere by 80 km.
  - With 6 per plane (12 satellites), neighbours are 60° apart and the Earth blocks the line, so there are **no RF links**.
  - With 10 per plane (30 satellites), neighbours are 4,280 km apart and the line clears, so each plane **closes a ring**.
- **Laser links (between planes):** every second satellite carries a laser terminal and links to the nearest laser-equipped satellite in the next plane, if it is within 6,000 km and in line of sight.

These links only exist in "Regenerative + ISL" mode.

## Steps 3–4: Routing graph and policy (`engine.py: topology`)

### Network graph

Nodes are satellites and gateways. Each edge's weight is its **delay in seconds**:

| Edge | Weight |
|---|---|
| Satellite ↔ satellite | distance / speed of light + 2 ms processing per hop |
| Gateway → satellite | distance / c + 10 ms gateway and 5G core processing + **fibre time to Frankfurt** (great-circle distance × 1.5 for real routes, at 2/3 c) |

Including the fibre leg means the route finder optimises total delay all the way to the cloud, not just to the nearest dish.

**Gateways are endpoints only.** Edges point from gateway to satellite, so a route can never go satellite → gateway → satellite. That would be a hidden ground hop, possibly through a station the policy forbids.

### Sovereignty

Each terminal belongs to a jurisdiction. Each jurisdiction lists the gateway countries allowed to receive its data:

| Jurisdiction | Allowed gateways |
|---|---|
| UK sector | UK only (Aberdeen) |
| NO sector | Norway only (Stavanger, Svalbard) |
| DK / NL / DE sectors | EEA (NO, DK, NL, DE, LU) |
| Atlantic (international waters) | Any |

For each jurisdiction, the engine runs **one Dijkstra search per step, starting only from that jurisdiction's allowed gateways**. The result is the fastest legal route, and its delay, from every satellite. Forbidden gateways are never in the search, so routing is **compliant by construction**.

It also runs one unrestricted search. Comparing the two shows when the fastest gateway was not allowed and the policy picked another ("policy re-routed").

Gateways switched off in the scenario (for example Stavanger) are left out of the graph entirely.

## Step 5: Capacity

At the start of each step, every link gets a byte budget for that step:

| Link | Capacity | Budget per 10 s step |
|---|---|---|
| Satellite uplink (shared by all terminals it serves) | 1 Mbps | 1.25 MB |
| Feeder link | 20 Mbps | 25 MB |
| RF link between satellites | 10 Mbps | 12.5 MB |
| Laser link between satellites | 1 Gbps | 1.25 GB |

A message can be sent only if **every link on its route** has room left. Otherwise it waits. This is how heavy load turns into queues and delay.

## Step 6: Traffic (`_generate`)

Messages are generated at random (Poisson) from 300 terminals spread over five offshore sectors (UK 30%, NO 30%, DK 15%, NL/DE 15%, Atlantic 10%):

| Class | Size | Rate per terminal | Priority | Expires after |
|---|---|---|---|---|
| critical (alarms) | 100–400 B | 1 per 6 h | Served first | 6 h |
| metadata (status, position) | 48–96 B | 1 per 30 min | Second | 6 h |
| regular (telemetry, files) | 1–100 kB | 1 per 15 min | Last | 12 h |

The **load** setting multiplies these rates. New messages stop in the final 2 hours so queues can drain before the run ends.

## Steps 7–8: Sending messages

Every terminal and every satellite keeps a **priority queue**: alarms first, then oldest first. **Stored messages are tried before new ones**, because they have waited longer.

For each terminal with waiting messages and at least one satellite in view, the engine picks the visible satellite with the lowest total delay (uplink plus the best legal route). If no visible satellite has a route, it picks the closest one. Then the payload mode decides what happens:

| Mode | Behaviour |
|---|---|
| **Bent-pipe** | The satellite only relays. The message can go only if *that same satellite* sees an allowed gateway *right now*. Otherwise it **stays on the terminal**. |
| **Regenerative, no ISL** | The satellite runs the gNB. It takes the message and delivers it if it can reach an allowed gateway directly. Otherwise it **stores it on board** (50 MB buffer) and retries every step until it passes over an allowed gateway. |
| **Regenerative + ISL** | Same, but the route can **relay across satellites**, so it is often deliverable immediately even with no gateway in view. |

### Drops

| Reason | When |
|---|---|
| `ttl` | The message waited past its class's expiry time |
| `buffer` | The satellite's onboard buffer was full when the message arrived |
| `pending` | Still waiting when the run ended (counted, not dropped) |

## How latency is calculated

```
latency = waiting time            (on the terminal + on board, in whole steps)
        + 20 ms                   network access (connection request + grant)
        + size × 8 / rate         transmission time
        + uplink distance / c
        + 5 ms                    gNB processing (10 ms on the ground for bent-pipe)
        + route delay             satellite hops + feeder + gateway/core + fibre to Frankfurt
```

For stored messages, the waiting time already covers the original upload, so only the onward route delay is added when they are finally sent.

### Worked example

A 200-byte alarm from the Norwegian sector, sent live via Stavanger with the satellite about 1,200 km away:

| Part | Time |
|---|---|
| Waiting | 0 ms |
| Network access | 20 ms |
| Transmission (200 B at ~106 kbps) | 15 ms |
| Uplink (~1,200 km) | 4 ms |
| gNB processing | 5 ms |
| Feeder down to Stavanger | ~4 ms |
| Gateway and 5G core | 10 ms |
| Fibre Stavanger → Frankfurt (~1,000 km) | 7 ms |
| **Total** | **≈ 65 ms** |

The simulated median for alarms sent live is 68 ms, consistent with this. Most of the time is radio access and transmission, not the distance to space.

If no satellite is in view, waiting time takes over (minutes). That is what the coverage-gap numbers capture.

## Step 9: What gets recorded

**Per delivered message (`Result.records`):**

| Column | Meaning |
|---|---|
| `cls`, `size`, `sector`, `jurisdiction` | What the message was and where it came from |
| `wait_terminal_s` | Time waiting on the terminal before upload |
| `wait_onboard_s` | Time stored on the satellite |
| `network_s` | Access, transmission, propagation and processing delay |
| `latency_s` | Total end-to-end latency |
| `sat`, `gateway`, `gw_country` | Where it went |
| `isl_hops` | Number of satellite-to-satellite hops |
| `path` | `direct`, `isl` (relayed live) or `store_forward` |
| `compliant` | Landed at an allowed gateway |
| `policy_redirect` | The fastest gateway was forbidden, so the policy chose another |

**Per step (`Result.series`):** satellites over the basin, share of terminals covered, satellites with a gateway in view, number of satellite links, onboard queue size, messages waiting on terminals, and messages delivered so far.

**Handovers:** counted when a terminal's best (highest-elevation) satellite changes between steps.

## Summary metrics

| Metric | What it means |
|---|---|
| `delivery_ratio` | Delivered ÷ generated |
| `critical_p50_s`, `critical_p95_s` | Median and 95th-percentile alarm latency |
| `critical_within_250ms` | Share of alarms meeting the satellite-relayed tier (<250 ms) |
| `all_within_90min` | Share of all traffic meeting the store-and-forward tier (≤90 min) |
| `basin_coverage` | Share of time at least one satellite is over the basin centre (57°N 3°E) |
| `max_gap_min`, `mean_gap_min` | Longest and average time with no satellite over the basin |
| `handovers_per_terminal_day` | How often terminals switch satellite |
| `max_onboard_queue_kb` | Most data stored on board at once |
| `routing_compliance` | Share of messages that landed at an allowed gateway (always 100%) |
| `policy_redirects` | Share where the policy overrode the fastest gateway |

`Result.by_class()` gives the same latency and delivery figures for each traffic class.

## Reproducibility

Every random choice (terminal positions, message timing, sizes) comes from one generator seeded by `Scenario.seed`. The same settings always give the same numbers, so a demo result can be re-run exactly.

## Performance

Run time grows with the number of messages, not the number of satellites. Measured on an 8-core laptop:

| Setup | Messages per simulated day | Run time per simulated day | Memory |
|---|---:|---:|---:|
| 30 sats, 300 terminals (default) | 30k | ~20 s | 190 MB |
| 60 sats, 300 terminals | 30k | ~30 s | 190 MB |
| 30 sats, 3,000 terminals | 300k | ~1 min | 280 MB |
| 30 sats, 300 terminals, 1 s steps | 30k | ~2.3 min | 280 MB |
| 30 sats, 1,000 terminals, 10× load | ~1M | ~8.5 min | 450 MB |

Each run uses one core, and `run.py` runs scenarios in parallel across all cores. Above roughly 1M messages a day, memory becomes the limit, because every delivered message is kept as a row. The fix is to keep running totals and latency histograms, or to group terminals into traffic sources, rather than to use a bigger machine.

## Files

| File | What it does |
|---|---|
| `ntnpulse/config.py` | All assumptions and scenario definitions |
| `ntnpulse/geometry.py` | Orbits, Earth rotation, elevation, distances, line of sight |
| `ntnpulse/links.py` | Link budget and links between satellites |
| `ntnpulse/engine.py` | The step loop, routing, queues and metrics |
| `run.py` | Runs all scenarios in parallel and writes CSVs |
| `dashboard.py` | Streamlit dashboard |
| `tests/test_model.py` | Physics and behaviour checks |

## Extending it

- **Change an assumption:** edit `config.py`, for example `SAT_SERVICE_CAPACITY_BPS`, `GATEWAYS` or `JURISDICTION_RULES`.
- **Add a gateway or country rule:** add a `Gateway(...)` entry and list its country in the relevant jurisdictions.
- **Add a traffic class:** add a `TrafficClass(...)` entry. Lower `priority` is served first.
- **New constellation:** add a `Constellation(...)` to `CONSTELLATIONS`, or use the dashboard's custom option.
- **New metric:** compute it in `Result.summary()` from `records` or `series`.
