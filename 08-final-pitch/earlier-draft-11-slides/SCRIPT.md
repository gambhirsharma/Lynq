# Lynq NTN-Pulse: 10-minute pitch script

> **Superseded.** This is the earlier 11-slide pitch for the North Sea (~12 → 30 satellite) design from the Phase 1
> proposal. The deck shown at the event is [`../Lynq-NTN-Pulse-final-pitch.pdf`](../Lynq-NTN-Pulse-final-pitch.pdf).

Deck: `lynq-ntn-pulse-pitch.pptx` (11 slides). The same text is in each slide's speaker notes.
Length: ~1384 words, about 10 minutes at ~140 words per minute. Timings are cumulative. Numbers come from `03-proposal/current/final.md` and `04-simulation/README.md`.

| # | Slide | Time |
|---|---|---|
| 1 | Title | 0:00–0:30 |
| 2 | The problem | 0:30–1:30 |
| 3 | Our answer | 1:30–2:40 |
| 4 | Technical: architecture | 2:40–3:50 |
| 5 | Technical: latency | 3:50–5:00 |
| 6 | Technical: coverage | 5:00–6:00 |
| 7 | Regulatory pathway | 6:00–7:15 |
| 8 | Business case | 7:15–8:30 |
| 9 | Benchmark | 8:30–9:15 |
| 10 | Risks and next steps | 9:15–9:45 |
| 11 | Closing | 9:45–10:00 |

## 1. Title  `0:00–0:30`

Good morning. We are Team Lynq, pronounced "link". OQ asked for a gNB-onboard LEO constellation that can serve any point on Earth, and for three things: an architecture sized to a coverage and latency target, a regulatory pathway, and a first business case.

Our answer is Lynq NTN-Pulse: a digital twin and policy engine that sits on top of OQ's regenerative satellites and decides, for every single message, which path it should take. Our tagline says it: every signal, the right path.

In the next ten minutes: the problem, our architecture, latency and coverage numbers from our simulation, the regulatory pathway, the business case, and what we want to do next.

## 2. The problem  `0:30–1:30`

Today most satellite IoT is bent-pipe. The satellite is a mirror: it only relays the signal down to a ground gateway. That creates three problems.

First, no gateway in view means no service. The terminal and a gateway must both see the same satellite at the same moment.

Second, a gateway can be in view but not allowed. National rules, data residency or licensing can forbid landing a given country's traffic there.

Third, all traffic is treated the same. A shutdown alarm queues behind a log file.

The people hit hardest are offshore operators: wind farms, platforms, vessels and pipelines in the North Sea, spread over five national sectors. That is our beachhead.

## 3. Our answer  `1:30–2:40`

Our answer is a software layer, NTN-Pulse. A digital twin models every satellite, gateway, link and queue; a policy engine assigns each message to a path.

Follow the cyan line. A platform sends a message to the gNB onboard the satellite overhead. The closest gateway is in view but blocked, for example a sector whose data may not land there. So instead of waiting, the satellite relays it over an RF link inside its plane, then an optical link across planes, down to an authorised gateway, and into the 5G core and cloud.

And because the gNB is onboard, the scheduler is in orbit too. Every message is sorted into three classes. Critical alarms go first, on the first authorised path, on this pass. Regular data like telemetry is stored onboard and forwarded within 90 minutes. Metadata tells the twin which gateway each asset may use.

## 4. Technical: architecture  `2:40–3:50`

The architecture. We start from OQ's real fleet, about 12 satellites today, ten OQ plus two ERMIS, and we size for the planned 30: three planes of ten at roughly 500 to 550 kilometres. At a 10-degree minimum elevation one footprint is about 3,000 kilometres wide, so one satellite in view covers the whole North Sea basin and every gateway around it.

The brief asked for two trade-offs.

Payload: we choose a full regenerative gNB. Bent-pipe cannot serve a user with no gateway in view, and a split gNB still keeps most of the RF power onboard while the RRC signalling round-trips to the ground. We keep power in check with a narrowband gNB and duty-cycling.

ISL: RF inside each plane, on every satellite, proven by Iridium for 25 years. Optical only across planes, on a subset of relay satellites: no spectrum licence, and European suppliers avoid ITAR. IoT needs only a few megabits, so all-optical isn't needed.

## 5. Technical: latency  `3:50–5:00`

Now the numbers. From our twin: 24 hours, 300 North Sea terminals, real orbits, link budgets and gateway rules.

With 30 satellites and all gateways up, a live alarm lands in the Frankfurt cloud in about 85 milliseconds, inside the continuous tier.

The chart is the interesting case. We take the Stavanger gateway offline. Norwegian-sector data is now only allowed to land at Svalbard. Bent-pipe and regenerative-without-ISL have to wait for a satellite that sees both the platform and Svalbard: the median alarm jumps to 30 to 35 seconds. With the ISL, the alarm simply relays north over the mesh and stays at about 100 milliseconds. Routing compliance was 100 percent in every scenario.

So the ISL is not just a speed feature. It is what makes sovereignty cheap.

## 6. Technical: coverage  `5:00–6:00`

Coverage. With today's 12 satellites the basin is in view only about a quarter of the day, with gaps up to four hours. That is passes, not coverage. Alarms wait for the next pass, about seven minutes.

At 30, the in-plane RF ring closes and coverage rises to 61 percent. But the worst gap is still almost two hours.

Our most useful finding: keep the same 30 satellites, but fly them in a 65-degree Walker delta instead of sun-synchronous planes. Sun-synchronous orbits spread passes over the poles; 65 degrees concentrates them at North Sea latitudes. Coverage goes to 79 percent, the worst gap drops from 118 minutes to 3, and 75 percent of alarms land under 250 milliseconds.

So for this market, orbit design is worth more than extra satellites. That is the kind of decision the twin exists to make.

## 7. Regulatory pathway  `6:00–7:15`

Regulation. The brief asks which authorities to engage first, and why.

One: Luxembourg, ILR and the Luxembourg Space Agency. OQ already holds a concession from November 2025; we extend it to ISL and regenerative operations.

Two: the ITU Radiocommunication Bureau, through Luxembourg, for priority filings: Article 9 coordination and the Article 22 EPFD limits that protect GSO systems.

Three: international waters. Offshore assets beyond territorial seas need no national landing rights, so this is where revenue can start earliest.

Four: the North Sea regulators and MNOs, UK, Norway, Denmark, the Netherlands and Germany, for coastal coverage. Five: EC and CEPT for spectrum.

The key idea is the bottom row. A regenerative gNB knows the user's identity, network and verified location. So we enforce data residency in the routing itself: each flow only lands at a gateway it is allowed to use, with local breakout, and the MNO keeps lawful intercept. In our twin, routing compliance was 100 percent in every scenario.

## 8. Business case  `7:15–8:30`

The business case. OQ asked for one viable segment first, not every segment at once.

Our first buyer is a European offshore energy operator or wind O&M provider, think Equinor, Ørsted or Eni. They have a real, expensive pain: blind spots, missed alarms, and dependence on VSAT and fixed gateways. They work in international waters and care about European sovereignty.

The unit economics. Running the North Sea network, including replacing satellites, costs about 9 million euros a year. We break even at about 75,000 offshore assets paying 120 euros a year, or at about 9,000 sovereign or defence endpoints at a thousand euros or more.

We price per asset, never per byte. At two to three euros per megabyte, byte pricing would kill adoption. Revenue comes from integration fees, per-asset subscriptions by traffic class, a usage charge for the priority tier, and MNO wholesale roaming along the coast.

## 9. Benchmark  `8:30–9:15`

OQ asked us to benchmark against three families: bent-pipe NTN IoT, GEO NTN IoT, and regenerative direct-to-cell.

Sateliot is the closest analogue: wholesale to MNOs, store-and-forward, but still Rel-17 bent-pipe. Skylo owns no satellites and runs over GEO: about 240 milliseconds round trip and no polar coverage. Starlink and AST have already built the mesh this challenge describes, at a scale and capital level nobody here can match.

We are not trying to out-build any of them. We out-position them: European sovereignty, data residency enforced in routing, and open 3GPP standards, for offshore and institutional buyers who will not route their traffic through US networks.

## 10. Risks and next steps  `9:15–9:45`

The risks are honest ones. The final payload limits may differ, so our policies are payload-independent and fall back to the ground. ISL and spectrum choices may change, so the twin simulates both and treats regulation as a hard constraint. And customers may resist new terminals, so we start with one alarm use case and a paid pilot with real SLA targets.

Next steps: in this Phase 2 we demo the live twin. Then we validate the 65-degree orbit with OQ's launch plan, and run a paid pilot with one North Sea operator. With the ISL, a software update reaches all 30 satellites in about an hour, versus 21 without.

## 11. Closing  `9:45–10:00`

To sum up: alarms reach the cloud in about 85 milliseconds, the right orbit cuts the worst North Sea gap to three minutes, and every flow lands only where it is allowed to. Every signal, the right path. Thank you, we're happy to take questions, and to show the live dashboard.

## Likely questions

- **Why not just use Starlink or Skylo?** US-controlled networks, no EU data residency; Skylo has ~240 ms GEO latency and no polar coverage.
- **Is the 65° Walker delta realistic for OQ?** It needs launches into dedicated planes instead of rideshare SSO slots. That trade is our first validation step with OQ's launch plan.
- **What does the simulation not model?** No J2/drag, uplink only, one fixed NB-IoT link budget (no beams, rain fade, Doppler residuals), optical ISL assumed always acquired, no cost model.
- **How do you handle lawful intercept?** Under MNO partnerships the MNO keeps it; flows land only at authorised gateways with local user-plane breakout.
- **Where does the €9M/yr come from?** North Sea network opex including ~6 satellite replacements a year; see `01-research/06-BUSINESS-CASE.md`.
