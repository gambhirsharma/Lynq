# Lynq NTN-Pulse

*Every signal, the right path.*

**Challenge:** OQ Technology — AnyPoint-NTN: Global gNB-Onboard LEO Constellation for Ubiquitous 5G NR-NTN
**Category:** Next-Gen Downstream
**Team:** Lynq — Davoud Jokar, Ines Bouissou, Gambhir Sharma, Maryam Amini

## 01 Executive Summary

Lynq NTN-Pulse is a software-defined digital twin and policy engine for OQ Technology's regenerative gNB-onboard LEO constellation.
It governs industrial traffic across onboard gNB, feeder/ISL paths, gateways, 5G Core and cloud, applying 3GPP-aligned policies for QoS, latency, availability, data residency, spectrum and cost.
The first beachhead is offshore energy and maritime operations: Lynq adds the software layer that makes regenerative NTN capacity measurable and deployable.

**Design point:**
- **~12** satellites in orbit today (OQ's current LEO fleet)
- **10°** minimum elevation
- **100%** full regenerative gNB on every satellite
- **RF+optical** RF intra-plane ISL, optical cross-plane relay subset
- Service tiers: **Continuous** <150 ms · **Mesh-relayed** <250 ms · **Store-and-forward** ≤90 min

## 02 Problem & Opportunity

**Status quo: the bent-pipe limit.** Transparent payloads relay radio signals but need a visible ground gateway and feeder link for processing, routing and terrestrial-core access.
If the gateway is outside the footprint, blocked, nationally restricted or overloaded, service degrades through delay, inefficient routing or loss of connectivity.
This hits offshore wind farms, energy platforms, vessels and pipelines, whose traffic needs different treatment: alarms and control commands need priority; telemetry, video and bulk files tolerate delay.

A regenerative gNB moves selected RAN and Layer 2/3 functions into orbit, but introduces Doppler and delay, handovers, intermittent feeder access, gateway selection, ISL routing and onboard compute limits.
Lynq's policy layer decides whether traffic is delivered immediately, routed, edge-processed or stored for later downlink.

## 03 Proposed Direction

### Technical angle

- **Digital twin:** satellite position, coverage, gateway visibility, feeder/ISL state, terminal location, traffic demand and onboard compute.
- **Policy engine:** assigns traffic classes to available paths by QoS, latency, reliability, residency and cost.
- **NTN model and dashboard:** timing, beam management, handover, link budgets, scheduling, queues, predicted outages and route decisions.

*[Figure] Data path: terminal → onboard gNB → policy engine → ISL/feeder → authorised gateway and 5G Core → enterprise app. Teal = policy-compliant path; grey = blocked gateway.*

**Constellation (sized with the twin).** We start with OQ's 12 LEO satellites focused on one region: the North Sea offshore energy basin (UK, Norwegian, Danish, Dutch and German sectors, ~51–61°N).
At ~500–550 km and 10° minimum elevation, one footprint is ~3,000 km across, so one satellite in view covers the whole basin and every land gateway around it.
Twelve satellites give frequent passes, not continuous coverage: alarms go out on the next pass and store-and-forward carries bulk data between passes.
At a 5-year life, that is ~2–3 replacements per year.
More satellites can later close the pass gaps and extend coverage to the Norwegian Sea and Atlantic approaches.

**Payload trade.** Full regenerative gNB: bent-pipe cannot serve users with no gateway in view, and split gNB (options 2/7.2x) keeps most RF/PHY power onboard while RRC still round-trips over the feeder.
Power, thermal and radiation costs are mitigated by a narrowband gNB, duty-cycling over empty ocean and COTS processing under a rad-hard supervisor.
The scheduler must sit in orbit because the gNB sorts every message into three classes: **critical** (alarms, safety/shutdown commands, a few hundred bytes) takes the first uplink slot and first authorised path on the current pass; **regular** (telemetry, logs, files) is queued onboard and store-and-forwarded on a later pass (≤90 min); **metadata** (device status, position, delivery receipts, policy tags) is tiny but tells the twin and policy engine where each asset is and which gateway it may use.
A bent-pipe payload cannot make this call without a gateway in view.

Example: mid-Atlantic platform → Frankfurt cloud in ~75–110 ms one-way over ISL, versus no service on bent-pipe.
Baseline is 3GPP Rel-17 NTN, with Rel-18 enhancements and a Rel-19-ready roadmap.

ISL trade (optical/laser vs. RF Ka/V/W-band): optical offers high capacity and low RF interference but needs precise acquisition, pointing and tracking; RF differs in acquisition and availability but adds spectrum, antenna and interference constraints.
Narrowband traffic needs only single-digit Mbps per satellite, so **we choose RF intra-plane ISL on all satellites** (near-static geometry, proven by Iridium) **and optical cross-plane on a relay subset** (no spectrum licence, hard to intercept), from European suppliers to avoid ITAR/EAR.

Doppler/delay pre-compensation from moving platforms uses applicable 3GPP Rel-17/18/19 procedures.
AI supports traffic forecasting, anomaly detection and resource prioritisation; deterministic timing, link-budget and safety controls remain authoritative.

### Regulatory angle

The Consultant's Dilemma: a local ground gateway may be technically attractive but unavailable because of national restrictions, data-residency rules or licensing.
A regenerative gNB knows the user's identity, PLMN and verified location, so Lynq applies routing policy onboard and sends each flow over an authorised ISL/feeder path only to a policy-compliant gateway with local user-plane breakout.
Under MNO partnerships, the MNO keeps lawful intercept on its own core.

Compliance treats ITU Radio Regulations Article 9 coordination and Article 22 EPFD limits as hard design constraints (feeder-link masks, gateway exclusion zones), with applicable PFD/EIRP conditions and national authorisations.
It supports EU-hosted processing, encryption, key ownership, data minimisation, pseudonymisation and controlled GDPR retention.
**Sovereignty is built into routing.**

**Engagement sequence**

1. **Luxembourg ILR/LSA** — Extend OQ's Nov-2025 concession to ISL and regenerative operation
2. **ITU BR via Luxembourg** — Priority filings
3. **International waters** — No landing rights needed
4. **North Sea regulators & MNOs** — Coastal coverage
5. **EC/CEPT** — EU 2 GHz MSS, off the critical path

### Business angle

The first buyer is a European offshore energy operator or offshore wind O&M provider (e.g., Equinor, Ørsted or Eni), aligned with OQ's European funding focus.
Lynq reduces blind spots, improves high-priority alarm delivery and lowers dependence on dedicated VSAT and fixed gateways.

Revenue: integration fees, monthly subscriptions by asset and traffic class, usage charges for data/priority QoS, and MNO wholesale or roaming.
For the 12-satellite North Sea network, opex including replenishment is ~€9M/yr: break-even at ~75k offshore assets at €120/yr, or ~9k sovereign/defence endpoints at €1,000+/yr.
At ~€2–3/MB we price per asset, never per byte.
OQ's EIC Accelerator award (€2.5M grant plus up to €15M equity) for direct-to-mobile connectivity funds a second service on the same network: SOS and safety messaging to unmodified phones for offshore crews and vessels, alongside asset IoT.
TCO is compared with VSAT, private LTE and manual inspection, benchmarked against Sateliot, Skylo, Starlink D2C/Lynk and Iridium.

## 04 Key Assumptions & Risks

| Risk | Assumption | Mitigation |
|---|---|---|
| Payload | Final power, compute, radiation and RAN-interface limits may differ. | Modular, payload-independent policies with cloud/gateway fallback; validate an OQ interface checklist. |
| ISL / regulatory | Final ISL, gateway and spectrum choices may change. | Simulate optical/RF ISLs, limited gateway visibility and store-and-forward; apply ITU and national rules as hard constraints. |
| Adoption | Customers may resist terminals, MNO integration or uncertain SLAs. | Start with one wind-turbine alarm use case, measure customer TCO and define a paid pilot with latency, availability and delivery targets. |

## 05 Next Steps

For Phase 2 in Luxembourg, Lynq will simulate one offshore or maritime corridor, comparing bent-pipe and regenerative architectures under changing visibility, gateway access, traffic load and ISL conditions.
The demo will show priority handling, Doppler/delay compensation, dynamic ISL/feeder/store-and-forward selection, QoS, latency, delivery probability, queue depth, TCO and routing compliance.

**Roles:** Davoud Jokar — Systems & digital twin · Ines Bouissou — NTN modelling & optimisation · Gambhir Sharma — Cloud, APIs & deployment · Maryam Amini — TCO, pricing, regulation & first-buyer case
