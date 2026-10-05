# 08 — Proposal: **AnyPoint-NTN / "Tiered Reach"**

*A concrete answer to OQ's three Expected Outcomes, sized to a company with ~€80M raised and 12 satellites flying.*

---

## 0. The pitch in five bullets

> - **"Any point on Earth" is a service catalogue, not a coverage map.** We deliver three tiers — Continuous, Mesh-Relayed, and Store-and-Forward — and sell each at a different price with a different SLA.
> - **~90 satellites in two shells at 550–600 km, ε ≥ 10°**, every satellite a **Rel-19 full regenerative gNB**, intra-plane **RF ISL** on all, **European optical cross-plane relay on a 20-satellite subset**.
> - **The regenerative gNB is what makes sovereignty enforceable**, not what threatens it: a base station in orbit knows the user's identity, location and jurisdiction, so routing becomes a policy decision. We call it a **jurisdiction-aware mesh**.
> - **First revenue from maritime and offshore IoT in international waters** — the only large global market needing **zero landing rights** — with government/defence as the margin engine.
> - **Four phases, each independently fundable**, starting with a 4–6 satellite regenerative pathfinder that fits an ESA ARTES-scale contract.

---

## 1. Service definition — the reframe that carries the whole proposal

The brief asks for "any point on Earth". A literal reading (continuous coverage everywhere at 30° elevation) costs **~516 satellites** (file 04 §2.2) and is unbuildable at OQ's scale. But the brief *also* asks for store-and-forward over "polar and oceanic coverage gaps". Those two requirements are only compatible if coverage is **graded by service**.

| Tier | Coverage | Latency | Mechanism | Sold to |
|---|---|---|---|---|
| **T1 — Continuous** | Inhabited latitudes (±60°) + major shipping lanes | < 150 ms one-way | Direct gateway or short mesh path | D2D messaging, defence, real-time monitoring |
| **T2 — Mesh-relayed** | Mid-ocean, remote, no gateway in view | < 250 ms one-way | Multi-hop ISL to nearest policy-compliant gateway | Maritime, offshore energy, aviation |
| **T3 — Store-and-forward** | Polar, extreme remote, degraded mesh | ≤ 90 min (contractual SLA) | On-board buffering, Rel-19 S&F | Low-rate sensors, environmental, tracking |

**Every point on Earth is served at *some* tier. That is a defensible "any point on Earth" claim, and it is what an operator actually sells.** Lead the presentation with this table.

---

## 2. Outcome 1 — Constellation architecture

### 2.1 Design point (state it in the first 90 seconds)

> **~90 satellites, two shells, 550–600 km, minimum elevation 10°, full regenerative Rel-19 gNB on every satellite, hybrid RF/optical ISL.**

| Parameter | Value | Why |
|---|---|---|
| Altitude | **550–600 km** | Natural de-orbit in years (debris compliance); below the inner belt; 6.1 ms one-way at ε=10° |
| Minimum elevation | **10°** | 🔑 The lever: 10° → 30° would multiply the constellation **4.4×** (118 → 516). The NB-IoT uplink closes at **+10.6 dB SNR** at ε=10° with an 18 dBi satellite antenna (file 04 §4.1), so narrowband *can* afford low elevation where voice cannot |
| **Shell A (service)** | ~70 sats, Walker Delta, ~60–65° inclination | Covers inhabited latitudes and the great-circle shipping lanes efficiently; avoids wasting capacity over empty poles |
| **Shell A′ (polar)** | ~20 sats, near-polar/SSO | Thin polar and high-latitude capability at T2/T3; also the natural home for the gateway-facing relay role |
| **Total** | **~90 satellites** | Against ~118 for naive continuous global at ε=10°; the saving comes from serving the poles at T3 rather than T1 |
| Design life | 5 years | → **18 satellites/year replenishment, forever** (in the business case, file 06 §5.1) |

### 2.2 Payload trade — decision and reasoning

**Decision: full regenerative gNB (3GPP Rel-19), narrowband, on every satellite; plus a transparent wideband repeater path in parallel.**

| Option | Verdict |
|---|---|
| Bent-pipe | ❌ Coverage is structurally limited to gateway footprint ∩ user footprint. Cannot deliver "any point on Earth" at any constellation size we can afford. Retained only as a parallel wideband repeater path. |
| Split gNB (CU on ground) | ❌ **Rejected by 3GPP for Rel-19 after four TSG RAN meetings**, and rightly: the DU holds the RF and PHY where most of the power and complexity live, so you pay nearly the regenerative price while RRC still round-trips over the feeder link. Worst of both. |
| **Full regenerative gNB** | ✅ **Chosen.** Removes the feeder-link coverage constraint; HARQ and random access terminate in orbit; native Xn over ISL; enables Rel-19 store-and-forward and in-orbit UE-to-UE; frozen in the standard Dec 2025, so the chipset ecosystem is coming to us. |

**Honest cost of the decision:** power, thermal dissipation and radiation exposure all rise. Our mitigations: the gNB is **narrowband only** (tens of watts, not kilowatts); it is **duty-cycled** — throttled over unserved ocean and at night, with heavy processing scheduled into eclipse; we fly a **12U–16U bus** rather than 6U to afford radiator area; and we use **COTS processors with ECC, scrubbing and watchdogs under a small rad-hard supervisor**, accepting a 5-year life rather than chasing 10.

### 2.3 ISL trade — decision and reasoning

**Decision: RF intra-plane on all 90 satellites + low-SWaP European optical cross-plane on a ~20-satellite relay subset.**

The argument, in order:

1. **Throughput is not the constraint.** A narrowband satellite serving a 1,664 km-radius footprint carries **single-digit Mbps**. A 10 Gbps laser terminal would be ~1000× oversized. **Anyone who picks optical for bandwidth hasn't done the traffic estimate.**
2. **Intra-plane geometry is nearly static** — relative positions barely change, pointing is trivial, links are permanent. RF is more than sufficient and far cheaper. Iridium has run exactly this since the 1990s.
3. **Cross-plane is where optical earns its cost** — and not for bandwidth. It earns it on **(a) no spectrum licence required**, which keeps the backhaul entirely outside the ITU/EPFD regime and matters enormously to a spectrum-poor operator; **(b) pencil-beam security**, un-interceptable and un-jammable, which is a chargeable feature for the defence segment; **(c)** it avoids adding cross-link interference into an already contested S-band environment.
4. **Only ~20 satellites need it.** Putting optical terminals on all 90 adds ~€70M of capex for capability that most satellites never use. Concentrating the relay role cuts that to ~€10–20M. **This is an architecture decision made for business-case reasons, and we say so.**
5. **European suppliers only** (Tesat SCOT-class, Mynaric CONDOR). 🔑 **A US-origin terminal would drag the system under ITAR/EAR and destroy the sovereignty proposition that is OQ's entire market position.** Export control here is a bill-of-materials decision, not a paperwork decision.

**Topology:** permanent intra-plane "+" links; **intermittent, ephemeris-scheduled** cross-plane links (dropped at the Walker seam where closing velocities double). Routing is **deterministic and pre-computed** — the topology is perfectly predictable from ephemeris, so routing tables for the next N minutes are computed on the ground and uploaded, rather than run as a reactive protocol in orbit. That removes a large chunk of on-board complexity and power.

### 2.4 The part OQ will care most about: mobility, not pipes

OQ's own pending ISL patent is about *"keeping different base stations aware of each other and record-keeping of terminal devices connectable to the different base stations."* So we address the control plane explicitly:

- **Xn-C over ISL** for handover preparation and **UE context transfer** between satellite gNBs — the UE's security keys and session state follow it across the sky.
- **Buffer forwarding** during inter-satellite handover so in-flight data follows the UE instead of being dropped — critical when a handover happens every few minutes.
- **Ephemeris-driven, pre-computed routing tables**, uploaded ahead of time.
- **Rel-19 store-and-forward** as the graceful degradation mode when the mesh is partitioned, rather than as a failure.

### 2.5 Ground segment (minimum viable)
- **~10 gateway sites** placed for policy compliance, not just geometry (see §3) — EU, Greece, Gulf, Australia, Rwanda/Africa, plus partner-hosted sites.
- **TT&C** kept separate and simple; it must work even when the mission payload doesn't.
- **5G core on the ground**, cloud-native, with **regional user-plane breakout (UPF)** for data-residency compliance.

### 2.6 Latency budget (mid-Atlantic sensor → Frankfurt cloud, no gateway in view)

| Segment | Delay |
|---|---|
| UE → satellite (ε=10°) | 6.1 ms |
| ~8 intra-plane ISL hops (30 sats/plane) | ~39 ms |
| 2 cross-plane hops | ~10 ms |
| Satellite → European gateway | 6.1 ms |
| Gateway → core → customer cloud | 5–20 ms |
| On-board processing/scheduling | 10–30 ms |
| **Total one-way** | **~75–110 ms** |

**Compare: bent-pipe with no gateway in view = no service at all.** That single comparison is the justification for the entire architecture. Put it on one slide.

---

## 3. Outcome 2 — Regulatory pathway

**The two genuinely gating items are Luxembourg's concession scope and the ITU milestone clock. Everything else runs in parallel.**

| Priority | Authority | Action | Why first |
|---|---|---|---|
| **1** | **Luxembourg (ILR + LSA)** | Extend the Nov-2025 concession to explicitly cover **ISL operation and regenerative payloads** | Flag state, filing administration, space-licence issuer, shareholder and first defence customer. **An ISL mesh may be a new service category — discover that now, not in year three.** |
| **1** | **ITU BR (via Luxembourg)** | Maintain filing priority; **sequence launches to hit bring-into-use milestones** | Priority filings are OQ's durable moat and they expire if unused. This makes launch scheduling a regulatory constraint. |
| **2** | **None — international waters** | Serve maritime IoT immediately | 🔑 **No national landing rights required outside territorial seas.** The only large global market legally addressable on day one. This is the regulatory reason the maritime segment is our anchor. |
| **3** | **European Commission (DG CONNECT/DEFIS) + CEPT/ECC** | Position for the **EU 2 GHz MSS governmental block**; design for **IRIS² interoperability** | The EC proposal (27 May 2026) reserves one-third of the band for governmental use by an EU operator integrated with IRIS². Regulation 2027–28, selection 2028–29, award ~2029. **This is the prize — but it funds Phase 3, so keep it off the Phase 1–2 critical path.** |
| **4** | **MNO-partner regulators (DE, NL)** | Convert market access into commercial deals with Telefónica, KPN, DT | 🔑 The MNO already holds the spectrum, the licence **and the lawful-intercept obligation**. Market access becomes a negotiation, not a campaign. |
| **5** | **Subsidiary jurisdictions** (GR, SA, AU, RW) | Relationship-led national authorisations | OQ already has legal entities and, in Saudi Arabia, an investor who is also a customer |
| **6** | **FCC (US)** | SCS framework, with a US MNO partner | Mature D2D regime, high value — but ITAR exposure |
| **—** | **IN, CN, RU, strict-localisation states** | **Deliberately deprioritised** | Saying where you will *not* go is a mark of seriousness |

### 3.1 Answering the contradiction OQ planted

> *"a global gNB-in-space service can technically bypass in-country ground infrastructure — several administrations require local traffic routing for lawful intercept and data sovereignty, which is at odds with a pure ISL-mesh architecture."*

**Our answer, and the strongest single argument in this proposal:**

> *"A regenerative gNB doesn't make sovereignty harder — it makes it **enforceable**. A bent-pipe satellite is a dumb mirror; it cannot tell whose traffic it is carrying. A gNB in orbit knows exactly who the user is, where they are (Rel-18 network-verified UE location), and which jurisdiction's rules apply — so routing becomes a **policy decision**, not a physical accident. We are not proposing an unconstrained mesh. We are proposing a **jurisdiction-aware mesh**."*

Implemented in three layers:
1. **Policy-based forwarding in orbit** — per-country rules bound to the UE's registered PLMN and verified position (e.g. *traffic from a German-registered UE on German territory must egress at an EU gateway through a German-hosted UPF*).
2. **Regional gateways with local user-plane breakout** — traffic transits the mesh to the nearest **policy-compliant** gateway, not merely the nearest one. This costs gateway sites; we budget for ~10.
3. **The wholesale shortcut** — under an MNO/SCS arrangement, the MNO is the licensed operator and already owns lawful intercept on its own core. **This is a regulatory argument for the wholesale business model, not just a commercial one.**

### 3.2 Two further regulatory design consequences
- **EPFD:** assume **no relief**. WRC-27 will study Article 22 limits but WRC-23 framed it explicitly as "without regulatory consequences at WRC-27 itself." Mitigations are architectural: S-band MSS is not the Ku/Ka battleground, and **optical ISLs sit entirely outside the EPFD regime**.
- **Debris:** 550–600 km decays naturally in years (compliant by design); 1,200 km takes centuries (rejected for that reason, among others). OQ's Tiger satellites already fly electric propulsion for EOL disposal.

---

## 4. Outcome 3 — Business case

### 4.1 The segment, and the four reasons

> **Phase 1 anchor: maritime and offshore IoT / asset monitoring, sold wholesale via MNOs and IoT aggregators, with government and defence as the attached high-margin segment.**

1. **Regulatory:** international waters need **no landing rights**. Zero regulatory critical path to first global revenue.
2. **Technical:** 🔑 the ocean is exactly where the bent-pipe gateway problem bites hardest **and** where store-and-forward is acceptable. **The segment that most needs this architecture is also the most tolerant of its cheapest version.** That alignment is rare and it is the core of our case.
3. **Commercial:** vessels already buy connectivity (VSAT, Inmarsat, Iridium) at prices well above IoT norms. We displace an existing budget line rather than creating one.
4. **Strategic:** maritime domain awareness is dual-use — the bridge from commercial IoT to the defence money that funds Gen-2, and OQ is already on that bridge (Project Sentinel, LUXUAV).

**What we explicitly reject:** consumer D2D as a Phase 1 revenue segment. At a few cents per subscriber-month for emergency messaging it does not pay for a laser terminal. **We propose it as a Phase 3 regulatory and political asset — it is what wins the EU 2 GHz governmental block and justifies public co-funding — not as a business.** And we reject broadband-to-handset outright: that is AST's segment and it needs a different spacecraft class and a different capital stack.

### 4.2 Unit economics

**Cost, at maturity (90 satellites):**

| Line | Annual |
|---|---|
| Replenishment: 18 sats/yr × €0.75M all-in (build + rideshare launch) | **€13.5M** |
| Ground segment (~10 gateways, TT&C, backhaul) | €3M |
| Network ops, NOC, conjunction management | €8M |
| Regulatory, spectrum, legal | €2M |
| **Total** | **~€26.5M/yr** |

*Initial deployment capex ~€68M; optical relay subset adds ~€10–20M.*

**Revenue, per connected device per year:**

| Blend | ARPU | Devices to break even |
|---|---|---|
| Low-end tracking only | €6 | 4.4M ❌ **we kill this option ourselves** |
| Premium maritime/offshore | €120 | 220,000 🟢 |
| Defence/sovereign endpoint | €1,000+ | **~26,000** 🟢 |
| **Realistic blend** | **~€60** | **~440,000 devices** |

**The three conclusions:**
1. A pure low-ARPU tracking play **does not close** — 4.4M devices is an order of magnitude beyond anything achieved in satellite IoT. We rule it out on our own slide.
2. The blended portfolio needs **~440k devices** at maturity. Ambitious, but the right order of magnitude.
3. 🔑 **Defence breaks the arithmetic open: ~26,000 sovereign endpoints cover the entire operating cost.** Commercial IoT provides scale, credibility and a working network; government provides the margin that funds Gen-2. **Neither works alone — and that is precisely the strategy OQ is already executing.**

**Per-bit reality check:** ~€1/MB, roughly 1,000× terrestrial mobile. **This business can never compete on price per bit. It works only where the alternative is no connectivity at all, or where a single bit carries disproportionate value — a leak alarm, a vessel position, a distress message.** Sell per asset monitored or per mission, never per byte.

### 4.3 Phasing — each phase independently fundable

| Phase | Time | Build | Funded by | Earns from |
|---|---|---|---|---|
| **0** | now | 12 sats, Rel-17 bent-pipe + S&F | EIB €25M, EIC | Enterprise IoT, oil & gas |
| **1** | 0–18 mo | **4–6 regenerative pathfinders + intra-plane RF ISL.** Prove Xn-over-ISL, in-orbit handover, on-board routing | ESA ARTES (BEAMSAT-5G precedent), EIC, Luxembourg defence | Maritime IoT (no landing rights) + Project Sentinel |
| **2** | 18–42 mo | **~48 satellites** — matches OQ's own stated Gen-2 target. T1 continuous across inhabited latitudes + shipping lanes | Series C, EIB, EU programmes | Wholesale MNO IoT at volume |
| **3** | 42–72 mo | **~90 satellites + optical cross-plane relay subset**; C-band/IMT D2D; bid the **EU 2 GHz governmental block**, IRIS² interoperable | EU institutional + defence | Government margin; D2D as strategic asset |

Phase 1 is deliberately sized to an ESA ARTES-scale contract, because that is how OQ has historically financed exactly this kind of step (MACSAT, CREST-5G, BEAMSAT-5G).

---

## 5. What would make us abandon this

An honest closing slide, and one most teams won't have:

- If **Rel-19 chipsets slip past 2029**, the regenerative advantage is theoretical and Phase 2 should stay Rel-17 bent-pipe with store-and-forward.
- If the **EU 2 GHz governmental block goes to a consortium that excludes small operators**, Phase 3's funding model collapses and the constellation should stop at ~48.
- If **thermal analysis shows the regenerative gNB cannot be duty-cycled within a 16U bus**, the platform class — and therefore the entire cost model — changes, and the business case must be rebuilt.
- If **maritime IoT ARPU proves to be €30 rather than €120**, the anchor segment is wrong and energy/defence must lead instead.

---

## 6. The seven sentences to actually say on stage

1. *"'Any point on Earth' isn't a coverage map — it's a service catalogue with three tiers, and we price each one differently."*
2. *"Minimum elevation angle, not orbit, is what sets constellation cost: ten degrees to thirty multiplies our satellite count by 4.4. Narrowband lets us afford ten."*
3. *"3GPP froze the regenerative full-gNB architecture in December 2025. We're not proposing research — we're proposing the first commercial exploitation of a nine-month-old standard."*
4. *"We chose optical cross-links for three reasons, and bandwidth isn't one of them: no spectrum licence, no interception, and no EPFD exposure."*
5. *"A gNB in orbit doesn't threaten sovereignty — it makes it enforceable. We're proposing a jurisdiction-aware mesh."*
6. *"Our first market needs no landing rights anywhere in the world, because it's the open ocean."*
7. *"Twenty-six thousand sovereign endpoints pay for the whole constellation. Four million trackers don't. That's why we're not selling trackers first."*
