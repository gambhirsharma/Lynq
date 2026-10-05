# OQ Technology / "AnyPoint-NTN" — Research Pack

**Challenge:** NEOSPACE Europe 2026 Challenge, category *Next-Gen Downstream*
**Use case sponsor:** OQ Technology S.à r.l. (Luxembourg)
**Use case title:** *AnyPoint-NTN: Global gNB-Onboard LEO Constellation for Ubiquitous 5G NR-NTN*
**Event:** 19–20 October 2026, Luxexpo The Box, Luxembourg (2-day team challenge, teams ≤6, mentored, pre-IP / ESA-format output)
**Pack compiled:** 18 September 2026

---

## Read in this order

| # | File | What it is | Read if… |
|---|------|-----------|----------|
| 01 | `01-PRIMER-no-space-background.md` | **Start here.** Explains every term in the challenge brief from zero. Orbits, 5G, gNB, NTN, bent-pipe vs regenerative, ISL, EPFD, SWaP, TRL. | You are not from a space/telecom background |
| 02 | `02-OQ-TECHNOLOGY-dossier.md` | Everything known about the sponsor: history, fleet, money, spectrum, patents, ESA projects, publications, partners, strategy | Always — you must pitch *to them* |
| 03 | `03-CHALLENGE-decoded.md` | What OQ is *actually* asking for, the unstated agenda, how to win | Always |
| 04 | `04-TECHNICAL-deep-dive.md` | Architecture options, constellation sizing maths (with worked numbers), ISL trade, link budget, SWaP budget | Technical dimension |
| 05 | `05-REGULATORY-deep-dive.md` | ITU, EPFD, 2 GHz MSS, SCS, landing rights, lawful intercept, export control, debris | Regulatory dimension |
| 06 | `06-BUSINESS-CASE.md` | Segments, unit economics, revenue model, comparables | Economic dimension |
| 07 | `07-COMPETITIVE-LANDSCAPE.md` | Starlink D2C, AST, Lynk, Sateliot, Skylo, Iridium, Kepler, IRIS² | Benchmarking (explicitly requested by OQ) |
| 08 | `08-OUR-PROPOSAL.md` | A concrete, defensible answer to the three Expected Outcomes | The deliverable |
| 09 | `09-SOURCES.md` | Full bibliography with links | Citations |

---

## The one-paragraph version

Mobile networks cover ~20% of land and almost none of the ocean. 3GPP (the body that writes the 5G rulebook) has now standardised satellites as part of 5G — first as dumb mirrors in orbit (Rel-17, 2022), and as of **Release 19 frozen in December 2025**, as *full 5G base stations flying in space* ("regenerative payload"), which unlocks satellite-to-satellite links and store-and-forward. OQ Technology is a Luxembourg operator with ~12 satellites in orbit doing exactly the first version of this for IoT, now moving into direct-to-smartphone. They are asking student teams to design what the *next* generation looks like: a constellation where every satellite is a full 5G base station, linked to its neighbours, serving any point on Earth without needing a ground station in view — and to be honest about what that costs technically, legally and commercially.

## The three things they will judge you on (their words, paraphrased)

1. **A defined constellation architecture** — satellite count, orbital shells, ISL topology, sized to a stated coverage and latency target, with explicit regenerative-vs-bent-pipe and optical-vs-RF ISL trade-offs.
2. **A regulatory pathway sketch** — which jurisdictions and authorities first, and *why*.
3. **A first-order business case** — one viable initial segment and revenue model, not all of them.

> They wrote *"rather than attempting to monetize every segment simultaneously"* and *"reason about unit economics per connected device or per bit rather than assume an unconstrained budget."* That is a direct instruction. Teams that pitch "$XX billion TAM, we'll take 1%" lose.
