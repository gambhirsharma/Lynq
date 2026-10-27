# Lynq NTN-Pulse: final pitch script

Spoken script for `final-pitch-deck.md`. Target: 10 minutes for slides 00–14 (about 1,400 words at ~140 words/min).
Times are cumulative. **[Click]** marks a slide change. Bold words are the ones to land.

### Who speaks when

Split by expertise: **technical** (Gambhir, Ines) and **business and regulatory** (Davoud, Maryam).

| Speaker | Focus | Slides | Time |
|---|---|---|---|
| Block | Speaker | Story | Slides | Time |
|---|---|---|---|---|
| 1 | **Davoud** | Why it matters: problem, market, value | 00–03 | 0:00–2:15 |
| 2 | **Gambhir** | What we built: solution, alarm flow, KubeEdge architecture | 04–06 | 2:15–4:20 |
| 3 | **Ines** | Proof and path: simulation results, benchmark, roadmap, risks | 07–10 | 4:20–7:15 |
| 4 | **Maryam** | Making it real: regulation, costs, funding ask, next steps, close | 11–15 | 7:15–10:00 |

Each speaker has one continuous block, so there are only three handovers. Each one is marked *Handover:* in the script.

Why this way: business opens with the customer's problem and the money, and the technical middle explains how we deliver it and proves it works. Regulation and the funding ask close the pitch. To keep each block continuous, Market and Value move up to follow the Problem, and Roadmap and Risks follow Feasibility.

**Q&A owners:** constellation, crosslinks, failures → Ines · updates, KubeEdge, onboard compute → Gambhir · licence, ITU, NIS2 → Maryam · pricing, customers, market → Davoud.

---

## Slide 00: Title · 0:00–0:25 · **Davoud**

Good morning. We are Lynq, and we took on OQ Technology's AnyPoint-NTN challenge.

Our proposal is **a 112-satellite polar 5G constellation**, and the software that runs it. With it, any alarm, from anywhere on Earth, reaches the cloud in **under 100 milliseconds**. And every satellite, gateway and device can be updated from one place.

**[Click]**

## Slide 01: The Problem · 0:25–1:05 · **Davoud**

Satellite IoT today has two problems.

First, it is not global. Offshore energy, shipping, pipelines: the assets that need it most sit where there is no ground station in reach. To cover the whole planet, every minute, with fast alarms, you need **112 satellites** in seven polar planes, linked to each other. That is the network we propose. Without those crosslinks, the open ocean stays dark no matter how many satellites you fly.

Second, it is hard to run. A regenerative network is a distributed computer: a base station on every satellite, dozens of gateways, hundreds of thousands of devices, and links that come and go every few minutes. You cannot update that by hand.

**[Click]**

## Slide 02: Market and Customers · 1:05–1:40 · **Davoud**

Satellite IoT is a **$2.3 to 3.1 billion** market this year, growing 14 to 23% a year.

Our customer is OQ Technology: it buys the constellation design, NTN-Pulse, orchestration and support. OQ's customers are offshore energy and maritime first, operators like Equinor, Ørsted and Eni, then defence and sovereign users.

The global network breaks even at about **290,000 assets** at OQ's €120 a year, or 35,000 sovereign endpoints at €1,000.

**[Click]**

## Slide 03: Value and Revenue · 1:40–2:15 · **Davoud**

Customers choose us for three things: **global alarms under 100 ms**, with no dark oceans; **updates in minutes, not missions**; and **AI at the edge**, so devices send insight, not raw data.

We license the platform to OQ per satellite and gateway node per year, sell a support contract, and charge per AI-enabled device.

Per bit, satellite can never compete. Per alarm delivered, and per update shipped safely, it is the only option.

*Handover:* Gambhir will show you how we build it.

**[Click]**

## Slide 04: Our Solution · 2:15–2:55 · **Gambhir**

We built a complete, operable global network, in four parts.

**The constellation:** seven planes of sixteen, at 700 kilometres, with Ka-band radio crosslinks. 100% of Earth, every minute, 99% of alarms in 98 milliseconds.

**The NTN-Pulse policy engine and digital twin:** it picks the path for every message, and only lands data at gateways where it is allowed.

**KubeEdge orchestration:** one control plane from the cloud down to each satellite and device.

And **AI-enabled devices** that send only what matters.

**[Click]**

## Slide 05: How It Works · 2:55–3:35 · **Gambhir**

Here is one alarm, end to end.

**Sense:** a sensor on an offshore platform detects a pressure spike. Its local AI model sends a 200-byte alarm, not raw data.

**Decide:** the base station on the satellite marks it critical. The policy engine picks the fastest allowed path.

**Route:** it hops over crosslinks to a satellite above an authorised gateway, then into the 5G core. About **72 milliseconds**.

**Update:** when we ship a new model or patch, it rolls out canary-first, plane by plane, during contact windows.

Critical alarms under 100 ms worldwide; routine telemetry by store-and-forward.

**[Click]**

## Slide 06: Technical Architecture · 3:35–4:20 · **Gambhir**

Four layers. In the cloud: KubeEdge CloudCore, our twin and policy engine, and the AI model registry. On the ground: 28 gateways and the 5G core, with local breakout. In space: 112 satellites, each with a regenerative NB-IoT base station and four radio crosslinks. At the bottom: standard 3GPP devices.

What is new is this: **we manage a satellite like a cloud node.** Policies, base-station software and AI models ship as containers. Kubernetes was built for data centres. KubeEdge extends it to nodes that disconnect, which is exactly what a satellite does. When the link drops, the satellite keeps serving; when contact returns, it syncs.

*Handover:* Ines will show you that it works, and what comes next.

**[Click]**

## Slide 07: Feasibility and Maturity · 4:20–5:05 · **Ines**

We are at **TRL 3** today, proof of concept in simulation, with every number reproducible from our repository.

We searched over **3,064 designs** on the MeluXina supercomputer. Seven by sixteen is the cheapest one with full coverage and p99 under 100 ms. We re-simulated it for 24 hours over 2,000 points worldwide: 100% coverage, 72 ms typical, 98 ms worst-case, and no loss when a gateway fails.

In our North Sea twin, with a gateway offline, alarms still arrive in about 100 milliseconds over the crosslinks, against 30 to 35 seconds without them.

Next: a KubeEdge testbed and hardware-in-the-loop at OQ's lab, to reach **TRL 5 by end of 2027**.

**[Click]**

## Slide 08: Prior Art and Benchmark · 5:05–5:45 · **Ines**

How do we compare? Sateliot uses store-and-forward: alarms take minutes. Starlink direct-to-cell is fast, but runs on thousands of satellites and billions in capital. Iridium proved the radio-crosslink mesh decades ago, on proprietary terminals.

We deliver **global alarms in 98 ms, on standard 3GPP chips, for €134 million capex**, with orchestrated edge AI nobody else offers.

On IP: OQ holds its own patents, including a pending crosslink patent. We don't compete on the link. We add **policy routing and orchestration on top**, built on Apache-licensed open source.

**[Click]**

## Slide 09: R&D Roadmap · 5:45–6:25 · **Ines**

Four milestones, each with a test and a pass criterion.

**Now:** the design and policy engine work in simulation. Done.

**Q2 2027:** a KubeEdge testbed on flight-like boards. An update must reach every node through simulated outages, and a failed canary must roll back on its own.

**Q4 2027:** hardware-in-the-loop at OQ's 5G Test Lab in Leudelange, plus the first AI-enabled terminal. Correct path in 99% of cases. **TRL 5.**

**2028:** a pilot on OQ's fleet with an offshore operator. 95% of alarms on tier, zero non-compliant landings.

**[Click]**

## Slide 10: Team, Partners and Risks · 6:25–7:15 · **Ines**

We are four: Davoud on systems and the digital twin, Ines on constellation optimisation, Gambhir on cloud and KubeEdge, and Maryam on cost, pricing and regulation. Our partners are OQ, LuxProvide's MeluXina, the KubeEdge community and Tor Vergata.

We named our weakest points ourselves.

**Radio margin** is thin, under 1 dB, so we design for plus 3 dB per link.

**One satellite failure** opens a four-minute gap, so we fly one spare per plane: seven satellites, about €7 million.

**Onboard compute** is tight, so we run a lightweight EdgeCore and update only in contact windows.

And launch cost: we use rideshare and transfer vehicles. The design still wins if launch costs rise.

*Handover:* Maryam will take us through regulation, costs and our ask.

**[Click]**

## Slide 11: Regulation and Standards · 7:15–7:55 · **Maryam**

Regulation is built into the design. Debris: we budget a deorbit burn, because 700 km decays too slowly. Spectrum: we build on OQ's priority ITU filings through Luxembourg. Data residency and lawful intercept: the onboard policy only lands data where allowed. 100% compliance in simulation. Cybersecurity under NIS2 and the Cyber Resilience Act: signed images, mutual TLS, audited rollouts.

Our one open point is **extending OQ's Luxembourg concession to crosslinks and regenerative operation.** That is our first regulatory step.

The same orchestration that gives speed gives an audit trail: who changed what, on which satellite, and when.

**[Click]**

## Slide 12: Costs and Economics · 7:55–8:35 · **Maryam**

On OQ's side, the 112-satellite network costs **€134 million to build and launch**, and €348 million over ten years, including a second satellite generation, 28 gateways and operations.

Lynq's costs are engineering, cloud and testbed hardware, and security certification. We run at a loss in year one with pilot revenue, turn a small profit of €0.2 million in year two once the licence covers all 112 satellites, and reach **€0.9 million** profit in year three with AI devices.

Our software is 3 to 7% of the network's ten-year cost. But it decides how fast OQ can operate and earn.

**[Click]**

## Slide 13: Funding Request · 8:35–9:05 · **Maryam**

We are asking for **€450,000** to reach TRL 5 in twelve months.

45% goes to R&D: satellite operators for KubeEdge, the policy engine, edge AI. 25% to testing and hardware-in-the-loop. 25% to the team. 5% to cloud, security audit and IP.

We will pursue ESA OSIP, ESRIC's startup programme, Luxembourg grants, and a paid software contract with OQ.

**[Click]**

## Slide 14: Next Steps · 9:05–9:45 · **Maryam**

What we need next: a **KubeEdge testbed and a hardware-in-the-loop slot at OQ's lab**, at €450,000. OQ as our software customer, and one offshore operator for a terminal pilot. Mentoring on the crosslink ITU filing, NIS2 certification and MNO roaming.

Since the start of the challenge, we moved from a 30-satellite North Sea fleet to a **global 112-satellite polar design chosen by optimisation**, and added orchestration and edge AI so OQ can run it.

Give us a testbed and one pilot, and in twelve months **OQ operates its satellites like a cloud.**

**[Click]**

## Slide 15: Thank You · 9:45–10:00 · **Maryam**

Thank you. Lynq, NTN-Pulse: every signal, the right path. We're happy to take your questions.

*(Leave this slide up for Q&A.)*

---

## Q&A cue card

Short answers; go to the backup slide only if the jury wants detail.

| Likely question | Answer | Backup |
|---|---|---|
| Why 112 and not fewer? | 96 satellites at 800 km covers the Earth, but without cross-plane links p99 is 110 ms. 7×15 (105 sats) leaves 1-min gaps and has 0.02 dB link margin. 112 is the cheapest design that meets both targets with margin. | C |
| Why radio crosslinks, not laser? | Radio was cheaper at every laser price we tested, down to €0.02M per terminal. A laser 6×20 design costs €125M more for the same service. | A |
| What if a satellite fails? | Coverage drops to 99.84% with a 4-min gap and p99 ~99 ms. One in-orbit spare per plane closes it. | A |
| What if a gateway fails? | No change. Svalbard offline still gives 100% coverage and p99 98 ms; traffic reroutes over crosslinks. | A |
| How do you update a satellite safely? | Signed image → one canary per plane → health check over the next pass → plane by plane → automatic rollback. Large images go as layer deltas at gateway contact, not over 1 Mbps crosslinks. | B |
| Can the onboard computer run Kubernetes? | KubeEdge EdgeCore is lightweight and built for constrained, disconnected nodes; we validate it on flight-like boards in milestone 2. | B |
| Is the licence in place? | Not yet for crosslinks and regenerative ops. Extending OQ's Luxembourg concession is our first regulatory step. | – |
| Where do the numbers come from? | All constellation numbers are reproducible: `07-constellation-optimization/design_detail.py 16` and `results/report.md`. | References |
