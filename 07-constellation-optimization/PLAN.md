# Plan: multi-objective LEO constellation optimisation

**Goal.** Find the constellation designs that best trade **coverage**, **latency** and **cost**. Altitudes can
be mixed (up to 3 shells, each at its own altitude). ISL technology (RF or optical), the number of ISL terminals
per satellite and the satellite cost are all decision variables. The output is a Pareto set of designs, not a
single number, plus a recommended "knee" design and the cheapest design for each service tier.

**Starting point.** `05-global-coverage` already has most of the physics:

| Already there (`05-global-coverage/globalnet`) | Missing for this study |
|---|---|
| Walker shells, several shells per design | Altitude-dependent cost (launch Δv, propulsion, deorbit, lifetime, radiation) |
| Equal-area global grid, 28 gateways, 12 PoPs | **RF vs optical ISL**: range, rate, per-hop delay, cost, mass, power |
| Dijkstra over the ISL mesh, per-step latency | **Number of ISL terminals** per satellite (0/2/3/4) and relay subsets |
| Coverage, max gap, sats in view, latency p50–p99, worst-point p95 | **Inter-shell links** (needed for mixed altitudes to pay off) |
| `optimize.py`: cheapest gap-free design per latency target | Several objectives at once, mixed-integer search over shells and ISL options |
| Cost = sats × €1.53 M flat | Lifecycle cost (TCO) over a service horizon |

So the plan is: **extend `globalnet` for ISL technology and inter-shell links (defaults unchanged), add a cost
model, and wrap both in a multi-objective optimiser** in a new folder `07-constellation-optimization/`.

> **Status (19 Oct 2026): implemented and run.** See `README.md` for results. Changes from the plan as written:
> NSGA-II is a small in-house implementation (`solve.py`), not `pymoo`, since every variable is discrete;
> Walker phasing F is a gene instead of an inner loop; the polar laser shutoff is a robustness scenario, not a
> decision variable (a design would never choose it); the default run uses up to 2 shells (`--max-shells 3` works).

---

## 1. The optimisation problem

### 1.1 Decision variables  *x*

Per shell *s* = 1..K (K ≤ 3; a shell can be switched off):

| Variable | Domain | Notes |
|---|---|---|
| `active_s` | {0, 1} | shell 1 is always active |
| `h_s` altitude | {450, 500, 550, 600, 700, 800, 1000, 1200} km | discrete. Fine enough, and keeps evaluations cacheable |
| `i_s` inclination | {53, 70, 80, 87, 97.6} deg | |
| `pattern_s` | {star, delta} | star only for i ≥ 80° |
| `P_s` planes | 2..30 | |
| `S_s` sats per plane | 2..40 | lower bound from `min_spp(h_s)` when the shell must cover on its own |
| `F_s` phasing | 0..P_s−1 | inner search only (see §3.2). Cheap to tune, large effect on gaps |
| `tech_in_s` in-plane ISL | {none, RF, optical} | |
| `tech_x_s` cross-plane ISL | {none, RF, optical} | |
| `n_isl_s` terminals / sat | {0, 2, 3, 4} | 2 = in-plane only, 3 = in-plane + one cross-plane ("brick"), 4 = +Grid |
| `rho_s` cross-plane fraction | {1, 1/2, 1/4} | share of satellites carrying cross-plane terminals (relay subset, as in the proposal) |
| `polar_off_s` | {none, 70°} | cross-plane links switched off above this latitude (real-world limit) |

Design-wide:

| Variable | Domain | Notes |
|---|---|---|
| `inter_shell` | {0, 1} | optical links between shells (the nearest satellite in the other shell within range) |
| `bus` | {12U, 16U, ESPA-150 kg} | derived, not free: the smallest bus whose mass and power fit the payload, terminals and propulsion |

Consistency rules (repair before evaluation, not penalties): `n_isl = 0 ⇔ tech_in = tech_x = none`; `n_isl = 2 ⇒
tech_x = none`; `rho < 1` only with `n_isl ≥ 3`; inter-shell links need a free optical terminal.

### 1.2 Objectives

| | Objective | Metric (from `Result.summary()`, plus additions) | Why this one |
|---|---|---|---|
| f₁ | **min cost** | 10-year TCO in M EUR (§2.3) | includes replenishment, so short-lived low shells are not "free" |
| f₂ | **min latency** | `latency_p99_ms` over all place-time samples (switch: `worst_point_p95_ms`) | p99 is what an SLA quotes; worst-point p95 is the "whole Earth" figure |
| f₃ | **max coverage** | `coverage_mean` (area × time). Report `coverage_worst_point` and `max_gap_min` too | continuous, so the optimiser has a gradient towards full coverage |

All three are minimised: f₃ is written as `1 − coverage_mean`.

### 1.3 Constraints *g(x) ≤ 0*

| Constraint | Default | Source |
|---|---|---|
| Terminal min elevation | ≥ 10°; gateway ≥ 5° | `config.py`, unchanged |
| Minimum service | `coverage_mean ≥ 0.90` (a floor; above it coverage is an objective) | user-tunable |
| Max gap (optional tier) | `max_gap_min ≤ 90` (the store-and-forward tier) | proposal tiers |
| Redundancy (optional) | `min_sats_in_view ≥ 2` | survives one failure |
| ISL geometry | every planned link ≤ its tech's max range and clears 80 km of atmosphere | handled inside the model: a link that does not close is dropped, and that shows up as a latency or coverage loss |
| Bus fit | Σ mass ≤ bus mass, Σ power ≤ bus power | §2.2 |
| Debris rule | deorbit within 5 years: altitude > ~600 km ⇒ propulsion mass carried | FCC 5-year rule / ESA Zero Debris |
| Budget (optional) | capex ≤ B | e.g. €150 M at OQ's scale |
| Fleet size | total sats ≤ 800 | keeps run time bounded |
| Sovereignty (parameter, not variable) | optical terminals from European suppliers (cost table uses Tesat/Mynaric prices) | `01-research/08-OUR-PROPOSAL.md` |

Formally: **min F(x) = (f₁, f₂, f₃)  subject to  g(x) ≤ 0, x ∈ X (mixed integer)**. F is a black box (a
time-stepped simulation), non-convex and non-smooth, so it is solved with a derivative-free multi-objective
search plus ε-constraint runs for the concrete answers (§3).

---

## 2. Models to add

### 2.1 ISL technology (`globalnet/config.py`, `globalnet/model.py`)

New `IslTech` dataclass, one row per technology. These numbers are **starting assumptions to check against data
sheets** and are kept in one table so they are easy to change:

| Parameter | RF (S/Ka-band smallsat crosslink) | Optical (SCOT20 / CONDOR class) |
|---|---|---|
| Max range | ~2,500 km (from the link budget, see below) | 4,500–6,000 km |
| Data rate | 1–10 Mbps, falls with range (Shannon on the link budget) | 100 Mbps–10 Gbps, fixed |
| Per-hop processing | 2 ms | 2 ms |
| Link acquisition | ~0 (wide beam) | 10–60 s per new cross-plane partner (link counts as down until acquired) |
| Cost per terminal | €0.05–0.15 M | €0.2–0.5 M (proposal: ~€70 M for 4 × 90 ⇒ ~€0.19 M) |
| Mass / power per terminal | 1–2 kg / 10–20 W | 1.7–12 kg / 20–80 W |
| Spectrum licence | needed (ITU filing, EPFD) | none |

Changes to the model:
1. **Range from a link budget for RF.** Compute ISL range and rate from EIRP, G/T and bandwidth, the same way
   `uplink_snr_db` does for the service link. A sparse shell with RF cross-plane then loses those links on its
   own, which is exactly the trade we want the optimiser to see.
2. **Hop weight** = distance / c + per-hop processing + 200 B / link rate. Currently it is distance / c + 2 ms.
3. **Terminal count and relay subset.** `n_isl = 3` gives one cross-plane link per satellite, alternating sides
   (brick). `rho < 1` gives cross-plane terminals only to every 2nd or 4th satellite. The existing "nearest in
   adjacent plane" matching is kept, but limited to satellites that carry a terminal.
4. **Optical acquisition.** Remember the partner from the previous step. If it changed, the link is down for
   `acquisition_s` (with 60 s steps, any change costs one step).
5. **Polar shutoff.** Drop cross-plane links when both ends are above `polar_off` latitude.
6. **Inter-shell links.** Each satellite with a spare optical terminal links to its nearest satellite in the
   other shell within range (greedy matching, one link per terminal). Without this, the current model only
   joins shells at gateways, so a "low shell for latency + high shell as backbone" design is unfairly penalised.

Backward compatibility: the defaults (`optical`, `n_isl = 4`, `rho = 1`, no inter-shell links, no shutoff)
reproduce today's `grid` mode, and a test pins the `05` results table to ±1 ms.

### 2.2 Satellite mass, power and bus (`costmodel.py`)

```
m_sat = m_bus_dry(bus) + m_payload_gNB + n_rf·m_rf + n_opt·m_opt + m_prop(Δv_total, m_dry)
Δv_total = Δv_raise(525 km → h)            # rideshare drop-off ~525 km; Hohmann transfer
         + Δv_station_keeping(h) · life    # drag; large below 500 km
         + Δv_deorbit(h)                   # lower perigee to ~300 km; 0 if h ≲ 600 km (natural decay < 5 y)
m_prop  = m_dry · (exp(Δv / (Isp·g0)) − 1)    # rocket equation, Isp ~ 220 s (green monoprop) or ~1,500 s (electric)
```

The bus is the smallest of {12U ~25 kg/100 W, 16U ~35 kg/150 W, ESPA ~150 kg/600 W} that fits mass and power.
The bus class steps the cost, which is how "more ISL terminals" turns into a bigger, more expensive satellite.

**Lifetime L(h)** (sets replenishment):
- below ~500 km: drag-limited unless propellant is carried (included through station-keeping Δv);
- 500–900 km: design life, 5 years (proposal);
- above ~1,000 km: radiation (inner Van Allen belt edge), 5 → 3–4 years, or shielding mass +x kg (choose one
  and record it).

### 2.3 Cost (`costmodel.py`)

10-year total cost of ownership, in M EUR, optionally discounted at rate r:

```
TCO = Σ_shells N_s · c_sat(s) · ⌈T / L(h_s)⌉          # build + replenish
    + Σ_shells N_s · m_sat(s) · c_launch_per_kg          # rideshare, ~€6k/kg
    + Σ_shells P_s · c_plane(h_s, i_s)                   # getting each plane its own RAAN
    + c_ground + c_ops · T                               # 28 gateways fixed for now; ops scale with N
c_sat   = c_bus(bus) + c_gNB + n_rf·c_rf + n_opt·c_opt + c_propulsion(h)
c_plane = min(dedicated small launcher ≈ €7–8 M,         # Electron-class
              OTV tug ≈ €1–2 M,                          # orbital transfer vehicle
              J2 drift ≈ €0 but a 6–18-month deployment delay; counted as a cost of delay)
```

Calibration: with 90 satellites, 5-year life and €0.75 M all-in, the model must give ~€13.5 M/yr replenishment
and ~€68 M initial capex (`01-research/08-OUR-PROPOSAL.md` §cost). A test pins this.

Per-plane cost matters most: it decides between "few planes with many satellites" and "many thin planes", and it
is the main reason a single mixed-altitude design can beat two separate shells.

---

## 3. Solution method

The search space is about 10¹⁰ points with K = 3, and one evaluation takes 5–15 s at screen fidelity. Exhaustive
search is out, so the solve is staged:

### 3.1 Stage 0: analytic pruning (milliseconds)
- Use the existing `min_spp(h)` and `min_planes(h, i)` for shells that must cover alone. A shell flown with a
  coverage shell may be sparser (halve the bound, as `optimize.py` already does).
- **ISL feasibility before simulating:** in-plane distance `2r·sin(π/S)` must be ≤ tech range; cross-plane
  distance at the equator `≈ 2r·sin(π/(2P))` (star) must be ≤ tech range. Infeasible combinations get repaired
  (more sats per plane) or dropped.
- Lower bounds on cost and latency (cost from N alone; latency ≥ 50 ms fixed + 2h/c), used to discard
  dominated candidates without simulating them.

### 3.2 Stage 1: multi-objective search at screen fidelity
- **NSGA-II** (`pymoo`, mixed-variable support), population 64–96, 40–60 generations ⇒ ~3–5k evaluations.
  Evaluations are parallel (`ProcessPoolExecutor` locally, or the existing `sweep.slurm` pattern on MeluXina)
  and cached on the design key (all variables are discrete).
- Screen fidelity = 3 h / 120 s / 1,000 points, the same as `optimize.py`.
- **Inner loop on phasing F:** for each candidate, try F ∈ {0, 1, P/2} and keep the best. This is cheap and
  stops a good geometry being discarded because of a bad phasing.
- Seed the population with known designs (the `05` presets, Iridium 6×11 RF, the proposal's 90-sat hybrid) so
  the front starts from real reference points.

### 3.3 Stage 2: ε-constraint answers (the numbers people will quote)
For each service tier, solve **min TCO s.t. coverage ≥ c\*, latency ≤ L\***:
- c\* ∈ {0.90, 0.99, full (worst point = 1.0)}
- L\* ∈ {150, 120, 100, 90} ms on p99
This is `optimize.py`'s current approach, generalised to the new variables, starting from the NSGA-II front
(the cheapest front points meeting each tier, then local moves ±1 plane / ±1 sat per plane / swap ISL tech).

### 3.4 Stage 3: confirmation and robustness
- Re-run every Pareto point and every tier answer at full fidelity (24 h / 60 s / 2,000 points). Drop the ones
  that fail and take the next candidate (as `optimize.py` already does).
- Robustness on the final picks only: one random satellite failure (10 draws), gateway outage
  (`--block Svalbard` etc.), and the polar shutoff turned on. Report how much latency and coverage degrade.
- Sensitivity of the winner to the cost assumptions: ±50% on optical terminal cost, launch €/kg and plane cost.
  The **RF ↔ optical crossover** (the optical price at which the optimum switches technology) is a headline
  result.

### 3.5 Stage 4: pick and explain
- **Knee point** of the 3-D front: the design that maximises the distance to the line between the extremes (or
  the smallest marginal cost per ms saved).
- Report: the Pareto table, the tier table, by-latitude coverage of the picks, and a cost breakdown (bus /
  terminals / launch / planes / replenishment).

---

## 4. Code layout

```
05-global-coverage/globalnet/         (extended; defaults unchanged)
  config.py      + IslTech table (RF, optical), Shell.isl_in/isl_x/n_isl/rho/polar_off, Design.inter_shell
  model.py       isl_edges(): per-tech range/rate/hop weight, terminal limits, relay subset,
                 acquisition memory, polar shutoff, inter-shell links

07-constellation-optimization/
  PLAN.md        this file
  README.md      question, how to run, results (written last)
  costmodel.py   mass/Δv/propellant, bus selection, lifetime, TCO with a breakdown
  problem.py     variables ↔ Design encoding, repair, constraints, objective evaluation + cache
  solve.py       Stage 0–3 driver: prune → NSGA-II → ε-constraint → confirm → robustness
  report.py      Pareto/tier tables, knee, sensitivity, CSV + markdown output
  sweep.slurm    MeluXina job (copy of the 05 one: account, gpu partition, QOS)
  requirements.txt  numpy scipy pandas pymoo tabulate
  tests/
    test_compat.py     default tech reproduces the 05 results table (±1 ms, ±0.1% coverage)
    test_isl.py        RF range drops sparse cross-plane links; acquisition and shutoff remove links
    test_cost.py       proposal calibration (90 sats → ~€68 M capex, ~€13.5 M/yr); cost rises with h above 600 km
    test_problem.py    encoding round-trip; repair rules; infeasible ISL geometry is caught in stage 0
  results/
```

`07` imports `globalnet` from `../05-global-coverage` (one `sys.path` line, as `04`/`05` are run from their own folders).

---

## 5. Milestones

| # | Work | Done when |
|---|---|---|
| 1 | `IslTech` + model changes (RF/optical, n_isl, rho, shutoff) | `test_compat` and `test_isl` pass |
| 2 | Inter-shell links | a 2-shell design with links has lower p99 than without; a test covers it |
| 3 | `costmodel.py` | `test_cost` passes; breakdown printed for the `05` presets |
| 4 | `problem.py` + stage 0 pruning | random designs encode/repair/evaluate; pruning rate reported |
| 5 | NSGA-II at screen fidelity (local, small population) | front found in < 1 h on 8 cores |
| 6 | ε-constraint + full-fidelity confirmation | tier table produced |
| 7 | Full run on MeluXina + robustness + sensitivity | final tables in `results/` |
| 8 | README with results and limits; link from the root README | |

Compute estimate: ~4k screen evaluations × ~10 s ≈ 11 core-hours, plus ~100 full-fidelity runs × ~60 s. About
1.5 h on 8 cores, or under 10 min on one MeluXina node.

---

## 6. Assumptions to confirm

1. **Cost numbers.** The RF/optical terminal prices, €/kg launch and per-plane cost drive the answer. They are
   placeholders from `01-research` and need a source each (like the `06` report's confidence column).
2. **Latency metric.** p99 over all samples (SLA-style) or p95 at the worst point (the "whole Earth" claim)?
   The plan defaults to p99 and reports both.
3. **Coverage as objective or constraint.** The default is a 90% floor with coverage as the third objective. If
   only full coverage counts, it becomes a constraint and the problem is 2-objective (simpler, faster).
4. **Horizon.** 10-year TCO, undiscounted by default.
5. **Gateways fixed at 28.** Making gateway count a variable is a natural next step (it trades directly against
   ISL), but it is left out of this plan to keep the search space manageable.

## 7. Known limits (carried over or new)

- Coverage and latency only: no traffic or capacity, so optical's throughput advantage is not valued. That is
  fine for narrowband IoT (proposal §ISL) but wrong for broadband.
- Circular orbits, no J2 (except in the plane-cost option), no drag decay during the 24 h.
- RF ISL interference and spectrum coordination are a cost line, not modelled physically.
- The cost model is parametric and calibrated to one point (the proposal). The ranking of designs is more
  trustworthy than the absolute euros.
