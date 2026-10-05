# OQ fleet growth (10 → 30 satellites): where to add it, and the line changes

Source: DCD, 6 Mar 2026, "OQ Technology lands $29.5m financing to build, launch 20+ satellites in 2 years"
https://www.datacenterdynamics.com/en/news/oq-technology-lands-295m-financing-to-build-launch-20-satellites-in-2-years/

- OQ operates **10** IoT satellites today, in low Earth orbit (S-band). Our proposal says ~12, which is wrong.
- The EIB lent **€25M** of venture debt (InvestEU). The terms require **≥20 satellites built and launched within 2 years**.
- OQ plans **30 satellites in the next few years**, and long term **100 direct-to-phone (D2D) payloads** on its own and hosted satellites.
- C-band D2D to ordinary smartphones starts mid-2026: text in 2026, voice across Europe in 2027.

## Which section

| Priority | Section | Why |
|---|---|---|
| **Main** | **03 Proposed Direction → Constellation paragraph** | The brief's Expected Outcome #1 is the sized constellation (satellite count, orbits, ISLs). This is where judges look. At 30 satellites (3 planes × 10) the RF inter-satellite ring also becomes feasible, which fixes review issue #2 |
| Required fix | **01 Executive Summary → Design Point panel** | "~12 satellites" is wrong; OQ has 10 today |
| Short mention | **05 Next Steps** | Shows we will *test* both fleet sizes in the Phase 2 simulation |
| Optional | 03 Business angle, 03 Engagement step 05, 04 Risk table | Adds the EIB financing, OQ's actual bands (S-band IoT, C-band D2D) and hosted payloads |

Do **not** put this only in Next Steps. There it reads as future work, but it belongs to the constellation design.

## Patch 1: core changes (6 lines, recommended)

Line numbers refer to `final.md`. Apply with `patch final.md < fleet-30-core.diff` (or `git apply`).

```diff
--- a/final.md
+++ b/final.md
@@ -13,7 +13,7 @@
 The first beachhead is offshore energy and maritime operations: Lynq adds the software layer that makes regenerative NTN capacity measurable and deployable.
 
 **Design point:**
-- **~12** satellites in orbit today (OQ's current LEO fleet)
+- **10 → 30** satellites: OQ's fleet today → planned (EIB-backed)
 - **10°** minimum elevation
 - **100%** full regenerative gNB on every satellite
 - **RF+optical** RF intra-plane ISL, optical cross-plane relay subset
@@ -38,11 +38,11 @@
 
 *[Figure] Teal = policy-compliant path via ISL to an authorised gateway and 5G Core; grey = blocked gateway.*
 
-**Constellation (sized with the twin).** We start with OQ's 12 LEO satellites focused on one region: the North Sea offshore energy basin (UK, Norwegian, Danish, Dutch and German sectors, ~51–61°N).
+**Constellation (sized with the twin).** We start with OQ's 10 in-orbit satellites and size the twin for its planned 30, focused on one region: the North Sea offshore energy basin (UK, Norwegian, Danish, Dutch and German sectors, ~51–61°N).
 At ~500–550 km and 10° minimum elevation, one footprint is ~3,000 km across, so one satellite in view covers the whole basin and every land gateway around it.
-Twelve satellites give frequent passes, not continuous coverage: alarms go out on the next pass and store-and-forward carries bulk data between passes.
-At a 5-year life, that is ~2–3 replacements per year.
-More satellites later close the gaps and extend to the Norwegian Sea and Atlantic.
+Ten satellites give frequent passes, not continuous coverage: alarms go out on the next pass and store-and-forward carries bulk data between passes.
+At a 5-year life, a 30-satellite fleet needs ~6 replacements per year.
+Scaling to OQ's planned 30 (e.g., 3 planes × 10) shrinks gaps between passes about 3× and lets each plane close an RF inter-satellite ring; the same policies then add mesh relaying and extend to the Norwegian Sea and Atlantic, on the way to OQ's 100 D2D payloads.
 
 **Payload trade.** Full regenerative gNB: bent-pipe cannot serve users with no gateway in view, and split gNB (options 2/7.2x) keeps most RF/PHY power onboard while RRC still round-trips over the feeder.
 Power, thermal and radiation costs are mitigated by a narrowband gNB, duty-cycling over empty ocean and COTS processing under a rad-hard supervisor.
@@ -96,4 +96,4 @@
 
 ## 05 Next Steps
 
-For Phase 2 in Luxembourg, Lynq will simulate one offshore corridor, bent-pipe vs. regenerative, under changing visibility, gateway access, load and ISL conditions, showing priority handling, dynamic ISL/feeder/store-and-forward selection, latency, delivery probability, queue depth, TCO and routing compliance.
+For Phase 2 in Luxembourg, Lynq will simulate one offshore corridor at 10 and 30 satellites, bent-pipe vs. regenerative, under changing visibility, gateway access, load and ISL conditions, showing priority handling, dynamic ISL/feeder/store-and-forward selection, latency, delivery probability, queue depth, TCO and routing compliance.
```

| Line in final.md | Section | Change |
|---|---|---|
| 16 | 01 Design Point | `~12` → `10 → 30` satellites (fleet today → planned) |
| 41 | 03 Constellation | 12 LEO satellites → 10 in orbit, twin sized for the planned 30 |
| 43 | 03 Constellation | "Twelve satellites" → "Ten satellites" |
| 44 | 03 Constellation | ~2–3 → ~6 replacements/yr (30 satellites ÷ 5-year life) |
| 45 | 03 Constellation | **The scaling sentence**: 3 planes × 10, gaps ~3× shorter, RF ring per plane, mesh relaying, path to 100 D2D payloads |
| 99 | 05 Next Steps | adds "at 10 and 30 satellites" |

Net length: about +2 lines at 10 pt. This fits in the ~3 spare lines on page 2.

## Patch 2: optional changes (apply after or without Patch 1)

```diff
--- a/final.md
+++ b/final.md
@@ -49,7 +49,6 @@
 The scheduler must sit in orbit because the gNB sorts every message into three classes: **critical** (alarms, safety/shutdown commands, a few hundred bytes) takes the first uplink slot and first authorised path on the current pass; **regular** (telemetry, logs, files) is queued onboard and store-and-forwarded on a later pass (≤90 min); **metadata** (device status, position, delivery receipts, policy tags) is tiny but tells the twin and policy engine where each asset is and which gateway it may use.
 
 Example: mid-Atlantic platform → Frankfurt cloud in ~75–110 ms one-way over ISL, versus no service on bent-pipe.
-Baseline is 3GPP Rel-17 NTN, with Rel-18 enhancements and a Rel-19-ready roadmap.
 
 ISL trade: optical offers high capacity and low interference but needs precise pointing and tracking; RF (Ka/V/W-band) adds spectrum and interference constraints.
 Narrowband traffic needs only single-digit Mbps per satellite, so **we choose RF intra-plane ISL on all satellites** (near-static geometry, proven by Iridium) **and optical cross-plane on a relay subset** (no spectrum licence, hard to intercept), from European suppliers to avoid ITAR/EAR.
@@ -73,7 +72,7 @@
 2. **ITU BR via Luxembourg** — Priority filings
 3. **International waters** — No landing rights needed
 4. **North Sea regulators & MNOs** — Coastal coverage
-5. **EC/CEPT** — EU 2 GHz MSS, off the critical path
+5. **EC/CEPT** — S-band MSS (IoT) and C-band D2D spectrum
 
 ### Business angle
 
@@ -81,16 +80,16 @@
 Lynq reduces blind spots, improves alarm delivery and cuts dependence on VSAT and fixed gateways.
 
 Revenue: integration fees, monthly subscriptions by asset and traffic class, usage charges for data/priority QoS, and MNO wholesale or roaming.
-For the 12-satellite North Sea network, opex including replenishment is ~€9M/yr: break-even at ~75k offshore assets at €120/yr, or ~9k sovereign/defence endpoints at €1,000+/yr.
+For the initial North Sea network, opex including replenishment is ~€9M/yr: break-even at ~75k offshore assets at €120/yr, or ~9k sovereign/defence endpoints at €1,000+/yr.
 At ~€2–3/MB we price per asset, never per byte.
-OQ's EIC Accelerator award (€2.5M grant plus up to €15M equity) for direct-to-mobile connectivity funds a second service on the same network: SOS and safety messaging to unmodified phones for offshore crews and vessels, alongside asset IoT.
+OQ's EIC Accelerator award (€2.5M grant plus up to €15M equity) and €25M EIB venture debt tied to 20+ launches within two years fund a second service on the same network: SOS and safety messaging to unmodified phones for offshore crews and vessels, alongside asset IoT.
 TCO is benchmarked against VSAT, private LTE, Sateliot, Skylo, Starlink D2C/Lynk and Iridium.
 
 ## 04 Key Assumptions & Risks
 
 | Risk | Assumption | Mitigation |
 |---|---|---|
-| Payload | Final power, compute, radiation and RAN-interface limits may differ. | Payload-independent policies with cloud/gateway fallback; OQ interface checklist. |
+| Payload | Final power, compute, radiation and RAN-interface limits may differ. | Payload-independent policies (dedicated and hosted payloads) with cloud/gateway fallback; OQ interface checklist. |
 | ISL / regulatory | Final ISL, gateway and spectrum choices may change. | Simulate optical/RF ISLs, gateway visibility and store-and-forward; ITU/national rules as hard constraints. |
 | Adoption | Customers may resist terminals, MNO integration or uncertain SLAs. | One wind-turbine alarm use case, measured TCO and a paid pilot with latency, availability and delivery targets. |
 
```

| Line in final.md | Section | Change |
|---|---|---|
| 52 | 03 Technical | **Deleted** "Baseline is 3GPP Rel-17 NTN…" to make room; Rel-17/18/19 is still cited in the Doppler line |
| 76 | 03 Engagement step 05 | "EU 2 GHz MSS, off the critical path" → "S-band MSS (IoT) and C-band D2D spectrum" |
| 84 | 03 Business | "12-satellite" → "initial" (the €9M/break-even figures stay) |
| 86 | 03 Business | adds €25M EIB venture debt tied to 20+ launches within two years |
| 93 | 04 Risk table | Payload mitigation now covers dedicated and hosted payloads |

With both patches, the net length is about +2–3 lines. Re-check that it still fits on 2 pages.

## Check before submitting
1. **3 planes × 10** is an example layout, not OQ's announced orbital plan. The ring works at about 550 km because the 36° spacing is under the roughly 41° line-of-sight limit.
2. **"Gaps about 3× shorter"** is a first estimate (3× the satellites). Confirm it with the pass/revisit simulation.
3. **€9M/yr opex** was sized for 12 satellites. At 30 it scales to about €22M/yr if linear (our estimate, not OQ's). Maryam should confirm it or state the 30-satellite figure.
4. The article does not confirm the **EIC €2.5M / €15M** figures. They still need their own source.
5. **"Nov-2025 concession"** (engagement step 01): the article's only Nov-2025 event is the emergency-broadcast demo to smartphones. Check that the concession is real.
6. Apply the same wording to `final.docx` (and regenerate `final.pdf`). The diffs above only cover `final.md`.
