# Lynq NTN-Pulse: global coverage study

`04-simulation` answers "how well do 12 or 30 satellites serve the North Sea?". This folder asks a different
question: **what does it take to serve the whole Earth (oceans and poles included) all the time, with low
latency?** The number of satellites is **not fixed**. It is an output: the sweep tries designs from 60 to
720+ satellites and reports the smallest ones that meet the targets.

What changed from the North Sea twin:

| | 04-simulation | 05-global-coverage |
|---|---|---|
| Goal | North Sea basin, 12 → 30 satellites | Every point on Earth, satellite count free |
| Terminals | 300 in 5 offshore sectors | Equal-area grid of 2,000 points over the whole globe (~450 km apart) |
| Gateways | 7 in NW Europe | 28 worldwide teleport / TT&C sites (incl. Svalbard, Punta Arenas, Troll, McMurdo) |
| End of the path | Frankfurt | Nearest of 12 internet PoPs / cloud regions to the landing gateway |
| ISL | RF in-plane, optical on every 2nd satellite | Optical **+Grid** on every satellite (2 in-plane + 2 cross-plane), or `inplane` / `none` |
| Constellation | One Walker shell | One or more shells (e.g. 53° delta + polar cap) |
| Sovereignty | Per-jurisdiction gateway rules | Not modelled (any gateway may land any flow) |
| Traffic / queues | Full message model | Not modelled: this is a coverage and latency-floor study |

Link budget, elevation masks (10° terminal, 5° gateway) and processing delays are the same as in
`04-simulation`, so numbers are comparable.

## Quick start

```bash
cd 05-global-coverage
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

.venv/bin/python run.py                     # all presets, 24 h at 60 s steps (~2 min on 8 cores)
.venv/bin/python sweep.py --dry-run         # size of the default sweep (882 designs)
.venv/bin/python sweep.py                   # run it (~1 h on 8 cores, ~15 min on a 128-core node)
.venv/bin/python sweep.py --report          # ranking from results/sweep.csv only
.venv/bin/python optimize.py                # cheapest full-coverage design per latency target (~15 min)
.venv/bin/python -m pytest -q tests         # sanity checks
```

Custom designs: `run.py --shell 15x16@550/53/delta --shell 6x20@560/97.6/star --isl grid`.
Hybrid sweep (every inclined shell on top of a fixed polar cap):
`sweep.py --inc 53 70 --extra-shell none --extra-shell 6x20@560/97.6/star`.
On MeluXina: `sbatch sweep.slurm` (same arguments as `sweep.py`, resumable).

## What the model does

For each 60 s step over 24 h:

1. **Orbits.** All shells are propagated as circular Walker orbits in a rotating Earth (`globalnet/geometry.py`).
2. **Satellite → ground.** For each satellite, the cheapest open gateway in view (≥5°):
   feeder distance / c + 10 ms gateway/5G Core + fibre to the nearest PoP (great circle × 1.5 at 2/3 c)
   + 280 ms GEO backhaul for the Antarctic sites.
3. **Mesh.** Laser ISLs (≤6,000 km, clear of the atmosphere by 80 km) form a graph. One Dijkstra from a virtual
   "ground" node gives every satellite its fastest route down, direct or over the mesh (`scipy.sparse.csgraph`).
   The seam of a Walker star (counter-rotating first/last plane) is left unlinked.
4. **Every grid point.** Among satellites above 10° whose link budget closes, pick the one with the lowest
   end-to-end time:

```
alarm latency = 20 ms random access + 200 B / link rate + uplink / c + 5 ms gNB
              + ISL hops (distance / c + 2 ms each) + feeder + gateway/core + fibre to PoP
```

About 50 ms of that is fixed (access, transmission, processing), so ~65 ms is the practical floor.

### Metrics (`Result.summary()`)

| Column | Meaning |
|---|---|
| `coverage_mean` | Share of Earth area × time with service (grid is equal-area) |
| `coverage_worst_point` | Time share served at the worst place on Earth. **1.0 = full coverage** |
| `full_coverage` | Every grid point served at every step |
| `max_gap_min` | Longest outage anywhere |
| `min_sats_in_view` | Fewest usable satellites seen anywhere, any time (≥2 = handover / redundancy margin) |
| `latency_p50/p95/p99/max_ms` | Over every served place-time sample |
| `worst_point_p95_ms` | p95 latency at the worst place on Earth: the "low latency for the whole Earth" figure |
| `within_75/100/150ms` | Share of all place-time samples under each tier (outages count as misses) |

`run.py` also writes `by_latitude.csv`: coverage, gap and latency per 10° band.

## Results (24 h, 60 s steps, 2,000 grid points)

Output of `python run.py`:

| Design | Sats | Coverage (mean) | Worst place | Max gap | p50 | p99 | Worst place p95 | <100 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| planned-30 (3×10, 550 km SSO) | 30 | 45% | 32% | 151 min | 80 ms | 115 ms | 119 ms | 40% |
| polar-66 (6×11, 780 km, Iridium-like) | 66 | 99.0% | 96.7% | 4 min | 79 ms | 109 ms | 116 ms | 94% |
| polar-72 (6×12, 780 km) | 72 | 99.8% | 98.8% | 3 min | 77 ms | 106 ms | 113 ms | 96% |
| **polar-1200-120** (8×15, 1,200 km) | **120** | **100%** | **100%** | 0 | 78 ms | 102 ms | 108 ms | 98% |
| **polar-550-240** (12×20, 550 km) | **240** | **100%** | **100%** | 0 | 66 ms | 88 ms | 96 ms | **100%** |
| hybrid-550-360 (15×16 @53° + 6×20 polar) | 360 | 100% | 100% | 0 | 66 ms | 86 ms | 91 ms | 100% |

Same 240-satellite polar shell **without ISL**: 83% mean coverage, mid-ocean points never served, p99 384 ms.

What this shows:

- **30 satellites cannot cover the Earth.** The planned SSO fleet serves 45% of area-time; the equator sees it
  only a third of the time, with gaps of 2.5 h. It was sized for passes over one basin, not global service.
- **Full coverage starts at ~60–120 satellites in a near-polar star**, if they fly higher. At 1,200 km, 8×15 = 120
  closes every gap with at least 2 satellites always in view. A smaller-sweep run (1,000 points) even found 6×10
  at 1,200 km gap-free, but with a single satellite in view and p99 120 ms.
- **Low latency everywhere needs lower and denser shells.** Going from 1,200 km to 550 km with 240 satellites
  drops the worst-place p95 from 108 ms to 96 ms and puts 100% of samples under 100 ms. Above ~240 satellites the
  gain flattens: the ~50 ms of access and processing dominate.
- **The ISL mesh is not optional for global service.** Over open ocean no gateway is in reach of the serving
  satellite; without ISLs those places are dark however many satellites fly.
- **Polar or hybrid, not inclined-only.** A 53° delta alone leaves the polar caps (>~65°) uncovered; it only makes
  sense with a polar shell on top (`hybrid-550-360`), which buys extra capacity at mid-latitudes rather than latency.

Run `sweep.py` for the full trade space; its report prints the smallest full-coverage designs, the smallest that
also meet `--max-p99-ms` (default 100 ms), and the Pareto front of satellite count vs. worst-place latency.

## Limits

- Coverage and latency floor only: no traffic, capacity or queues. Feed a chosen design back into
  `04-simulation` for load behaviour.
- Circular orbits without J2 or drag; no inter-shell ISLs (shells meet through gateways only).
- Cross-plane lasers are assumed to stay locked near the poles; real systems often switch them off above ~70°.
- Grid points ~450 km apart at 2,000 points: short gaps in small slivers can be missed. Raise `--grid` to confirm a pick.
- No sovereignty rules, gateway outages (except `--block`), rain fade, beams or interference.
