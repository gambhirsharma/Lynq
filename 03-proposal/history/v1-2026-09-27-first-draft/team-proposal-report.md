# Review Report — `team-proposal.md` (Lynq NTN-Pulse)

**Reviewed against:** `NEOSPACE Challenge OQ.md` (the official brief), `research/03-CHALLENGE-decoded.md`, `research/08-OUR-PROPOSAL.md`, `research/02-OQ-TECHNOLOGY-dossier.md`
**Format:** 2-page Phase 1 proposal (Title / Challenge / Category / Team → 1 Exec Summary → 2 Problem & Opportunity → 3 Proposed Direction → 4 Key Assumptions & Risks → 5 Next Steps)
**Current length:** ~760 words. Two pages hold roughly 900–1,000 words, so there is room for about 150–250 more words once the filler is cut.

---

## 1. Verdict in one paragraph

The draft is well written. It follows the required section structure, it reads professionally, and it has two strong ideas: **policy-based and sovereignty-aware routing** and **differentiated traffic classes with store-and-forward**. The problem is that **it answers a different question from the one OQ asked.** OQ's three Expected Outcomes are (1) a **constellation architecture** with satellite count, shells, ISL topology and a stated coverage and latency target, (2) a **sequenced regulatory pathway**, and (3) a **first-order business case with unit economics**. The draft presents a *software product* (digital twin + policy engine) and leaves every architecture decision as a "configurable scenario". It has **no numbers at all**: no satellite count, no altitude, no elevation angle, no latency target, no price, no ARPU, no device count. The judges score "design point stated early" and "show your arithmetic". As written, the draft is likely to be read as *"a nice dashboard that avoided the trade-offs."*

**The fix is not to throw it away.** Reposition Lynq NTN-Pulse as **the tool that we used to produce a concrete design point**, then state that design point. We keep the product story and we also answer OQ's three questions.

**Score against OQ's Expected Outcomes (current draft):**

| OQ Expected Outcome | Covered? | Comment |
|---|---|---|
| 1. Constellation architecture (count, shells, ISL topology, coverage/latency target) | 🔴 **Missing** | No satellite count, orbit or coverage target. The ISL choice is explicitly left open ("remains a configurable scenario"). |
| 1b. Regenerative vs bent-pipe trade-off | 🟡 Partial | The bent-pipe limitation is explained well. The split-gNB option (named in the brief) is never discussed. Costs of regenerative (SWaP, thermal, radiation) are only mentioned under risks. |
| 1c. Optical vs RF ISL trade-off | 🟡 Partial | Pros and cons are listed, but **no decision is made**. The brief asks for a choice. |
| 2. Regulatory pathway: *which authorities first, and why* | 🔴 **Missing** | Rules are listed (ITU, GDPR). There is no sequence and no named authority (Luxembourg ILR/LSA, ITU BR, EC/CEPT, MNO regulators). |
| 3. Business case: one segment + revenue model + unit economics | 🟡 Partial | The segment choice is good (offshore energy). The revenue lines are listed, but there is **no per-device or per-bit number**, which the brief asks for explicitly. |
| All three dimensions (tech / reg / econ) | 🟢 Yes | All three angles exist. |
| Format compliance | 🟢 Mostly | The sections are correct. A few meta lines and formatting issues need fixing (§4 below). |

---

## 2. What is good (keep these)

1. **Offshore energy / wind O&M as the beachhead.** This is a strong choice. It fits OQ's actual customers (oil & gas, Aramco-linked investor Wa'ed Ventures, Saudi subsidiary). International waters mostly need no landing rights, and the alarm-vs-bulk-data split is a real operational need.
2. **Traffic classes (alarms, control, telemetry, video, bulk).** This is the seed of the "any point on Earth = a service catalogue" reframe that `03-CHALLENGE-decoded.md` calls Trap 2. Push it further (see §3.1).
3. **Sovereignty built into routing.** This is our strongest idea and it matches the contradiction OQ planted in the brief (ISL mesh vs lawful intercept/data sovereignty). It needs sharper wording (see §3.3).
4. **AI is advisory and deterministic safety controls stay authoritative.** Mentors will like this framing.
5. **Risk section.** It is compact, each risk has a mitigation, and it ends with a paid-pilot success criterion. This is good practice.
6. **Phase 2 demo plan.** Comparing bent-pipe and regenerative on one corridor is concrete and credible for a 2-day event.

---

## 3. What is missing or weak (by priority)

### 3.1 🔴 No design point and no numbers (most important)
The judges want numbers in the first paragraph. Add **one sentence of design point** to the Executive Summary and a short architecture paragraph in §3. Suggested design point (taken from our own `research/08-OUR-PROPOSAL.md`; re-check the numbers before submitting):

> *~90 satellites in two shells at 550–600 km (Walker ~60–65° service shell + ~20-satellite near-polar shell), minimum elevation 10°, full regenerative Rel-19 gNB on every satellite, RF intra-plane ISL on all satellites plus optical cross-plane links on a ~20-satellite relay subset. Three service tiers: Continuous (<150 ms), Mesh-relayed (<250 ms), Store-and-forward (≤90 min).*

Also add **one comparison with numbers**, for example: *"Mid-Atlantic platform → Frankfurt cloud, no gateway in view: ~75–110 ms one-way via ISL vs **no service** on bent-pipe."* That single line justifies the whole architecture.

### 3.2 🔴 ISL choice is not made
"The topology remains a configurable scenario" reads as avoiding the decision. **Make a decision and justify it:**
- Narrowband IoT traffic per satellite is only single-digit Mbps, so **throughput is not the reason to pick optical**.
- **RF intra-plane**: the geometry is almost static, so it is cheap and proven (Iridium has done this since the 1990s).
- **Optical cross-plane on a subset only**: it needs no spectrum licence, sits outside the EPFD regime, and is hard to intercept, which is a sellable feature for defence.
- **European terminal suppliers only** (Tesat, Mynaric). A US-origin terminal would bring in **ITAR/EAR** and weaken the sovereignty pitch. This also covers the export-control point in the brief, which the draft does not mention.

### 3.3 🔴 Regulatory section: wording risk and no sequence
- **Wording risk:** *"bypassing a restricted gateway where legally permitted"* can read as regulatory evasion to a Luxembourg operator whose business depends on regulators. Replace it with the **"jurisdiction-aware mesh"** framing: *"A regenerative gNB knows the user's identity, registered PLMN and verified location (Rel-18 network-verified UE location), so routing becomes an enforceable policy: traffic egresses only at a policy-compliant gateway with local UPF breakout. Under MNO/SCS partnerships, the MNO keeps lawful intercept on its own core."* This presents sovereignty as something we **enforce**, which is the answer OQ is fishing for.
- **Technical inaccuracy:** a routing/policy engine cannot "enforce ITU Article 22 EPFD limits". EPFD is a property of the constellation design, the filing and the transmit masks (and mostly concerns Ka/Ku feeder links, not S-band access). Article 9 is the coordination *procedure*. Rephrase as: *"EPFD and coordination limits are treated as hard design constraints in the twin (feeder-link masks, gateway exclusion zones)."*
- **Missing sequence (the brief asks "who first, and why").** Add a 4–5 step sequence in one or two lines:
  1. **Luxembourg ILR + LSA**: extend the Nov-2025 concession to cover ISL and regenerative operation. Luxembourg is OQ's filing administration and flag state.
  2. **ITU BR (via Luxembourg)**: protect priority filings and meet bring-into-use milestones.
  3. **International waters**: offshore and maritime service can start without national landing rights (territorial seas and EEZ installations need a check).
  4. **Offshore-state regulators** (e.g. NO/UK/NL/DE North Sea) plus **MNO partners** (Telefónica DE, already a live OQ trial) for coastal and territorial coverage.
  5. **EC / CEPT**: EU 2 GHz MSS renewal and IRIS² interoperability. This is a later-phase prize and should stay off the critical path.
- **Not covered at all:** MNO spectrum for D2D (SCS arrangements), **space debris / IADC deorbit** (550–600 km decays naturally, so this is one line), **export control** (EU Dual-Use, ITAR/EAR), **landing rights and lawful intercept**. Each can be a half-line.

### 3.4 🟡 Business case has no unit economics
The brief explicitly asks for *"unit economics per connected device or per bit rather than assume an unconstrained budget."* Add two or three numbers, for example from `research/06` and `research/08`:
- Mature operating cost ~€26.5M/yr, including **replenishment** of ~18 satellites/yr at a 5-year life (Trap 3: if we ignore replenishment the case looks about 2× too good).
- Break-even: ~440k devices at a ~€60 blended ARPU. At the premium offshore ARPU (~€120) it is ~220k assets. **~26k defence/sovereign endpoints at €1,000+/yr cover the entire opex.**
- **Per-bit reality:** ~€1/MB, so we sell *per asset or per alarm class*, never per byte.
- Name the **comparables** the brief asks to benchmark: bent-pipe NTN IoT (Sateliot), regenerative D2C (Starlink D2C / Lynk), GEO NTN IoT (Skylo/Inmarsat), plus VSAT for offshore. One line.
- **Say what we are *not* selling first** (consumer D2D, broadband-to-handset). The brief rewards picking one segment and rejecting the others out loud.

### 3.5 🟡 Regenerative payload trade is incomplete
- Mention the **split-gNB option** (the brief names options 2 and 7.2x) and why we reject it. 3GPP did not adopt split for Rel-19, and it keeps the RF/PHY cost onboard while RRC still round-trips over the feeder link.
- State the **cost** of regenerative in §3, not only under risks: power, thermal, radiation. Give the mitigation: narrowband gNB (tens of watts), duty-cycling over empty ocean, a 12U–16U bus, COTS processing plus a rad-hard supervisor, and a 5-year life.

### 3.6 🟡 Missing OQ's favourite topic: mobility and context transfer over ISL
OQ has a **pending patent on ISL for cellular constellations** about base-station awareness and device record-keeping. Add one line: *"Xn-C over ISL for inter-satellite handover and UE context transfer, buffer forwarding during handover, and ephemeris-driven pre-computed routing tables uploaded from the ground."* This shows we read their IP and that we treat the ISL as more than a pipe.

### 3.7 🟡 Standards baseline is dated
*"Rel 17 baseline … Rel 19-ready roadmap"* undersells us. **Rel-19 was frozen in December 2025** and standardises the regenerative payload and store-and-forward, so Rel-19 should be the baseline for the regenerative gNB, with Rel-17/18 kept for legacy and UE compatibility. Also, Doppler/delay pre-compensation in NTN is done **by the UE using broadcast ephemeris and timing advance**. The system "supports/models" it rather than "implements" it. Rephrase to avoid an overclaim.

### 3.8 🟡 Not grounded in OQ's reality
Using public OQ facts shows we engaged with *the company*: **12 satellites in orbit**, **60 MHz of MSS S-band**, **Nov-2025 Luxembourg concession incl. D2D**, **priority ITU filings via Luxembourg**, **Telefónica Germany D2D demo (Jun 2026)**, **€25M EIB (Feb 2026)**, **ESA BEAMSAT-5G / CREST-5G**. Add a **migration path** from their 12 satellites (e.g. Phase 1: 4–6 regenerative pathfinders at ESA ARTES scale → ~48 → ~90). Right now the draft has no link to OQ's existing fleet.

---

## 4. Format and editorial fixes

| # | Issue | Fix |
|---|---|---|
| 1 | *"Phase 1 requires a credible two-page concept, not a complete operational MVP."* This is an internal note that was left in. | **Delete.** Use the space for the design point. |
| 2 | The team-roles line is out of order and broken: *"Maryam, TCO, … case.Davoud systems …; Gambhir, …; "* (missing space, trailing semicolon, Maryam listed first but last in the header) | *"Roles: Davoud Jokar — systems & digital twin; Ines Bouissou — NTN modelling & optimisation; Gambhir Sharma — cloud, APIs & deployment; Maryam Amini — TCO, pricing, regulation & first-buyer case."* |
| 3 | Category *"NextGen Downstream"* | Match the brief exactly: **"Next-Gen Downstream"**. |
| 4 | Title line has no subtitle or descriptor | e.g. **"Lynq NTN-Pulse — a jurisdiction-aware regenerative NTN for offshore operations"** |
| 5 | Mixed capitalisation / inconsistent terms: "Advanced Doppler/delay", "ISL Topology", "Rel 17" vs "Rel-17" | Use lower case mid-sentence. Standardise on "Rel-17/18/19". |
| 6 | No headings/bold in the markdown (plain lines). | Make the section titles `##` and the angle titles bold so the 2-page PDF can be scanned quickly. |
| 7 | No figure | If the template allows one, a **tiny data-path diagram or tier table** is worth more than 80 words of text. |
| 8 | Abbreviations not expanded on first use (QoS, TCO, ISL, gNB, EPFD, VSAT) | Expand once. Some mentors are business people. |
| 9 | "Consultant's Dilemma" is an unexplained label | Either define it in 5 words or drop it. |
| 10 | Pre-IP requirement | Check that nothing reads as patentable detail or confidential OQ data. The draft is fine now. Keep it that way when adding numbers. |

---

## 5. Suggested rewrites (drop-in text)

**Executive Summary (replacement, ~110 words):**
> Lynq NTN-Pulse turns OQ Technology's regenerative gNB-onboard constellation into a service operators can sell and regulators can approve. Design point: **~90 satellites in two 550–600 km shells, ε ≥ 10°, full Rel-19 regenerative gNB on every satellite, RF intra-plane ISL with an optical cross-plane relay subset.** "Any point on Earth" is delivered as three service tiers: Continuous (<150 ms), Mesh-relayed (<250 ms), Store-and-forward (≤90 min). Our digital twin and policy engine size this architecture and route every traffic class by QoS, latency, cost and **jurisdiction**, making data sovereignty enforceable in orbit. Beachhead: offshore energy and wind O&M, where no gateway is in view and no landing rights are needed, with defence as the margin segment.

**Regulatory angle (replacement for the "bypass" sentence):**
> A bent-pipe satellite cannot tell whose traffic it carries. A regenerative gNB knows the user's identity, PLMN and verified location, so Lynq routes each flow over ISL only to a **policy-compliant gateway with local user-plane breakout**. Under MNO partnerships, the MNO keeps lawful intercept on its own core. We call this a **jurisdiction-aware mesh**.

**Business angle (add after the revenue sentence):**
> At maturity, opex including ~18 replacement satellites/year is ~€26.5M. This breaks even at ~220k offshore assets at €120/yr, or ~26k sovereign/defence endpoints at €1,000+/yr. At ~€1/MB we never sell per byte: we price per asset and per priority class, against VSAT and private LTE TCO.

---

## 6. Checklist before submission

- [ ] Design point with numbers in the Executive Summary (count, shells, altitude, elevation, latency tiers)
- [ ] ISL **decision** made and justified (RF intra-plane + optical subset, European suppliers)
- [ ] Split-gNB option rejected in one line; regenerative SWaP cost + mitigation stated
- [ ] Regulatory **sequence** with named authorities (Luxembourg ILR/LSA → ITU BR → international waters → offshore states/MNOs → EC/CEPT)
- [ ] "Bypass" wording replaced by "jurisdiction-aware mesh"; EPFD claim corrected
- [ ] Debris, export control, SCS/MNO spectrum, lawful intercept: one half-line each
- [ ] Unit economics: opex incl. replenishment, break-even devices, ARPU, per-bit reality
- [ ] Comparables named (Sateliot, Skylo, Starlink D2C/Lynk, Iridium, VSAT)
- [ ] Xn-over-ISL / UE context transfer (OQ's patent area) mentioned
- [ ] Rel-19 as the baseline; Doppler wording fixed
- [ ] OQ grounding: 12 satellites, S-band, Nov-2025 concession, Telefónica demo, migration phases
- [ ] Meta line deleted; team-roles line fixed; category spelling matches the brief
- [ ] Fits on 2 pages (target ≤1,000 words)
