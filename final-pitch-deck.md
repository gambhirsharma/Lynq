# Lynq NTN-Pulse: pitch deck

Format: 10-minute pitch + 10-minute Q&A. Slides 01–14 at about 45 s each.
Footer on every content slide: `Lynq · NTN-Pulse · NN`

Structure per slide: `## Slide NN: Title`, then `### On slide`, then `### Speaker notes`, then `### Script` (word-for-word, with timing and speaker; slides 00–15 only). Full script and Q&A cue card: `final-pitch-script.md`.
Items still in [brackets] are open placeholders.

---

## Slide 00: Title

### On slide
- NEOSPACE CHALLENGE 2026 · NEXT-GEN DOWNSTREAM
- **Lynq NTN-Pulse**
- *Every signal, the right path.*
- A 112-satellite polar 5G constellation and the cloud-to-edge software that runs it: every alarm anywhere on Earth in under 100 ms, with satellites, gateways and AI-enabled IoT devices updated from one place.
- Team **Lynq** · Challenge: **OQ Technology: AnyPoint-NTN**
- Davoud Jokar · Ines Bouissou · Gambhir Sharma · Maryam Amini
- Università degli Studi di Roma Tor Vergata · [other universities]

### Speaker notes
"We are Lynq. We designed the constellation OQ needs for global 5G IoT, and we built the software to operate it: routing, orchestration and edge AI."

### Script (0:00–0:25 · Davoud)
Good morning. We are Lynq, and we took on OQ Technology's AnyPoint-NTN challenge.

Our proposal is **a 112-satellite polar 5G constellation**, and the software that runs it. With it, any alarm, from anywhere on Earth, reaches the cloud in **under 100 milliseconds**. And every satellite, gateway and device can be updated from one place.

**[Click]**

---

## Slide 01: The Problem

### On slide
- **Today's satellite IoT is neither global nor easy to run.**
- **Who has it:** Offshore energy, vessels, pipelines and remote infrastructure are hit hardest.
- **Operations:** A regenerative network is a distributed computer: a gNB on every satellite, dozens of gateways, hundreds of thousands of devices. Links come and go every few minutes. Updating software or AI models by hand does not scale.
- **Big number: 112 satellites**
  - **Coverage:** truly global 5G IoT takes 112 satellites in 7 polar planes, the cheapest design that covers 100% of Earth every minute with alarms under 100 ms (p99). That is the network we propose.
  - Over open ocean no gateway is in reach. Without inter-satellite links, those places stay dark however many satellites fly.
- *Source: Lynq constellation optimisation, NSGA-II over 3,064 designs, confirmed at 24 h, 2,000 points (07-constellation-optimization)*

### Speaker notes
"Two problems: global coverage takes a 112-satellite network with crosslinks, and once it exists, it is too complex to run by hand."

### Script (0:25–1:05 · Davoud)
Satellite IoT today has two problems.

First, it is not global. Offshore energy, shipping, pipelines: the assets that need it most sit where there is no ground station in reach. To cover the whole planet, every minute, with fast alarms, you need **112 satellites** in seven polar planes, linked to each other. That is the network we propose. Without those crosslinks, the open ocean stays dark no matter how many satellites you fly.

Second, it is hard to run. A regenerative network is a distributed computer: a base station on every satellite, dozens of gateways, hundreds of thousands of devices, and links that come and go every few minutes. You cannot update that by hand.

**[Click]**

---

## Slide 02: Market and Customers

### On slide
| Card | Big number | Detail |
|---|---|---|
| Total market | **$2.3–3.1B** | Satellite IoT in 2026, growing **14–23%/yr**. Commercial research houses; see References |
| Market you can reach | **~290k** | Global network breaks even at **~290k assets × €120/yr**, or **~35k sovereign endpoints × €1,000+/yr**. ≈ €35M/yr average 10-year TCO |
| First customers | **2 layers** | **OQ Technology:** buys the constellation design, NTN-Pulse, KubeEdge orchestration and support. **OQ's end customers:** offshore energy and maritime first (e.g. Equinor, Ørsted, Eni), then defence/sovereign |

- **Alternatives today:** VSAT, Iridium, Sateliot / Skylo, in-house ops tools. **Main limit:** no global low-latency coverage, no data-residency control, slow manual operations

### Speaker notes
"Lynq sells to OQ, and OQ sells to offshore operators. Our platform makes OQ's network both global and easy to run."

### Script (1:05–1:40 · Davoud)
Satellite IoT is a **$2.3 to 3.1 billion** market this year, growing 14 to 23% a year.

Our customer is OQ Technology: it buys the constellation design, NTN-Pulse, orchestration and support. OQ's customers are offshore energy and maritime first, operators like Equinor, Ørsted and Eni, then defence and sovereign users.

The global network breaks even at about **290,000 assets** at OQ's €120 a year, or 35,000 sovereign endpoints at €1,000.

**[Click]**

---

## Slide 03: Value and Revenue

### On slide
**Why customers choose us**
1. **Global alarms in <100 ms (p99)**, with no dark oceans
2. **Updates in minutes, not missions:** gNB, policies and AI models rolled out from one control plane
3. **AI at the edge:** devices send insight, not raw data, which suits a narrowband network and lowers cost per asset

**How we make money**

| Who pays | For what | Price model |
|---|---|---|
| OQ Technology | NTN-Pulse + KubeEdge platform licence | Per satellite / gateway node per year |
| OQ Technology | Software support, updates, SRE | Annual support contract |
| OQ / device makers | AI-enabled device agent + model updates | Per device per year |
| End customers (via OQ) | Priority asset monitoring | €120/asset/yr (OQ's tariff) |

- **Offer:** *"We sell OQ a cloud-to-edge platform and support to run its 112-satellite network, licensed per node and per AI-enabled device."*

### Speaker notes
"Per bit, satellite can never compete. Per alarm delivered, and per update shipped safely, it is the only option."

### Script (1:40–2:15 · Davoud)
Customers choose us for three things: **global alarms under 100 ms**, with no dark oceans; **updates in minutes, not missions**; and **AI at the edge**, so devices send insight, not raw data.

We license the platform to OQ per satellite and gateway node per year, sell a support contract, and charge per AI-enabled device.

Per bit, satellite can never compete. Per alarm delivered, and per update shipped safely, it is the only option.

*Handover:* Gambhir will show you how we build it.

**[Click]**

---

## Slide 04: Our Solution

### On slide
- **A complete, operable global NTN:** the constellation, the routing brain and the orchestration layer, delivered with software support for OQ.

| Card | Text |
|---|---|
| 7×16 polar constellation | 112 satellites at 700 km, Ka-band RF crosslinks. **100% of Earth, every minute, alarm p99 98 ms.** |
| NTN-Pulse policy engine + digital twin | Picks the path for every message: deliver now, relay over ISL, or store and forward. Lands data only at allowed gateways. |
| KubeEdge orchestration | One control plane from cloud → gateways → satellites → devices. Push updates in minutes, and nodes keep running when the link drops. |
| AI-enabled IoT devices | Models run on the terminal and on satellites, so they send only the alarms and summaries that matter. |

### Speaker notes
"Four parts, one system. The constellation gives coverage, the policy engine gives the right path, and KubeEdge lets OQ run and update all of it quickly."

### Script (2:15–2:55 · Gambhir)
We built a complete, operable global network, in four parts.

**The constellation:** seven planes of sixteen, at 700 kilometres, with Ka-band radio crosslinks. 100% of Earth, every minute, 99% of alarms in 98 milliseconds.

**The NTN-Pulse policy engine and digital twin:** it picks the path for every message, and only lands data at gateways where it is allowed.

**KubeEdge orchestration:** one control plane from the cloud down to each satellite and device.

And **AI-enabled devices** that send only what matters.

**[Click]**

---

## Slide 05: How It Works

### On slide
1. **Sense:** An AI-enabled device detects an anomaly locally, e.g. vibration or a pressure spike, and sends a 200-byte alarm instead of raw data.
2. **Decide:** The onboard gNB classes it as **critical**. The policy engine picks the fastest **allowed** path.
3. **Route:** It hops over RF crosslinks to a satellite above an authorised gateway, then to the 5G Core and cloud: **~72 ms typical**.
4. **Update:** Operators push a new model, policy or gNB patch through KubeEdge. It rolls out canary-first, plane by plane, during contact windows.

- **Service tiers:** Critical **<100 ms (p99)** worldwide · Regular telemetry by store-and-forward **≤90 min**
- **In scope:** Global LEO service, uplink IoT and alarms, satellite + gateway + device software lifecycle
- **Out of scope:** Broadband to phones (a different satellite class), and the downlink path (it mirrors the uplink graph)

### Speaker notes
"The device decides what matters, the satellite decides where it goes, and KubeEdge keeps every piece current."

### Script (2:55–3:35 · Gambhir)
Here is one alarm, end to end.

**Sense:** a sensor on an offshore platform detects a pressure spike. Its local AI model sends a 200-byte alarm, not raw data.

**Decide:** the base station on the satellite marks it critical. The policy engine picks the fastest allowed path.

**Route:** it hops over crosslinks to a satellite above an authorised gateway, then into the 5G core. About **72 milliseconds**.

**Update:** when we ship a new model or patch, it rolls out canary-first, plane by plane, during contact windows.

Critical alarms under 100 ms worldwide; routine telemetry by store-and-forward.

**[Click]**

---

## Slide 06: Technical Architecture

### On slide
Layered diagram (top to bottom):

| Layer | Contents | Link to next layer |
|---|---|---|
| CLOUD | KubeEdge CloudCore · NTN-Pulse twin + policy engine · AI model registry · dashboard | Kubernetes API, policies, images, models |
| GROUND | 28 gateways (EdgeCore) · 5G Core · local user-plane breakout | Feeder links |
| SPACE | 112 satellites (EdgeCore) · regenerative NB-IoT gNB · onboard policy + AI | Ka-band RF crosslinks: fore/aft in-plane, left/right cross-plane |
| DEVICES | AI-enabled IoT terminals (KubeEdge device twin / mappers) · standard 3GPP chips | |

**Key subsystems**
- **Space segment:** 7 planes × 16, 700 km, 87° Walker star. 16U, 30 kg, 100 W. gNB + 4 RF crosslink terminals
- **Ground segment:** 28 gateways worldwide, 5G Core, sovereign local breakout
- **Software platform:** KubeEdge: CloudCore in the cloud, EdgeCore on gateways and satellites. Edge AI with KubeEdge Sedna

**What is new:** A satellite is managed like a cloud node. Policies, gNB software and AI models ship as containers. Edge autonomy keeps every satellite serving through link outages and syncs it when contact returns.

### Speaker notes
"Kubernetes was built for data centres. KubeEdge extends it to nodes that disconnect, which is exactly what a satellite is."

### Script (3:35–4:20 · Gambhir)
Four layers. In the cloud: KubeEdge CloudCore, our twin and policy engine, and the AI model registry. On the ground: 28 gateways and the 5G core, with local breakout. In space: 112 satellites, each with a regenerative NB-IoT base station and four radio crosslinks. At the bottom: standard 3GPP devices.

What is new is this: **we manage a satellite like a cloud node.** Policies, base-station software and AI models ship as containers. Kubernetes was built for data centres. KubeEdge extends it to nodes that disconnect, which is exactly what a satellite does. When the link drops, the satellite keeps serving; when contact returns, it syncs.

*Handover:* Ines will show you that it works, and what comes next.

**[Click]**

---

## Slide 07: Feasibility and Maturity

### On slide
- TRL bar: 1–3 filled, 4–5 outlined, 6–9 dim
- **TRL today: 3** (proof of concept in simulation) · **Target: TRL 5 by Q4 2027**

**Already done · proves TRL 3 today**
- **Global optimiser:** NSGA-II over 3,064 designs on MeluXina. 7×16 is the cheapest design with 100% coverage and p99 <100 ms
- **Re-simulated design:** 24 h at 60 s steps over 2,000 points. Coverage 100%, p50 72 ms, p99 98 ms, survives a failed gateway with no loss
- **Policy engine in the North Sea twin:** with a gateway offline, alarms stay at ~100 ms over the ISL mesh (vs 30–35 s without it). 100% routing compliance
- **Reference systems:** Iridium (66-sat RF crosslink mesh since the 1990s), KubeEdge (CNCF graduated), 3GPP Rel-17/19 NTN

**Planned · to reach TRL 5**
- **KubeEdge testbed:** CloudCore + EdgeCore on flight-like boards, with simulated link outages
- **Hardware-in-the-loop** with OQ's 5G Satellite Test Lab (Leudelange)
- **AI-enabled terminal pilot** with one offshore operator

*Details in the R&D roadmap →*

### Speaker notes
"The constellation and routing are proven in simulation, and every number is reproducible from our repo. The orchestration layer is built on a mature open-source project. Next comes the testbed."

### Script (4:20–5:05 · Ines)
We are at **TRL 3** today, proof of concept in simulation, with every number reproducible from our repository.

We searched over **3,064 designs** on the MeluXina supercomputer. Seven by sixteen is the cheapest one with full coverage and p99 under 100 ms. We re-simulated it for 24 hours over 2,000 points worldwide: 100% coverage, 72 ms typical, 98 ms worst-case, and no loss when a gateway fails.

In our North Sea twin, with a gateway offline, alarms still arrive in about 100 milliseconds over the crosslinks, against 30 to 35 seconds without them.

Next: a KubeEdge testbed and hardware-in-the-loop at OQ's lab, to reach **TRL 5 by end of 2027**.

**[Click]**

---

## Slide 08: Prior Art (IP) and Benchmark

### On slide
| Criterion | Lynq on OQ (7×16) | Sateliot | Starlink D2C | Iridium |
|---|---|---|---|---|
| Architecture | Regenerative gNB, RF mesh, KubeEdge-managed | Rel-17 NB-IoT, bent-pipe + S&F | Broadband D2C, laser mesh | Proprietary, RF mesh |
| Alarm latency | **p99 98 ms, 100% Earth** | Minutes (store-and-forward) | ~25–60 ms (broadband) | Global, not published |
| Cost | **€134M capex** (€0.83M/sat), €348M / 10 yrs | Not disclosed | Billions, ~11,100 sats | High, 66 sats |
| Maturity (TRL) | 3 (design + software) | 9 | 9 | 9 |
| Operability | Cloud-native updates, standard 3GPP chips | Standard 3GPP | Own ecosystem | Own terminals |
| Edge AI on devices | **Yes, orchestrated** | No | No | No |
| IP position | Own know-how on open source (Apache-2.0) | Patented S&F roaming | Proprietary | Proprietary |

- **Key patents:** OQ holds 12 patents (2018 priority) plus a **pending ISL patent for cellular constellations**. Sateliot holds a patent on S&F roaming. We differ by doing **policy routing and orchestration on top** of the link, not the link itself.
- **Freedom to operate:** **To check.** KubeEdge is Apache-2.0. Our policy engine, satellite operators and edge-AI models are our own know-how.
- *Sources: USPTO grants to OQ (SpaceNews; SpaceWatch.Global, Dec 2022), Espacenet, company websites. See References.*

### Speaker notes
"We don't try to out-build Starlink. We win on sovereignty, open standards, operability and cost per alarm."

### Script (5:05–5:45 · Ines)
How do we compare? Sateliot uses store-and-forward: alarms take minutes. Starlink direct-to-cell is fast, but runs on thousands of satellites and billions in capital. Iridium proved the radio-crosslink mesh decades ago, on proprietary terminals.

We deliver **global alarms in 98 ms, on standard 3GPP chips, for €134 million capex**, with orchestrated edge AI nobody else offers.

On IP: OQ holds its own patents, including a pending crosslink patent. We don't compete on the link. We add **policy routing and orchestration on top**, built on Apache-licensed open source.

**[Click]**

---

## Slide 09: R&D Roadmap

### On slide
| # | Date | Milestone | TRL | Validation (test + success criterion) |
|---|---|---|---|---|
| 1 | Oct 2026 | 7×16 design + policy engine in twin (done) | 2 → 3 | 100% coverage, p99 <100 ms, 100% routing compliance in simulation |
| 2 | Q2 2027 | KubeEdge testbed: cloud + gateway + satellite boards | 3 → 4 | Update reaches all nodes with simulated outages. Nodes keep serving offline. Failed canary rolls back automatically |
| 3 | Q4 2027 | HIL at OQ's 5G Test Lab + first AI-enabled terminal | 4 → 5 | Correct priority/path in ≥99% of cases. Device model updated over the air |
| 4 | 2028 | Pilot on OQ's fleet with an offshore operator | 5 → 6 | ≥95% of alarms delivered on tier over 3 months, zero non-compliant landings |

- **Facilities and partners needed:** OQ 5G Satellite Test Lab (Leudelange), MeluXina HPC, OQ fleet access, one offshore operator

### Speaker notes
"Each step has a test and a pass criterion, and each one is fundable on its own."

### Script (5:45–6:25 · Ines)
Four milestones, each with a test and a pass criterion.

**Now:** the design and policy engine work in simulation. Done.

**Q2 2027:** a KubeEdge testbed on flight-like boards. An update must reach every node through simulated outages, and a failed canary must roll back on its own.

**Q4 2027:** hardware-in-the-loop at OQ's 5G Test Lab in Leudelange, plus the first AI-enabled terminal. Correct path in 99% of cases. **TRL 5.**

**2028:** a pilot on OQ's fleet with an offshore operator. 95% of alarms on tier, zero non-compliant landings.

**[Click]**

---

## Slide 10: Team, Partners and Risks

### On slide
| Name | Role · study field |
|---|---|
| Davoud Jokar | Systems and digital twin · [study field] |
| Ines Bouissou | NTN modelling and constellation optimisation · [study field] |
| Gambhir Sharma | Cloud, KubeEdge orchestration and deployment · ICT & Internet Eng. / MSc Telecom Eng. |
| Maryam Amini | TCO, pricing, regulation and first-buyer case · [study field] |

- **Key partners:** OQ Technology (challenge company), MeluXina / LuxProvide (HPC), KubeEdge / CNCF community, Università di Roma Tor Vergata

**Main risks**

| Risk | Mitigation |
|---|---|
| **Technical:** RF crosslinks have only 0.58 dB margin. A single satellite failure opens 4-min gaps. Onboard compute is tight (40 W payload) | Design for +3 dB per link. Fly 1 in-orbit spare per plane (7 sats, ~€7M). Lightweight EdgeCore, staged updates only in contact windows |
| **Regulatory/market:** concession not yet extended to ISL. Security certification (NIS2/CRA) | Luxembourg first. Signed images, audit logs and a security review built in from the start |
| **Delivery/funding:** launch cost per plane (dedicated launch raises 10-yr cost by ~50%) | Rideshare + transfer vehicles. The design ranking holds under that sensitivity |

### Speaker notes
"We named our weakest points ourselves: radio margin, single-satellite gaps and onboard compute. Each one has a fix."

### Script (6:25–7:15 · Ines)
We are four: Davoud on systems and the digital twin, Ines on constellation optimisation, Gambhir on cloud and KubeEdge, and Maryam on cost, pricing and regulation. Our partners are OQ, LuxProvide's MeluXina, the KubeEdge community and Tor Vergata.

We named our weakest points ourselves.

**Radio margin** is thin, under 1 dB, so we design for plus 3 dB per link.

**One satellite failure** opens a four-minute gap, so we fly one spare per plane: seven satellites, about €7 million.

**Onboard compute** is tight, so we run a lightweight EdgeCore and update only in contact windows.

And launch cost: we use rideshare and transfer vehicles. The design still wins if launch costs rise.

*Handover:* Maryam will take us through regulation, costs and our ask.

**[Click]**

---

## Slide 11: Regulation and Standards

### On slide
| Requirement | Source | How we comply | Status |
|---|---|---|---|
| Debris mitigation | IADC guidelines, 5-year deorbit trend | At 700 km natural decay is too slow, so a deorbit burn is budgeted (Δv 207 m/s, electric propulsion) | Planned |
| Spectrum use | ITU RR Art. 9 coordination, Art. 22 EPFD | OQ's priority ITU filings via Luxembourg. €1M budgeted for the Ka-band crosslink filing | In progress |
| Operation licence | Luxembourg space law (2020), ILR/LSA | Extend OQ's Nov-2025 concession to ISL + regenerative ops | **Open** |
| Data residency + lawful intercept | GDPR, national LI rules | Onboard policy routing, local breakout, the MNO keeps LI. 100% compliance in simulation | Done (sim) |
| Cybersecurity | NIS2 (space is a critical sector), Cyber Resilience Act (IoT devices) | Signed container images, mTLS between CloudCore and EdgeCore, audited rollouts, device update path | Planned |
| Export control | EU dual-use, ITAR/EAR | European crosslink suppliers, no US-origin parts | Planned |

- **Sovereignty and security are built into the software:** routing rules and signed updates are enforced by the platform. **Open point:** extending OQ's Luxembourg concession to ISL and regenerative operations, our first regulatory step.
- **Engagement order:** Luxembourg ILR/LSA → ITU BR → international waters (no landing rights) → MNO partner countries → EC/CEPT spectrum

### Speaker notes
"The same orchestration that gives speed also gives an audit trail: who changed what, on which satellite, and when."

### Script (7:15–7:55 · Maryam)
Regulation is built into the design. Debris: we budget a deorbit burn, because 700 km decays too slowly. Spectrum: we build on OQ's priority ITU filings through Luxembourg. Data residency and lawful intercept: the onboard policy only lands data where allowed. 100% compliance in simulation. Cybersecurity under NIS2 and the Cyber Resilience Act: signed images, mutual TLS, audited rollouts.

Our one open point is **extending OQ's Luxembourg concession to crosslinks and regenerative operation.** That is our first regulatory step.

The same orchestration that gives speed gives an audit trail: who changed what, on which satellite, and when.

**[Click]**

---

## Slide 12: Costs and Economics

### On slide
**Costs and assumptions**
- **Network (OQ side):** €134.2M capex · €348.2M over 10 years (satellites ×2 generations €185.9M, launch + transfer vehicles €82.5M, 28 gateways €36.4M, ops €43.4M)
- **Lynq side, main costs:** engineering team, cloud and testbed hardware, security certification
- **Key assumptions:** €10k per node/yr licence · support contract · €2 per AI device/yr

**Economics**

| Lynq | Year 1 | Year 2 | Year 3 |
|---|---:|---:|---:|
| Revenue (€) | 0.3M (pilot + integration) | 1.2M (licence for 112 sats + support) | 2.5M (+ AI devices) |
| Costs (€) | 0.6M | 1.0M | 1.6M |
| Result (€) | −0.3M | +0.2M | +0.9M |

- The software layer is **~3–7%** of the network's 10-year cost (€12–25M), but it decides how fast OQ can operate and earn.

### Speaker notes
"OQ spends €348 million on the network. We make every euro of it easier to operate, for a few percent of that."

### Script (7:55–8:35 · Maryam)
On OQ's side, the 112-satellite network costs **€134 million to build and launch**, and €348 million over ten years, including a second satellite generation, 28 gateways and operations.

Lynq's costs are engineering, cloud and testbed hardware, and security certification. We run at a loss in year one with pilot revenue, turn a small profit of €0.2 million in year two once the licence covers all 112 satellites, and reach **€0.9 million** profit in year three with AI devices.

Our software is 3 to 7% of the network's ten-year cost. But it decides how fast OQ can operate and earn.

**[Click]**

---

## Slide 13: Funding Request and Use

### On slide
- **Funding needed:** **€450k**
- **Goal:** reach TRL 5 in 12 months
- **Use of funds:**
  - R&D (KubeEdge satellite operators, policy engine, edge AI) **45%**
  - Testing (testbed, HIL) **25%**
  - Team **25%**
  - Other (cloud, security audit, IP) **5%**
- **Funding routes:** ESA OSIP · ESRIC Startup Support Programme · Luxembourg national grants · Paid software contract with OQ

### Speaker notes
"With this, the platform leaves simulation and runs on flight-like hardware with OQ."

### Script (8:35–9:05 · Maryam)
We are asking for **€450,000** to reach TRL 5 in twelve months.

45% goes to R&D: satellite operators for KubeEdge, the policy engine, edge AI. 25% to testing and hardware-in-the-loop. 25% to the team. 5% to cloud, security audit and IP.

We will pursue ESA OSIP, ESRIC's startup programme, Luxembourg grants, and a paid software contract with OQ.

**[Click]**

---

## Slide 14: Next Steps

### On slide
- **What we need next:** A KubeEdge testbed and HIL slot at OQ's 5G Satellite Test Lab, at €450k to reach TRL 5
- **Partner we are looking for:** OQ as software customer, plus one offshore operator for an AI-enabled terminal pilot
- **Test facility or data:** OQ gNB payload interface, flight-like onboard computer, fleet telemetry, continued MeluXina access
- **Mentoring:** ITU filing for Ka-band crosslinks, NIS2/CRA security certification, MNO roaming
- **Since the start of the challenge:** [feedback from OQ/mentors]. **Changes we made:** moved from a North Sea 30-satellite fleet to a **global 7×16 polar design** chosen by optimisation, and added **KubeEdge orchestration and edge AI** so OQ can run and update the network quickly.

### Speaker notes
"Give us a testbed and one pilot, and in twelve months OQ operates its satellites like a cloud."

### Script (9:05–9:45 · Maryam)
What we need next: a **KubeEdge testbed and a hardware-in-the-loop slot at OQ's lab**, at €450,000. OQ as our software customer, and one offshore operator for a terminal pilot. Mentoring on the crosslink ITU filing, NIS2 certification and MNO roaming.

Since the start of the challenge, we moved from a 30-satellite North Sea fleet to a **global 112-satellite polar design chosen by optimisation**, and added orchestration and edge AI so OQ can run it.

Give us a testbed and one pilot, and in twelve months **OQ operates its satellites like a cloud.**

**[Click]**

---

## Slide 15: Thank You

### On slide
- THANK YOU
- QUESTIONS ARE WELCOME
- **Lynq · NTN-Pulse:** *Every signal, the right path.*
- hey@gambhir.dev · gambhir.dev · [LinkedIn]

### Speaker notes
Leave this slide on screen during the 10-minute Q&A. Use the backup slides to answer detailed questions.

### Script (9:45–10:00 · Maryam)
Thank you. Lynq, NTN-Pulse: every signal, the right path. We're happy to take your questions.

*(Leave this slide up for Q&A.)*

---

## Slide 16: Backup Slides (divider)

### On slide
- FOR THE Q&A
- **BACKUP SLIDES**
- A · 7×16 polar design · B · KubeEdge orchestration layer · C · Cost per design alternative · References and sources. Full regulatory analysis: 01-research/05-REGULATORY-deep-dive.md. Show these only when the jury asks.

### Speaker notes
Show only if the jury asks.

---

## Slide 17: Backup A: 7×16 Polar Design

### On slide
| Figure | Value |
|---|---|
| Orbit | 7 planes × 16 = 112 sats, 700 km, 87°, Walker star, period 98.6 min |
| Coverage | 100% of Earth, every minute, longest gap 0 min. 2.58 satellites in view on average |
| Alarm latency p50 / p95 / p99 | 72 / 91 / 98 ms |
| Crosslinks | Ka-band RF, 4 per satellite, ~1 Mbps, 186 of 208 links up on average |
| Satellite | 16U, 30.1 kg, 100 W, €0.83M |
| Capex / 10-yr TCO | €134.2M / €348.2M |
| 1 satellite fails | 99.84% coverage, 4-min gap, p99 ~99 ms |
| Svalbard gateway down | No change (100%, p99 98 ms) |

- **Why RF and not laser:** RF is cheaper at every laser price tested (down to €0.02M/terminal). A laser 6×20 design costs **€125M more** for the same service.

### Speaker notes
Backup: show only if the jury asks.

---

## Slide 18: Backup B: KubeEdge Orchestration Layer

### On slide
| Layer | Component | Job |
|---|---|---|
| Cloud | CloudCore + Kubernetes API | Desired state for every node. Image and model registry |
| Gateways | EdgeCore | Runs 5G Core functions, local breakout, gateway-side policy |
| Satellites | EdgeCore (lightweight) | gNB apps, onboard policy engine, onboard AI. **Edge autonomy:** keeps running when the feeder link drops |
| Devices | Device twin + mappers (MQTT, Modbus) | Device state, config and model updates for AI-enabled terminals |
| AI | KubeEdge Sedna | Joint cloud–edge inference, incremental and federated learning |

- **Rollout policy:** signed image → 1 canary satellite per plane → health check over the next pass → plane by plane → automatic rollback on failure. Large images ship as layer deltas during gateway contact, not over 1 Mbps crosslinks.

### Speaker notes
Backup: show only if the jury asks.

---

## Slide 19: Backup C: Cost per Design Alternative

### On slide
| Design | Sats | p99 | 10-yr cost |
|---|---:|---:|---:|
| 6×16 @ 800 km, in-plane RF only | 96 | 110 ms | €256M |
| 7×15 @ 700 km, RF in-plane + cross | 105 | 99.5 ms | €333M (1-min gaps, 0.02 dB margin) |
| **7×16 @ 700 km, RF in-plane + cross** | **112** | **98 ms** | **€348M** |
| 6×20 @ 800 km, laser | 120 | 99.7 ms | €473M |
| 17×18 @ 500 km, laser grid | 306 | 84.8 ms | €1,211M |

- **7×16** is the cheapest design with 100% coverage and p99 <100 ms.

### Speaker notes
Backup: show only if the jury asks.

---

## Slide 20: References and Sources

### On slide
1. Lynq, Constellation optimisation and 7×16 design sheet (07), Global coverage study (05), NTN-Pulse digital twin (04), 2026. github.com/gambhirsharma/Lynq
2. OQ Technology / NEOSPACE Europe, AnyPoint-NTN: Global gNB-Onboard LEO Constellation for Ubiquitous 5G NR-NTN, challenge brief, 2026
3. KubeEdge project documentation (kubeedge.io) and KubeEdge Sedna, CNCF [add access date]
4. Patents: USPTO grants to OQ Technology (SpaceNews; SpaceWatch.Global, Dec 2022); Sateliot S&F roaming patent. Search via Espacenet [add query + date]
5. Market: satellite IoT forecasts in 01-research/06-BUSINESS-CASE.md [name the publisher for the figure you quote]; LEO operator figures in 06-leo-constellations/README.md (as of 19 Oct 2026)
6. Regulation: ITU Radio Regulations Art. 9 and 22; Luxembourg Law on Space Activities (2020); OQ Luxembourg concession (SpaceWatch.Global, Nov 2025); IADC Space Debris Mitigation Guidelines; GDPR (EU 2016/679); NIS2 Directive (EU 2022/2555); Cyber Resilience Act (EU 2024/2847)

### Speaker notes
List every source quoted in the pitch, numbered as in the proposal.
