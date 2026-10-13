# Lynq NTN-Pulse: simulation

Digital twin of a regenerative gNB-onboard LEO constellation over the North Sea, built for Phase 2 of the
OQ Technology challenge. It runs the comparison promised in the proposal (section 05): **12 vs. 30 satellites,
bent-pipe vs. regenerative, with changing visibility, gateway access, load and ISL conditions**, and reports
latency, delivery probability, queue depth and routing compliance.

## Quick start

```bash
cd 04-simulation
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

.venv/bin/streamlit run dashboard.py      # interactive dashboard
.venv/bin/python run.py                   # full scenario matrix -> results/*.csv (~2.5 min)
.venv/bin/python -m pytest -q tests       # physics sanity checks
```

`run.py --help` lists the options (`--sats 12 30 60`, `--hours`, `--block Stavanger`, `--loads`, ...).

## What the model does

Each time step (default 10 s over 24 h) the topology is frozen and rebuilt:

1. **Orbits.** Walker constellation of circular orbits in a rotating Earth (`ntnpulse/geometry.py`).
   Presets: `today-12` (2 x 6, SSO 97.6°), `planned-30` (3 x 10, SSO), `scale-60` (6 x 10); any shape in the dashboard.
2. **Visibility.** Elevation and slant range for every terminal and gateway to every satellite
   (10° mask for terminals, 5° for gateways).
3. **Links.** Free-space path loss → uplink SNR → derated Shannon rate on one 180 kHz NB-IoT carrier
   (`ntnpulse/links.py`). RF ISL to in-plane neighbours and optical ISL between relay satellites in adjacent
   planes, each only if in range **and** clear of the atmosphere (80 km grazing height).
4. **Routing graph.** Gateways → satellites → ISL mesh. Edge weight = propagation delay + processing, and
   feeder edges also carry gateway → 5G Core → Frankfurt cloud fibre delay. Gateways are endpoints only, so
   traffic can never bounce through an unauthorised ground station.
5. **Policy.** Each terminal's jurisdiction (`UK`, `NO`, `EEA`, international waters) has an allowed set of
   gateway countries. Dijkstra runs once per jurisdiction from its allowed gateways only, so routing is compliant
   by construction. The engine also records when the latency-optimal gateway was *not* allowed ("policy re-routed").
6. **Traffic and queues.** Three classes from the proposal: **critical** (alarms, 100–400 B, served first),
   **metadata** (status, ~64 B) and **regular** (telemetry/files, 1–100 kB). Per-satellite uplink, feeder and
   ISL capacities are enforced every step. Messages that cannot go now wait:
   - **bent-pipe:** on the terminal, until one satellite sees the terminal *and* an allowed gateway at the same time;
   - **regenerative:** onboard the satellite (store-and-forward, 50 MB buffer) until it has a path;
   - **regenerative + ISL:** same, but the path may hop across the mesh.

**Latency** = waiting time (terminal + onboard) + random access + transmission (size / link rate) + propagation
on every hop + gNB/ISL/ground processing + terrestrial fibre to the cloud.

All assumptions (link budget, capacities, delays, gateways, sectors, traffic mix) live in
`ntnpulse/config.py`. Change them there.

For the full step-by-step walkthrough, formulas, worked latency example and metric definitions, see
[HOW-IT-WORKS.md](HOW-IT-WORKS.md).

## Results (24 h, 300 terminals, 10 s steps)

Output of `python run.py`, abridged. Critical = alarms; `<250 ms` is the mesh-relayed tier.

| Sats | Mode | Gateway offline | Load | Critical p50 | Critical p95 | Critical <250 ms | All ≤90 min | Max gap | Peak onboard queue |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 12 | Bent-pipe | – | 1x | 430 s | 3.2 h | 23% | 79% | 246 min | – |
| 12 | Regen + ISL | – | 1x | 425 s | 3.1 h | 23% | 80% | 246 min | 1.7 MB |
| 30 | Bent-pipe | – | 1x | 90 ms | 77 min | 56% | 97% | 118 min | – |
| 30 | Regen, no ISL | – | 1x | 85 ms | 70 min | 56% | 98% | 118 min | 2.1 MB |
| 30 | Regen + ISL | – | 1x | 84 ms | 60 min | 59% | 98% | 118 min | 0.08 MB |
| 30 | Bent-pipe | Stavanger | 1x | 30 s | 80 min | 47% | 96% | 118 min | – |
| 30 | Regen, no ISL | Stavanger | 1x | 35 s | 84 min | 47% | 97% | 118 min | 9.0 MB |
| 30 | **Regen + ISL** | Stavanger | 1x | **100 ms** | 60 min | **58%** | 98% | 118 min | 0.2 MB |
| 30 | Regen + ISL | Stavanger | 5x | 102 ms | 67 min | 57% | 97% | 118 min | 1.0 MB |

Routing compliance was 100% in every scenario.

What this shows:

- **12 satellites give passes, not coverage.** The basin is in view ~26% of the time, with gaps of up to 4 h.
  Alarms wait for the next pass (median ~7 min). The ISL adds nothing at 12, because 6 satellites per plane are 60°
  apart and the Earth blocks the in-plane link. This matches the proposal's "frequent passes, not continuous coverage".
- **At 30 satellites the in-plane RF ring closes** (10 per plane, ~4,280 km hops, ~14 ms each). Live alarms land
  in Frankfurt in **~85 ms**, inside the <150 ms tier.
- **ISL is what makes sovereignty cheap.** With Stavanger offline, Norwegian-sector data may only land at Svalbard.
  Bent-pipe and regen-without-ISL then wait for a satellite that sees both ends: the critical median jumps from
  0.09 s to **30–35 s** and onboard queues grow 4x. With ISL, traffic relays north over the mesh and the median
  stays at **~100 ms**.
- **Orbit choice beats satellite count for the North Sea.** The same 30 satellites in a **65° Walker delta**
  (the research pack's service shell) instead of sun-synchronous planes cover the basin 79% of the time (vs. 61%),
  cut the worst gap from **118 min to 3 min** and put 75% of alarms under 250 ms (vs. 59%). Try the
  "30 (65 deg Walker delta)" preset in the dashboard.

## Dashboard

`streamlit run dashboard.py`. The sidebar sets the constellation (presets or custom planes, altitude, inclination,
star/delta spacing, optical relay density), payload mode or a side-by-side comparison of all three, offline
gateways, load, terminal count, duration and step.

- **KPIs**: delivery ratio, critical latency, tier compliance, longest coverage gap, routing compliance.
- **Latency**: CDFs for critical alarms by mode and for every class; per-path millisecond breakdown; per-sector table.
- **Network map**: globe with satellites (stars carry optical terminals), RF/optical ISLs, feeder links,
  gateways (offline ones marked) and terminals, at any minute of the run.
- **Queues & coverage**: onboard store-and-forward queue, messages waiting on terminals, satellites over the basin.
- **Policy**: where each jurisdiction's traffic lands, compliance and policy re-routing.
- **Data**: per-class tables and a CSV download of every delivered message.

## Limits

- Circular orbits without J2 or drag: fine for a day, not for long-term station keeping.
- Uplink only (terminal → cloud). Downlink commands would mirror it with the same graph.
- Link budget is one fixed-parameter NB-IoT carrier. No beams, interference, rain fade or Doppler residuals.
  Doppler and timing are assumed pre-compensated per 3GPP Rel-17.
- The ISL is assumed always acquired when geometry allows. No pointing/acquisition time is modelled for optical links.
- Gateways have no outage statistics. Blocking one is an on/off scenario switch.
- No cost model yet. TCO stays in the proposal's spreadsheet numbers.
