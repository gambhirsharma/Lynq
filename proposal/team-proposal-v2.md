# Lynq NTN-Pulse

**Challenge:** OQ Technology - AnyPoint-NTN: Global gNB-Onboard LEO Constellation for Ubiquitous 5G NR-NTN
**Category:** Next-Gen Downstream
**Team:** Lynq - Davoud Jokar, Ines Bouissou, Gambhir Sharma, Maryam Amini

## 1. Executive Summary

Lynq NTN-Pulse is a software-defined digital twin and policy engine for OQ Technology's regenerative gNB-onboard LEO constellation. It governs industrial traffic across onboard gNB, feeder/ISL paths, gateways, 5G Core and cloud applications. A 3GPP-aligned model applies policies for QoS, latency, availability, data residency, spectrum and cost. **Design point: ~90 satellites in two 550–600 km shells, 10° minimum elevation, a full regenerative gNB on every satellite, RF intra-plane ISL plus an optical cross-plane relay subset, and three service tiers: Continuous (<150 ms), Mesh-relayed (<250 ms), Store-and-forward (≤90 min).** The first beachhead is offshore energy and maritime operations. Lynq adds the software layer that makes regenerative NTN capacity measurable and deployable.

## 2. Problem & Opportunity

**Status Quo: The Bent-Pipe Limit.** Traditional transparent payloads relay radio signals but require a visible ground gateway and feeder link for network processing, routing and terrestrial-core access. If the gateway is outside the footprint, geographically blocked, nationally restricted or overloaded, service degrades through delay, inefficient routing or loss of connectivity.

This affects offshore wind farms, energy platforms, vessels and pipelines. Their traffic needs different treatment: alarms and control commands require priority, while telemetry, video and bulk files can tolerate delay.

A regenerative gNB moves selected RAN and Layer 2/3 functions into orbit, but introduces Doppler and delay, handovers, intermittent feeder access, gateway selection, ISL routing and onboard compute limits. Lynq provides the policy layer that decides whether traffic is delivered immediately, routed, edge-processed or stored for later downlink.

## 3. Proposed Direction

**Technical angle.** Lynq combines:
- **Digital twin:** Models satellite position, coverage, gateway visibility, feeder/ISL state, terminal location, traffic demand and onboard compute.
- **Policy engine:** Assigns traffic classes to available paths using QoS, latency, reliability, residency and cost.
- **NTN model and dashboard:** Covers timing, beam management, handover, link budgets, scheduling, queues, predicted outages and route decisions.

**Constellation (sized with the twin).** ~70 satellites in a Walker Delta service shell (~60–65°) over inhabited latitudes and shipping lanes, plus ~20 near-polar satellites for high latitudes. A 10° rather than 30° minimum elevation cuts the count about 4× and narrowband links still close; at a 5-year life, ~18 replacements per year.

**Payload trade.** Full regenerative gNB: bent-pipe cannot serve users with no gateway in view, and split gNB (options 2/7.2x) keeps most RF/PHY power onboard while RRC still round-trips over the feeder. Power, thermal and radiation costs are mitigated by a narrowband gNB, duty-cycling over empty ocean and COTS processing under a rad-hard supervisor.

The data path is industrial terminal → regenerative onboard gNB → policy engine → ISL/feeder → authorised gateway and 5G Core → enterprise application. Example: mid-Atlantic platform → Frankfurt cloud in ~75–110 ms one-way over ISL, versus no service on bent-pipe. The design uses 3GPP Rel-17 as the NTN baseline, incorporates Rel-18 enhancements and keeps a Rel-19-ready roadmap.

It evaluates ISL topology (optical/laser vs. RF Ka/V/W-band): optical links offer high capacity and low RF interference but require precise acquisition, pointing and tracking; RF links provide different acquisition and availability characteristics but add spectrum, antenna and interference constraints. Narrowband traffic needs only single-digit Mbps per satellite, so **we choose RF intra-plane ISL on all satellites** (near-static geometry, proven by Iridium) **and optical cross-plane on ~20 relay satellites** (no spectrum licence, hard to intercept), from European suppliers to avoid ITAR/EAR.

The system implements advanced Doppler/delay pre-compensation from moving platforms using applicable 3GPP Rel-17/18/19 procedures. AI supports traffic forecasting, anomaly detection and resource prioritisation; deterministic timing, link-budget and safety controls remain authoritative.

**Regulatory angle.** The Consultant's Dilemma is that a local ground gateway may be technically attractive but unavailable because of national restrictions, data-residency rules or licensing. A regenerative gNB knows the user's identity, PLMN and verified location, so Lynq applies routing policy onboard and sends each flow through an authorised ISL/feeder path only to a policy-compliant gateway with local user-plane breakout. Under MNO partnerships, the MNO keeps lawful intercept on its own core.

The compliance layer treats ITU Radio Regulations Article 9 coordination and Article 22 EPFD limits as hard design constraints (feeder-link masks, gateway exclusion zones), together with applicable PFD/EIRP conditions and national authorisations. It supports EU-hosted processing, encryption, key ownership, data minimisation, pseudonymisation and controlled GDPR retention. Sovereignty is built into routing.

**Engagement sequence:** (1) Luxembourg ILR/LSA, extending OQ's Nov-2025 concession to ISL and regenerative operation; (2) ITU BR via Luxembourg, for priority filings; (3) international waters, needing no landing rights; (4) North Sea regulators and MNO partners for coastal coverage; (5) EC/CEPT for EU 2 GHz MSS, off the critical path.

**Business angle.** The first buyer is an offshore energy operator or offshore wind O&M provider. Lynq reduces blind spots, improves high-priority alarm delivery and lowers dependence on dedicated VSAT and fixed gateways.

Revenue combines integration fees, monthly subscriptions by assets and traffic class, usage charges for data/priority QoS, and MNO wholesale or roaming. Mature opex including replenishment is ~€26.5M/yr: break-even at ~220k offshore assets at €120/yr, or ~26k sovereign/defence endpoints at €1,000+/yr. At ~€1/MB we price per asset, never per byte. The business case compares TCO with VSAT, private LTE and manual inspection baselines, benchmarked against Sateliot, Skylo, Starlink D2C/Lynk and Iridium. Consumer D2D is not a first target. Expansion markets include maritime logistics, UAV/drone telemetry and defence reconnaissance.

## 4. Key Assumptions & Risks

- **Payload risk:** Final power, compute, radiation and RAN-interface limits may differ. *Mitigation:* Use modular, payload-independent policies with cloud/gateway fallback; validate an OQ interface checklist.
- **ISL/regulatory risk:** Final ISL, gateway and spectrum choices may change. *Mitigation:* Simulate optical/RF ISLs, limited gateway visibility and store-and-forward; apply ITU and national rules as hard constraints.
- **Adoption risk:** Customers may resist terminals, MNO integration or uncertain SLAs. *Mitigation:* Start with one wind-turbine alarm use case, measure customer TCO and define a paid pilot with latency, availability and delivery targets.

## 5. Next Steps

For Phase 2 in Luxembourg, Lynq will simulate one offshore or maritime corridor and compare bent-pipe and regenerative architectures under changing visibility, gateway access, traffic load and ISL conditions. The demonstration will show priority handling, Doppler/delay compensation, dynamic ISL/feeder/store-and-forward selection, QoS, latency, delivery probability, queue depth, TCO and routing compliance.

**Roles:** Davoud Jokar — systems & digital twin; Ines Bouissou — NTN modelling & optimisation; Gambhir Sharma — cloud, APIs & deployment; Maryam Amini — TCO, pricing, regulation & first-buyer case.
