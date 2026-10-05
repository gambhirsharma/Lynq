<!-- Converted from `NEOSPACE Challenge OQ.docx` -->

# Use case Title: AnyPoint-NTN: Global gNB-Onboard LEO Constellation for Ubiquitous 5G NR-NTN

## Category selected

- Next-Gen Downstream

## Problem Description / Context

Terrestrial mobile networks cover roughly a fifth of the Earth's landmass and a small fraction of the oceans, leaving billions of people and vast maritime, aviation, polar, and remote areas outside 3GPP coverage. 3GPP Release 17/18 introduced NR-NTN and IoT-NTN, moving beyond bent-pipe relay toward satellites that host a full or split gNB (regenerative payload) capable of onboard scheduling, HARQ termination, and beam management. This use case asks teams to define the operational scenarios and requirements for a constellation of satellites carrying an onboard gNB capable of serving any point on Earth, and to assess the inter-satellite link (ISL) architecture and the regulatory and economic constraints associated with it.

Why it matters: direct-to-device/direct-to-cell service, global IoT/M2M, maritime and aviation connectivity, disaster and emergency response, and defense/NATO-grade resilient communications all depend on eliminating terrestrial dead zones without waiting for local network build-out.

Existing constraints: bent-pipe NTN systems depend on a visible gateway feeder link, which limits effective coverage to the gateway's footprint; reaching "any point on Earth" therefore requires either a very dense constellation or an inter-satellite mesh that can relay traffic without a local gateway; LEO satellites have short ground-station contact windows; regenerative gNB payloads are bounded by size, weight, power (SWaP), radiation tolerance and thermal dissipation.

Who is affected: mobile network operators seeking NTN roaming and coverage extensions; IoT/MM verticals (maritime, agriculture, utilities, asset tracking) needing defined service reach; governments and defense/NATO users needing beyond-line-of sight, resilient comms; and end-users in oceanic, polar, and other underserved regions requiring coverage availability.

Reference points: 3GPP TR 38.821 / TR 22.822 NTN study material as the standards baseline.

## Key Constraints

### Technical Dimension

- Onboard gNB architecture must be either a full-stack "regenerative" gNB-in-space, a split option (e.g., option 2 or 7.2x with a central unit on the ground), or a bentpipe relay; regenerative reduces feeder-link dependency but increases payload complexity, power draw, and thermal load.

- Standards baseline must include 3GPP Release 17 NR-NTN and IoT-NTN, Release 18 enhancements, and ongoing Release 19 NTN work on regenerative payloads, ISL-aware mobility, and store-and-forward operation.

- Multi-team, steerable phased-array antennas are required for Earth coverage, with onboard beam management and handover across fast-moving LEO.

- Precise time/frequency synchronization and Doppler/delay pre-compensation are required, using ephemeris broadcast and extended timing advance per the 3GPP NTN specifications, to keep NR frame timing valid from a moving platform.

- An ISL subsystem is required to relay traffic and signaling between satellites without a local gateway: choose optical/laser ISL (multi-Gbps, precise pointing/acquisition/tracking, higher SWaP and cost) or RF ISL (Ka/V/W-band, lower throughput, simpler pointing, lower cost) and define the topology as sameplane or cross-plane mesh.

- Onboard packet routing and buffering are required for a "network in space" capable of store-and-forward over polar and oceanic coverage gaps. Radiation-hardened processing, a per-satellite SWaP budget, thermal dissipation for an active digital payload, and satellite design life/replenishment cadence must be defined.

- The minimum viable ground segment must include feeder-link gateways for Telemetry, Tracking, and Command and any gateway-based traffic offload that complements the ISL mesh.

- Indicative TRL must be 4–6, individual building blocks (NR-NTN waveform, optical ISL terminals) are flight-proven, but full gNB-onboard integration with a global ISL mesh has few operational precedents.

### Regulatory Dimension

- Spectrum coordination under the ITU Radio Regulations (Article 9 / Article 22 EPFD limits protecting GSO systems from NGSO interference), filed through a national administration, covering feeder-link/gateway spectrum and any accesslink band.

- Direct-to-device service typically requires spectrum access through terrestrial MNO partnerships (“supplemental coverage from space”-type arrangements) rather than a dedicated global MSS allocation; harmonize these arrangements across countries, since this is a known obstacle.

- Space debris mitigation and orbital safety compliance (IADC guidelines, evolving deorbit-timeline requirements, conjunction/collision-avoidance obligations) for a large constellation.

- Market access and landing rights: obtain national telecom licenses in every country served, since a global gNB-in-space service can technically bypass in-country ground infrastructure — several administrations require local traffic routing for lawful intercept and data sovereignty, which is at odds with a pure ISL-mesh architecture.

- Export control exposure: satellite and NTN/gNB technology may fall under the EU Dual-Use Regulation and, where US-origin components are involved, ITAR/EAR.

- Cross-jurisdictional considerations are central to this use case by design (“any point on Earth”), requiring simultaneous coordination with incumbent GSO/NGSO operators and multiple national regulators.

### Economic Dimension

Target market/customer segments: MNOs seeking NTN roaming or coverage extension (direct-to-device), IoT/M2M verticals (maritime, logistics, agriculture, utilities, asset tracking), government/defence and disaster-response users, and maritime/aviation connectivity providers.

- Comparable approaches teams should benchmark against include bent-pipe NTN IoT constellations, regenerative direct-to-cell systems, and GEO-based NTN IoT, each reflecting a different trade-off among payload complexity, coverage, and cost.

- Cost drivers to reason about qualitatively rather than with fixed figures: payload complexity (regenerative gNBs plus ISL terminals raise per-satellite costs relative to bent-pipe), constellation size needed for continuous global coverage, launch and replenishment cadence, ground-gateway footprint, and spectrum-access costs, where MNO partnerships are required.

- Plausible revenue paths to anchor a business model: wholesale capacity/roaming agreements with MNOs, subscription-based IoT connectivity, and government/institutional contracts; teams should reason about unit economics per connected device or per bit rather than assume an unconstrained budget.

## Expected Outcomes

OQ Technology is interested in seeing the following key constraints first:

1. A defined constellation architecture, including satellite count, orbital shell(s), and ISL topology, sized to a stated coverage and latency target, with an explicit trade-off discussion between regenerative and bent-pipe payloads, and between optical and RF ISL.

2. A regulatory pathway sketch that identifies which jurisdictions and authorities must be engaged first, and why.

3. A first-order business case identifying the most viable initial customer segment and revenue model, rather than attempting to monetize every segment simultaneously.
