<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="02-brand/lynq-brand-kit/logos/orbital-link/horizontal/lynq-orbital-link-horizontal-dark.svg">
    <img alt="Lynq" src="02-brand/lynq-brand-kit/logos/orbital-link/horizontal/lynq-orbital-link-horizontal-light.svg" width="320">
  </picture>
</p>

<h3 align="center">Lynq NTN-Pulse</h3>
<p align="center"><em>Every signal, the right path.</em></p>

<p align="center">
  <a href="08-final-pitch/Lynq-NTN-Pulse-final-pitch.pdf"><b>🎤 Final pitch deck (PDF)</b></a> ·
  <a href="07-constellation-optimization/DESIGN-7x16.md"><b>🛰️ 7×16 design sheet</b></a> ·
  <a href="04-simulation/README.md">Digital twin</a> ·
  <a href="07-constellation-optimization/README.md">Optimiser</a> ·
  <a href="03-proposal/current/final.pdf">Phase 1 proposal</a> ·
  <a href="01-research/00-START-HERE.md">Research pack</a>
</p>

---

Team **Lynq**'s entry for the **NEOSPACE Europe 2026** challenge set by **OQ Technology**:
*AnyPoint-NTN: Global gNB-Onboard LEO Constellation for Ubiquitous 5G NR-NTN* (category: Next-Gen Downstream).

> **In one line:** we designed a 112-satellite polar 5G constellation for OQ Technology, along with the
> cloud-to-edge software that runs it. Every IoT alarm, anywhere on Earth, reaches the cloud in under 100 ms (p99).
> Satellites, gateways and AI-enabled devices are all updated from one Kubernetes/KubeEdge control plane.
> We chose the design by searching 3,064 candidate constellations on the **MeluXina** supercomputer.
> Every number in the pitch can be reproduced from this repo.

| | |
|---|---|
| **Event** | NEOSPACE Europe 2026, 19–20 October 2026, Luxexpo The Box, Luxembourg |
| **Challenge sponsor** | OQ Technology S.à r.l. (Luxembourg), a satellite 5G IoT operator |
| **Deliverables** | Phase 1: two-page proposal. Phase 2: on-site simulation and a 10-minute pitch to a jury |
| **Status** | Done. Pitched on site; final deck in [`08-final-pitch/`](08-final-pitch/) |

## The problem

Today's satellite IoT is **neither global nor easy to run**.

- **Not global.** Most satellite IoT uses *bent-pipe* satellites. They only relay signals, so a ground gateway
  must be in view at the same time. Over open ocean there is none. Offshore energy, shipping and pipelines are
  left in the dark however many satellites fly.
- **Hard to run.** OQ is moving to *regenerative* satellites, each running a full 5G base station (gNB) in orbit.
  That turns the network into a distributed computer: a gNB on every satellite, dozens of gateways, hundreds of
  thousands of devices, and links that come and go every few minutes. Updating software or AI models by hand does not scale.

## Our solution

A complete global NTN that OQ can operate, in four parts:

| Part | What it does |
|---|---|
| **7×16 polar constellation** | 112 satellites at 700 km, 87°, linked by Ka-band RF crosslinks. Covers **100% of Earth every minute**, with alarm latency **p50 72 ms / p99 98 ms** |
| **NTN-Pulse policy engine + digital twin** | Picks a path for every message: deliver now, relay over inter-satellite links, or store and forward. Lands data **only at gateways allowed to receive it** (data residency built into routing) |
| **KubeEdge orchestration** | One control plane: cloud → gateways → satellites → devices. Satellites run as edge nodes. Updates roll out canary-first, plane by plane, with automatic rollback, and nodes keep serving when the link drops |
| **AI-enabled IoT devices** | Models run on the terminal and on the satellite, so a narrowband link carries alarms and summaries, not raw data |

```
CLOUD    KubeEdge CloudCore · NTN-Pulse twin + policy engine · AI model registry · dashboard
   │       Kubernetes API, policies, images, models
GROUND   28 gateways (EdgeCore) · 5G Core · local user-plane breakout
   │       feeder links
SPACE    112 satellites (EdgeCore) · regenerative NB-IoT gNB · onboard policy + AI
   │       Ka-band RF crosslinks: fore/aft in-plane, left/right cross-plane
DEVICES  AI-enabled IoT terminals (KubeEdge device twin / mappers) · standard 3GPP chips
```

## Key results

All results come from our own simulation code in this repo. The source is listed next to each one.

| Result | Value | Source |
|---|---|---|
| Design search | NSGA-II over **3,064 constellation designs** on MeluXina, confirmed at 24 h / 60 s / 2,000 points | [`07/results/report.md`](07-constellation-optimization/results/report.md) |
| Chosen design | **7 planes × 16 = 112 satellites**, 700 km, 87° Walker star | [`DESIGN-7x16.md`](07-constellation-optimization/DESIGN-7x16.md) |
| Coverage | **100% of Earth, every minute**, longest gap 0 min | `design_detail.py 16` |
| Alarm latency | p50 **72 ms** · p95 91 ms · p99 **98 ms** | `design_detail.py 16` |
| Cost | **€134.2M** capex (€0.83M/satellite) · **€348.2M** 10-year TCO | [`costmodel.py`](07-constellation-optimization/costmodel.py) |
| RF vs laser crosslinks | RF wins at every laser price tested. A laser 6×20 design costs **€125M more** for the same service | report §RF vs optical |
| Resilience | Gateway outage: no change. One satellite lost: 99.84% coverage, 4-min gap | DESIGN-7x16 §6 |
| Sovereign routing | With a gateway offline, alarms stay at **~100 ms** over the crosslink mesh (vs 30–35 s without it). **100% routing compliance** | [`04-simulation`](04-simulation/README.md#results-24-h-300-terminals-10-s-steps) |
| Fleet updates | A 100 MB canary + waves update reaches 30 satellites in **~1.2 h** with crosslinks vs **~21 h** without | [`FLEET-OPS.md`](04-simulation/FLEET-OPS.md) |
| Maturity | **TRL 3** today (proof of concept in simulation), target TRL 5 by Q4 2027 | [Pitch slide 05](08-final-pitch/deck.md) |

Business side of the pitch: a $2.3–3.1B satellite IoT market growing 14–23% a year. The global network
breaks even at ~290k assets × €120/yr. Lynq licenses the platform to OQ per node and per AI-enabled device,
and asks for €450k to reach TRL 5 in 12 months. See [`08-final-pitch/deck.md`](08-final-pitch/deck.md), slides 07–11.

## How the project evolved

The design changed a lot between the first draft and the pitch. Each step is kept in the repo:

1. **Research** ([`01-research/`](01-research/00-START-HERE.md)). Primer, sponsor dossier, technical, regulatory,
   business and competitor deep dives.
2. **Phase 1 proposal** ([`03-proposal/current/`](03-proposal/current/final.pdf)). Two pages, with a North Sea
   offshore focus on OQ's ~12 satellites growing to 30.
3. **North Sea digital twin** ([`04-simulation/`](04-simulation/README.md)). Orbits, link budgets, routing graph,
   queues and a jurisdiction-aware policy engine, with a Streamlit dashboard. It showed that crosslinks make
   sovereign routing cheap, and that the choice of orbit matters more than the satellite count.
4. **Global coverage study** ([`05-global-coverage/`](05-global-coverage/README.md)). This step drops the fixed
   satellite count and asks what it takes to cover the *whole* Earth with low latency.
5. **Multi-objective optimisation** ([`07-constellation-optimization/`](07-constellation-optimization/README.md)).
   NSGA-II over cost, p99 latency and coverage, with RF vs optical crosslinks as a decision variable, run as a Slurm job
   on MeluXina. It produced the **7×16** design.
6. **Fleet operations** ([`04-simulation/FLEET-OPS.md`](04-simulation/FLEET-OPS.md)). The constellation modelled as a
   KubeEdge edge cluster: control-plane reachability, and over-the-air rollouts over the crosslink mesh.
7. **Final pitch** ([`08-final-pitch/`](08-final-pitch/)). 15 slides plus backups, with a script and a Q&A cue card.

## Run it yourself

Python 3.10+. Each folder is self-contained.

```bash
# Digital twin + interactive dashboard (default preset: the 7×16 design)
cd 04-simulation
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run dashboard.py
.venv/bin/python -m pytest -q                 # 17 tests

# Reproduce every number on the 7×16 design sheet (~2 min)
cd ../07-constellation-optimization
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python design_detail.py 16
.venv/bin/python -m pytest -q                 # 21 tests

# Full optimisation (laptop, or MeluXina via sweep.slurm, see the folder README)
.venv/bin/python solve.py --help
```

## Tech and skills shown

- **Space systems modelling:** Walker constellations, orbital geometry, elevation masks, link budgets
  (FSPL, SNR, derated Shannon), ISL range and Earth blocking, Δv and propellant budgets, deorbit rules.
- **Networking:** 3GPP Rel-17/19 NTN, regenerative vs bent-pipe payloads, Dijkstra routing over a time-varying
  mesh, store-and-forward queues, policy-constrained (sovereign) routing.
- **Optimisation and HPC:** NSGA-II written from scratch in NumPy (non-dominated sorting, crowding, constraint
  handling), parallel evaluation with caching and resume, Slurm batch jobs on the MeluXina EuroHPC supercomputer.
- **Cloud-native / edge:** Kubernetes and KubeEdge (CloudCore/EdgeCore, edge autonomy, device twins, Sedna edge
  AI), canary rollouts and rollback, signed images and mTLS.
- **Software:** Python (NumPy, pandas, NetworkX, SciPy), Streamlit + Plotly dashboard, 49 pytest tests, static
  website (HTML/CSS/JS on Vercel), Node.js build scripts for the `.docx` proposal and `.pptx` deck.
- **Business and regulation:** TCO model, pricing and break-even, ITU filings, Luxembourg space law, GDPR,
  NIS2 / Cyber Resilience Act, IP and freedom-to-operate check.

## Repository layout

```
.
├── 00-challenge-brief/            Official OQ use-case brief (.docx original + .md conversion)
├── 01-research/                   Research pack. Start with 00-START-HERE.md
├── 02-brand/lynq-brand-kit/       Logos, favicons, CSS tokens, BRAND-GUIDE.md
├── 03-proposal/
│   ├── current/                   Phase 1 proposal as submitted (.pdf, .docx, .md, .html) + build script
│   ├── working-notes/             Condensing to 2 pages; fleet 10 → 30 update
│   └── history/                   Every earlier proposal version, oldest first
├── 04-simulation/                 NTN-Pulse digital twin, policy engine, fleet ops model, Streamlit dashboard
├── 05-global-coverage/            Whole-Earth coverage and latency study, satellite count left free
├── 06-leo-constellations/         Market report: who runs LEO constellations today
├── 07-constellation-optimization/ NSGA-II cost / latency / coverage optimiser, MeluXina job, 7×16 design sheet
├── 08-final-pitch/                ★ Final pitch deck (PDF), slide text, script, Q&A cue card
└── website/                       Static one-page site (Vercel)
```

## Team

| Name | Role |
|---|---|
| Davoud Jokar | Systems and digital twin |
| Ines Bouissou | NTN modelling and constellation optimisation |
| Gambhir Sharma | Cloud, KubeEdge orchestration and deployment |
| Maryam Amini | TCO, pricing, regulation and first-buyer case |

Partners: OQ Technology (challenge company), MeluXina / LuxProvide (HPC), KubeEdge / CNCF community,
Università di Roma Tor Vergata.

## Limits and honesty notes

- All results are **simulation** (TRL 3), not flight data. The models use circular orbits with no J2 or drag,
  no traffic load in the global study, and fixed gateways. Every assumption lives in a `config.py` or
  `costmodel.py` and can be changed and re-run.
- Costs are parametric. Trust the **ranking** of designs more than the absolute euros.
- The challenge brief in `00-challenge-brief/` and the OQ ONE notes in `01-research/` belong to OQ Technology and
  NEOSPACE. They are included only for reference.
- Some older notes in `03-proposal/history/` and `working-notes/` still use paths from before the repo was
  reorganised.
