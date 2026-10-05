Lynq NTN-Pulse
Challenge: OQ Technology - AnyPoint-NTN: Global gNB-Onboard LEO Constellation for Ubiquitous 5G NR-NTN
Category: NextGen Downstream
Team: Lynq - Davoud Jokar, Ines Bouissou, Gambhir Sharma, Maryam Amini
1. Executive Summary
Lynq NTN-Pulse is a software-defined digital twin and policy engine for OQ Technology’s regenerative gNB-onboard LEO constellation. It governs industrial traffic across onboard gNB, feeder/ISL paths, gateways, 5G Core and cloud applications. A 3GPP-aligned model applies policies for QoS, latency, availability, data residency, spectrum and cost. The first beachhead is offshore energy and maritime operations. Lynq adds the software layer that makes regenerative NTN capacity measurable and deployable.
2. Problem & Opportunity
Status Quo: The Bent-Pipe Limit. Traditional transparent payloads relay radio signals but require a visible ground gateway and feeder link for network processing, routing and terrestrial-core access. If the gateway is outside the footprint, geographically blocked, nationally restricted or overloaded, service degrades through delay, inefficient routing or loss of connectivity.
This affects offshore wind farms, energy platforms, vessels and pipelines. Their traffic needs different treatment: alarms and control commands require priority, while telemetry, video and bulk files can tolerate delay.
A regenerative gNB moves selected RAN and Layer 2/3 functions into orbit, but introduces Doppler and delay, handovers, intermittent feeder access, gateway selection, ISL routing and onboard compute limits. Lynq provides the policy layer that decides whether traffic is delivered immediately, routed, edge-processed or stored for later downlink.
3. Proposed Direction
Technical angle. Lynq combines:
Digital twin: Models satellite position, coverage, gateway visibility, feeder/ISL state, terminal location, traffic demand and onboard compute.
Policy engine: Assigns traffic classes to available paths using QoS, latency, reliability, residency and cost.
NTN model and dashboard: Covers timing, beam management, handover, link budgets, scheduling, queues, predicted outages and route decisions.
The data path is industrial terminal → regenerative onboard gNB → policy engine → ISL/feeder → authorised gateway and 5G Core → enterprise application. The design uses 3GPP Rel 17 as the NTN baseline, incorporates Rel 18 enhancements and keeps a Rel 19-ready roadmap.
It evaluates ISL Topology (Optical/laser vs. RF Ka/V/W-band): optical links offer high capacity and low RF interference but require precise acquisition, pointing and tracking; RF links provide different acquisition and availability characteristics but add spectrum, antenna and interference constraints. The topology remains a configurable scenario.
The system implements Advanced Doppler/delay pre-compensation from moving platforms using applicable 3GPP Rel 17/18/19 procedures. AI supports traffic forecasting, anomaly detection and resource prioritisation; deterministic timing, link-budget and safety controls remain authoritative.
Regulatory angle. The Consultant’s Dilemma is that a local ground gateway may be technically attractive but unavailable because of national restrictions, data-residency rules or licensing. A regenerative gNB lets Lynq apply routing policy onboard and send traffic through an authorised ISL/feeder path to an approved European core or cloud, bypassing a restricted gateway where legally permitted.
The compliance layer enforces ITU Radio Regulations Article 9 & Article 22 EPFD limits, applicable coordination, PFD/EIRP conditions and national authorisations. It supports EU-hosted processing, encryption, key ownership, data minimisation, pseudonymisation and controlled GDPR retention. Sovereignty is built into routing.
Business angle. The first buyer is an offshore energy operator or offshore wind O&M provider. Lynq reduces blind spots, improves high-priority alarm delivery and lowers dependence on dedicated VSAT and fixed gateways.
Revenue combines integration fees, monthly subscriptions by assets and traffic class, usage charges for data/priority QoS, and MNO wholesale or roaming. The business case compares TCO with VSAT, private LTE and manual inspection baselines. Expansion markets include maritime logistics, UAV/drone telemetry and defence reconnaissance.
4. Key Assumptions & Risks
Payload risk: Final power, compute, radiation and RAN-interface limits may differ. Mitigation: Use modular, payload-independent policies with cloud/gateway fallback; validate an OQ interface checklist.
ISL/regulatory risk: Final ISL, gateway and spectrum choices may change. Mitigation: Simulate optical/RF ISLs, limited gateway visibility and store-and-forward; apply ITU and national rules as hard constraints.
Adoption risk: Customers may resist terminals, MNO integration or uncertain SLAs. Mitigation: Start with one wind-turbine alarm use case, measure customer TCO and define a paid pilot with latency, availability and delivery targets.
5. Next Steps
Phase 1 requires a credible two-page concept, not a complete operational MVP.
For Phase 2 in Luxembourg, Lynq will simulate one offshore or maritime corridor and compare bent-pipe and regenerative architectures under changing visibility, gateway access, traffic load and ISL conditions. The demonstration will show priority handling, Doppler/delay compensation, dynamic ISL/feeder/store-and-forward selection, QoS, latency, delivery probability, queue depth, TCO and routing compliance.
Maryam, TCO, pricing, regulation and the first-buyer case.Davoud systems and the digital twin; Ines, NTN modelling and optimisation; Gambhir, cloud, APIs and deployment; 
