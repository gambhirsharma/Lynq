# 03 — The Challenge, Decoded

## 1. What the brief literally asks

Three "Expected Outcomes", in OQ's order of interest:

1. **Constellation architecture** — satellite count, orbital shell(s), ISL topology, *sized to a stated coverage and latency target*, with explicit trade-offs: regenerative vs bent-pipe, optical vs RF ISL.
2. **Regulatory pathway sketch** — which jurisdictions and authorities must be engaged **first**, and **why**.
3. **First-order business case** — the **single** most viable initial customer segment and revenue model.

Plus the challenge format requires all three dimensions (technical / regulatory / economic) to be addressed, output must be **pre-IP and ESA-format-compliant**, and AI tools are permitted.

## 2. What they are actually asking

Read the constraints again and a pattern emerges. The brief is unusually honest about the things that *don't work*:

> "bent-pipe NTN systems depend on a visible gateway feeder link, which limits effective coverage to the gateway's footprint"
> "reaching 'any point on Earth' therefore requires **either a very dense constellation or an inter-satellite mesh**"
> "regenerative reduces feeder-link dependency but **increases payload complexity, power draw, and thermal load**"
> "full gNB-onboard integration with a global ISL mesh has **few operational precedents**"
> "a global gNB-in-space service can technically bypass in-country ground infrastructure — several administrations require local traffic routing for lawful intercept and data sovereignty, **which is at odds with a pure ISL-mesh architecture**"

That last sentence is the giveaway. **OQ has already identified that the elegant answer (a full autonomous mesh) is the one that is hardest to license.** They are not looking for a team to rediscover the mesh; they are looking for a team that can navigate the contradiction.

### The three real questions behind the three stated ones

| Stated | Actually asking |
|---|---|
| "Define a constellation architecture" | *How little can you get away with?* Where is the minimum viable point on the regenerative/ISL spectrum that still delivers a defensible "any point on Earth" claim, for a company with ~€80M raised and 12 satellites flying? |
| "Regulatory pathway sketch" | *How do you serve everywhere without needing everyone's permission at once?* Sequence, not a list. And: how do you reconcile ISL routing with lawful intercept? |
| "First-order business case" | *Who writes the first cheque, and is it big enough to pay for the ISL terminals?* |

## 3. The four traps

**Trap 1 — The mega-constellation.** It is easy to compute that continuous global coverage at 30° minimum elevation needs several hundred satellites, and to then propose 400 satellites with lasers. That design exists; it is called Starlink and it cost ~$10B. Proposing it to OQ is proposing they lose. *The interesting answer is architecturally graded: not every satellite needs a laser, not every region needs continuous coverage, not every service needs sub-second latency.*

**Trap 2 — Treating "any point on Earth" as "continuous coverage everywhere".** The brief says *"serving any point on Earth"* and separately mentions *"store-and-forward operation"* over *"polar and oceanic coverage gaps"*. Those two statements are only compatible if coverage is **service-differentiated**: continuous where it is needed and paid for, store-and-forward where it is not. **Say this explicitly and early. It reframes the whole problem and it is what a real operator does.**

**Trap 3 — Ignoring replenishment.** A 5-year design life means ~20% of the fleet must be rebuilt and relaunched every year, forever. A business case that amortises a constellation once over ten years is wrong by roughly a factor of two.

**Trap 4 — Monetising everything.** The brief explicitly warns against it. Pick one segment. Defend the choice by *rejecting* the others out loud.

## 4. How to win

A judging panel of industry mentors, in two days, rewards:

1. **A stated design point, early.** "We size to X% of Earth's surface with continuous service at ε ≥ Y°, and Z-minute store-and-forward elsewhere, at N satellites." Numbers in the first 90 seconds.
2. **Showing your arithmetic.** Constellation sizing, link budget and latency budget are all closed-form. Compute them; put the method on a slide. It separates you from teams that gesture.
3. **Naming the contradiction they planted.** The ISL-vs-lawful-intercept conflict. Answer it with an architecture, not a caveat.
4. **Grounding in *their* reality.** 12 satellites, 60 MHz MSS S-band, priority ITU filings via Luxembourg, Rel-19 frozen Dec 2025, BEAMSAT-5G and CREST-5G running, Telefónica Germany trial live, EU 2 GHz MSS proceeding in flight, €25M EIB. All of that is public and none of it is in the brief. Using it proves you engaged with *the company*, not just the problem statement.
5. **A migration path, not a clean-sheet.** Show how you get from OQ's today to your design in phases where each phase is independently fundable and independently revenue-generating.
6. **An honest risk register.** What kills this? EPFD limits, EU 2 GHz timeline slipping to 2029, thermal limits on the payload, laser terminal export control, a single MNO partner walking.

## 5. Suggested deliverable structure (ESA-ish, 2-day scope)

```
1. Executive summary — the design point in five bullets + one diagram
2. Mission & service definition — who, where, what latency, what data rate
3. System architecture
   3.1 Payload trade: bent-pipe / split / regenerative        [decision + why]
   3.2 Constellation design: shells, count, Walker notation   [with sizing maths]
   3.3 ISL trade: optical vs RF, topology                     [decision + why]
   3.4 Ground segment: gateways, TT&C, core
   3.5 Link + latency budgets                                 [numbers]
   3.6 SWaP, thermal, radiation, design life                  [numbers]
4. Regulatory pathway — sequenced, with a critical-path Gantt
5. Business case — segment choice, unit economics, revenue model, 10-yr shape
6. Roadmap — Phase 0 (today) → Phase 3, with gates and funding sources
7. Risk register + what would make us abandon this
```

Keep sections 3.1, 3.3, 4 and 5 as the load-bearing ones — those map 1:1 onto OQ's three Expected Outcomes.
