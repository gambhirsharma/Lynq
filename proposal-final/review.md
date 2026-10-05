# Lynq NTN-Pulse: condensing change log and review

Source: `../working-pdf.pdf`, 3 pages. The third page held only about 3 lines of Next Steps plus the roles and footer.
Result: `final.pdf`, 2 pages A4, with about 2 cm free at the bottom of page 2.
Word count went from 1,336 to 1,260 (about −6%). No facts, numbers, names or claims were removed.

## Files

| File | What it is |
|---|---|
| `final.md` | Final proposal (Markdown) |
| `final.html` / `final.pdf` | Final proposal, styled, 2 pages |
| `original.md` | The working PDF transcribed to Markdown (baseline for the diff) |
| `working-pdf.txt` | Raw text of the working PDF. The line numbers below refer to this file |
| `changes.diff` | Unified line diff, `original.md` → `final.md` |
| `changes-word.diff` | Word-level diff (easier to read) |

## 1. What changed (line numbers are from `working-pdf.txt`)

### Layout (this did most of the work to fit two pages)
- Page margins: 12/16/11 mm → 10/14/9 mm.
- Body text: 8.7 pt / 11.6 pt leading → 8.6 pt / 11.2 pt.
- Title: 22 pt → 20 pt. The space above and below H2/H3 headings is tighter.
- These are unchanged: the Design Point panel, the data-path figure, the engagement sequence, the risk table, the roles and the footer.

### Text

| Orig. lines | Section | Change |
|---|---|---|
| 17–18 | Exec summary | Joined two sentences: "…5G Core and cloud, applying 3GPP-aligned policies for…" |
| 29–30 | Exec summary | Moved the beachhead sentence up into the summary paragraph, above the Design Point panel. This removed one paragraph block |
| 33–34 | Problem | "Traditional transparent" → "Transparent"; "require" → "need"; dropped "network" |
| 35 | Problem | Dropped "geographically" |
| 36–37 | Problem | Joined two sentences with "…pipelines, whose traffic…"; "require priority, while" → "need priority;"; dropped "can" |
| 39–40 | Problem | "Lynq provides the policy layer that decides" → "Lynq's policy layer decides" |
| 44 | Technical | Removed the lead-in "Lynq combines:" (the bullets follow the heading directly) |
| 45–50 | Technical | Dropped the lead verbs "models" and "covers"; "using QoS" → "by QoS" |
| 55–56 | Figure caption | "industrial terminal → regenerative onboard gNB" → "terminal → onboard gNB"; "application" → "app" |
| 58 | Constellation | "and focus them on" → "focused on" |
| 59–60 | Constellation | Dropped "a typical", "altitude" and "a"; "a single satellite" → "one satellite" |
| 61 | Constellation | "rather than" → ", not" |
| 62–63 | Constellation | Rewrote: "More satellites can later close the pass gaps and extend coverage to…" |
| 66–71 | Payload trade | Reordered the sentence so the reason comes first: "The scheduler must sit in orbit because the gNB sorts every message into three classes:". Class names are now **bold**. Also: "safety and shutdown" → "safety/shutdown"; "sensor telemetry" → "telemetry"; "delivered by store-and-forward" → "store-and-forwarded"; dropped "the" twice |
| 73 | Standards | Rewrote: "Baseline is 3GPP Rel-17 NTN, with Rel-18 enhancements and a Rel-19-ready roadmap." |
| 74–76 | ISL | "It evaluates ISL topology" → "ISL trade"; "links offer" → "offers"; "RF links provide different … characteristics" → "RF differs in acquisition and availability" |
| 76–78 | ISL | No text change. The RF and optical choice is now **bold** (as in the v2 HTML) |
| 79 | Doppler | "The system implements advanced Doppler/delay pre-compensation … using" → "Doppler/delay pre-compensation … uses" |
| 84 | Regulatory | "Dilemma is that" → "Dilemma:" |
| 86 | Regulatory | "through an authorised" → "over an authorised" |
| 88–89 | Regulatory | "The compliance layer" → "Compliance"; dropped "together" |
| 101–102 | Business | Dropped the Oxford comma; "explicitly aligning" → "aligned" |
| 104 | Business | "Revenue combines" → "Revenue:"; "assets" → "asset" |
| 107–108 | Business | "gives a funded route to" → "funds"; dropped "North Sea" (the paragraph already names the network) |
| 109 | Business | "The business case compares TCO with … baselines" → "TCO is compared with …" |
| 117 | Risk table | "Use modular" → "Modular" |
| 129 | Next steps | "and compare" → ", comparing" |
| 131 | Next steps | "demonstration" → "demo" |

I kept every number, company name, regulation, tier and claim word for word. In particular, I did not fix any of the review issues below inside the final version. That is your call as authors, and there is about 2 cm of space on page 2 to do it.

---

## 2. Deep review

The review is measured against the OQ brief (`NEOSPACE Challenge OQ.md`) and its three expected outcomes: (1) a sized constellation with payload and ISL trade-offs, (2) a regulatory pathway, (3) a focused business case.

### A. Critical: contradictions inside the proposal that an OQ judge will spot

1. **Satellites in orbit today cannot gain ISLs.** The Design Point says "~12 satellites in orbit today (OQ's current fleet)". It also says "100% regenerative gNB on every satellite", "RF ISL on all satellites" and "optical cross-plane relay subset". ISL terminals cannot be retrofitted to satellites already in orbit, and the current fleet is not described anywhere as having ISLs.
   *Fix:* describe it as a 12-satellite **Block-1** of next-generation satellites that replaces or joins the current fleet through the planned 2–3 replacements per year. Alternatively, say plainly that ISL arrives with replenishment.

2. **An ISL mesh does not close with 12 satellites unless they share a plane.** At about 550 km, with about 100 km of atmospheric grazing clearance, the maximum in-plane line-of-sight separation is about 41°. A closed intra-plane ring therefore needs ≥ 9 satellites per plane. Twelve satellites spread over several planes give no working intra-plane chain and almost no cross-plane links.
   So "Mesh-relayed <250 ms" and "mid-Atlantic → Frankfurt over ISL in 75–110 ms" are **not supported by the 12-satellite design**.
   *Fix:* state the plane layout. For example, 1 plane × 12 satellites at 30° spacing gives an RF link of about 3,600 km, which is feasible at single-digit Mbps. Or move the mesh claims explicitly to the scale-out phase.

3. **The "Continuous <150 ms" tier contradicts the constellation paragraph.** That paragraph says "frequent passes rather than continuous coverage".
   *Fix:* label the tiers per phase ("Phase 1: Store-and-forward + next-pass alarms; scale-out: Continuous/Mesh"). Another option is to map them onto the three message classes (critical / regular / metadata). Right now there are two unrelated sets of three, which is confusing.

4. **Safety and shutdown commands sent "on the next pass".** A gap of tens of minutes is not acceptable for safety-instrumented functions, and energy-operator judges will object.
   *Fix:* position the service as a backup or last-resort alarm path and non-safety-critical backhaul. Then quote twin numbers: mean and maximum revisit gap at 55°N for the actual orbits. OQ's fleet is mostly in sun-synchronous orbit, so gaps can be uneven. The "≤90 min" store-and-forward figure needs a stated maximum gap behind it.

5. **The global sizing has gone.** The brief's first expected outcome is a constellation for "any point on Earth", sized to a coverage and latency target. v2 had "~90 satellites in two 550–600 km shells". The working version dropped it, so the proposal now answers a regional question only.
   *Fix:* add one line: "Phase 1: 12 satellites, North Sea. Global scale-out: ~90 satellites, two shells (~70 Walker Delta ~60–65° + ~20 near-polar), which enables the Continuous/Mesh tiers." This also resolves points 2 and 3. The line fits in the free space.

### B. Brief requirements the proposal does not address
6. **Space debris and orbital safety.** IADC guidelines, the deorbit timeline (the 5-year rule for LEO, ESA Zero Debris, the proposed EU Space Act) and collision avoidance are not mentioned. The brief lists this explicitly under Regulatory.
7. **EU Dual-Use Regulation (EU) 2021/821.** Only ITAR/EAR is named. The brief asks for both.
8. **SWaP, thermal and TRL.** There is no per-satellite power or mass budget and no thermal figure. There is also no TRL 4–6 statement, which the brief asks for directly.
9. **Spectrum bands.** The access-link band is never named (OQ uses 2 GHz MSS S-band, and MNO spectrum for D2D), and neither is the feeder band.
   The engagement step "EU 2 GHz MSS, off the critical path" needs checking. If 2 GHz MSS is OQ's access band in Europe, it *is* on the critical path. Also, the current EU 2 GHz MSS authorisations expire in May 2027, so the post-2027 regime is a live opportunity or risk.
10. **Minimum viable ground segment.** The brief requires TT&C and feeder gateways. The proposal names none: no sites (e.g., Norway, Denmark, Luxembourg), no count.
11. **Phased-array antennas and onboard beam management.** The brief requires these. They appear only as a dashboard item.
12. **D2D harmonisation across countries.** The EIC direct-to-mobile service needs MNO spectrum deals in the UK, NO, DK, NL and DE. The engagement sequence only says "North Sea regulators & MNOs – coastal coverage". Name it as a supplemental-coverage-from-space-style arrangement per country.

### C. Regulatory accuracy
13. **"International waters – no landing rights needed" is wrong for platforms.** North Sea platforms and wind farms sit on the coastal states' continental shelf and EEZ. Coastal states have jurisdiction over installations there (UNCLOS arts. 60/80), and the UK and Norway regulate telecoms on them. Only vessels on the high seas fall under flag-state rules.
    *Fix:* limit step 03 to vessels on the high seas, and move platforms into step 04.
14. **Lawful intercept outside MNO partnerships.** LI is covered only for the MNO case. State who handles LI and data retention when OQ provides the service directly as an MSS operator.
15. **NIS2.** Both the space sector and the energy sector are in NIS2 scope. For critical-infrastructure buyers, a line on NIS2 compliance and cybersecurity is a cheap way to gain credibility.
16. **Check the facts before submitting:** "OQ's Nov-2025 concession" and "EIC Accelerator €2.5M grant + up to €15M equity". Add a source or date for each. A wrong number here costs more credibility than leaving it out.

### D. Business case
17. **"~75k offshore assets" looks too large for the North Sea** if it means installations. There are a few thousand turbines and a few hundred oil and gas installations.
    *Fix:* call them "connected endpoints" and show the bottom-up count (turbines × sensors + platforms + pipelines + vessels).
18. **Pricing is internally inconsistent.** "Price per asset, never per byte" sits next to "usage charges for data/priority QoS". Also spell out the check: €120/yr ÷ €2–3/MB ≈ 40–60 MB per asset per year. That shows the price is consistent with narrowband IoT.
19. **Opex of €9M/yr includes 2–3 replacements per year.** That implies roughly €2–3M per satellite including launch. That is plausible for a small satellite, but not once optical terminals are added. Add a three-line cost breakdown and a capex line. Nothing currently says who funds the 12-satellite block.
20. **Lynq's own position in the value chain is unclear.** Is Lynq selling software to OQ, or selling connectivity to energy operators with OQ as the network? State Lynq's revenue share.
21. **Benchmarks are missing Tampnet**, the incumbent offshore 4G/5G network across the North Sea and the real alternative for platforms. Starlink Maritime is also missing for crew connectivity. The brief also asks for a GEO-based NTN IoT comparison: note that Skylo covers it, or add Viasat IoT.

### E. Technical precision
22. **"Narrowband gNB".** Rel-17 IoT-NTN (NB-IoT/eMTC) is LTE-based, so the node is an eNB. A gNB is NR. OQ's service is NB-IoT. Use "eNB/gNB (NB-IoT today, NR-NTN/RedCap later)". OQ engineers will notice this.
23. **Doppler/delay pre-compensation "from moving platforms".** In 3GPP NTN, the UE performs pre-compensation using GNSS plus broadcast ephemeris (SIB31 for IoT-NTN, SIB19 for NR-NTN), with extended timing advance and K_offset. Say this; the brief asks for it explicitly.
24. **The 75–110 ms figure has no breakdown.** Give the split between uplink, ISL hops, feeder and terrestrial legs.
25. **Phase 2 demo has no success criteria.** Add measurable targets, e.g., critical-message delivery ≥ 99% within X minutes, and 100% routing compliance under blocked-gateway scenarios.
26. **No references.** Cite 3GPP TR 38.821 and TR 22.822, which the brief names as the baseline, plus the TS numbers for the Rel-17/18 NTN features used.

### F. What is strong (keep it)
- A clear single beachhead: the North Sea offshore energy basin. This is exactly the focus the brief asks for.
- An explicit trade-off between regenerative, split and bent-pipe payloads, and between optical and RF ISL, with a decision.
- "Sovereignty is built into routing" is a strong answer to the Consultant's Dilemma, and user-plane breakout plus MNO-held LI is the right mechanism.
- The engagement sequence is ordered and justified. The break-even arithmetic is shown.
- AI is kept advisory, with deterministic safety and timing controls. Judges value that.

### Suggested priority if you have one hour
Fix issues 1–3 with a Phase 1 / scale-out split in one line using the ~90-satellite v2 sizing. Then fix 13 (international waters), add one sentence for 6 and 7 (debris and dual-use), and correct 22 (eNB/gNB). All of this fits in the space left on page 2.
