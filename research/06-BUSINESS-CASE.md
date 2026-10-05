# 06 — Business Case

> OQ's instruction, verbatim: *"identifying the **most viable initial customer segment** and revenue model, rather than attempting to monetize every segment simultaneously"* and *"reason about unit economics **per connected device or per bit** rather than assume an unconstrained budget."*
>
> This is a scoring rubric disguised as a sentence. Obey it literally.

---

## 1. The budget reality that bounds everything

| Source | Amount |
|---|---|
| Series A (2022) | ~€13M |
| Series B convertible (Oct 2024) | undisclosed; round target €35–40M |
| EIC Accelerator (2025) | €2.5M grant + up to €15M equity |
| **EIB venture debt (Feb 2026)** | **€25M** |
| **Total disclosed, order of magnitude** | **€60–80M** |

Against that: AST SpaceMobile and SpaceX operate at 10–100× this scale. **Any architecture costing more than ~€150M to reach first revenue is not a proposal OQ can act on.** Size the recommendation to the balance sheet — and say that you did. Judges from a scale-up notice.

---

## 2. Market context (use sparingly — TAM slides are a trap here)

| Market | 2026 | Forecast | CAGR |
|---|---|---|---|
| Direct-to-device satellite connectivity | ~$558M | ~$3.26B by 2034 | ~24.7% |
| Satellite IoT | ~$2.3–3.1B | $6.5B (2034) – $24.6B (2036), source-dependent | 14–23% |
| Satellite NTN | ~$0.7B | $5.3B by 2033 / $42B by 2040 | 34–36% |

*Forecasts from commercial research houses vary by 3–4× on the same market. Quote a range, cite the source, and move on. Do not build a case on them.*

**The useful observation:** satellite IoT today is ~4–5× the size of D2D and is *actually generating revenue*, while D2D is mostly promises. **The near-term money is in IoT. The near-term narrative is in D2D.** OQ needs both — IoT to pay the bills, D2D to raise the capital. Reflect that in your phasing.

---

## 3. Segment selection — score them, then choose one

| Segment | Willingness to pay | Regulatory friction | Latency tolerance | Volume | Fit to OQ today | **Verdict** |
|---|---|---|---|---|---|---|
| **Maritime IoT + vessel monitoring** | Medium-high | 🟢 **None in international waters** | High (S&F fine) | Medium | ✅ Already serving | **🏆 PHASE 1 ANCHOR** |
| **Government / defence / sovereign** | 🟢 **Very high** | Medium (but OQ has Luxembourg) | Mixed | Low volume, high value | ✅ Project Sentinel, LUXUAV | **🏆 PHASE 1 MARGIN** |
| Energy / oil & gas remote assets | High | Medium (national) | High | Medium | ✅ Aramco is investor *and* customer | Phase 1–2 |
| Logistics / asset tracking | Low per unit | Medium | Very high | 🟢 Very high | ✅ Eseye/Monogoto channel | Phase 2 — volume play |
| Agriculture / utilities | Low | Medium | Very high | High | ✅ Australia forest project | Phase 2 |
| **D2D emergency messaging (consumer)** | 🔴 Very low per user | 🔴 High — needs MNO + regulator per country | Low | 🟢 Enormous | 🟡 5NETSAT, Telefónica trial | Phase 3 — *strategic, not profitable* |
| D2D broadband to handsets | High | High | Very low | High | 🔴 Wrong satellite class | ❌ **Reject — that's AST's game** |
| Aviation connectivity | High | High | Low | Medium | 🔴 Wrong capacity class | ❌ Reject for now |

### The choice, and the argument

> **Phase 1 anchor segment: maritime and offshore IoT/asset monitoring, sold wholesale through MNOs and IoT aggregators, with government/defence as the high-margin attached segment.**

Defend it on four grounds — and note that **each ground comes from a different dimension of the challenge**, which is exactly the cross-dimensional reasoning the format rewards:

1. **Regulatory (file 05):** international waters need **no national landing rights**. It is the only large market you can legally serve on day one, worldwide, with the licences OQ already holds. Zero regulatory critical path.
2. **Technical (file 04):** the ocean is precisely where the bent-pipe gateway problem bites hardest and where store-and-forward is acceptable. **The segment that most needs the architecture is also the one most tolerant of its cheapest version.** That is a rare and valuable alignment — lead with it.
3. **Commercial:** vessels already pay for connectivity (VSAT, Inmarsat, Iridium) at prices far above IoT norms. There is an established budget line. You are displacing spend, not creating it.
4. **Strategic:** maritime domain awareness is dual-use. It is the bridge from commercial IoT to the defence/sovereign money that actually funds Gen-2 — and OQ has already stepped onto that bridge with Project Sentinel and LUXUAV.

**And say what you are rejecting:** *"We are not proposing consumer D2D as a revenue segment. At a few cents per subscriber per month for emergency messaging, it does not pay for a laser terminal. We propose it as a Phase 3 **regulatory and political asset** — it is what wins the EU 2 GHz governmental block and justifies public co-funding — not as a Phase 1 business."* That sentence alone will distinguish your team.

---

## 4. Revenue model

**Recommendation: wholesale-first, with a direct high-margin overlay.**

| Model | Mechanics | Margin | Scale speed | Use for |
|---|---|---|---|---|
| **Wholesale / roaming with MNOs** | The MNO's subscriber roams onto your NTN; standard 3GPP roaming; MNO pays per device or per byte | Low–medium | 🟢 Fast | **Default. Volume IoT.** |
| **IoT aggregator channel** (Eseye, Monogoto) | Your coverage inside their eSIM/connectivity platform | Low–medium | 🟢 Fast | Long-tail enterprise |
| **Direct enterprise** | Sell to the shipping line / oil major yourself | 🟢 High | Slow | Maritime + energy anchors |
| **Government / institutional** | Framework contracts, defence programmes, EU/ESA co-funding | 🟢 Very high | Slow | The margin engine |
| Retail consumer | Your own brand to end users | Medium | Slow, costly | ❌ Reject |

**Why wholesale first — three reasons, one of them non-obvious:**
- The MNO already owns the customer, the billing and the brand. You skip all of it.
- 🔑 **It solves the regulatory problem (file 05 §4c): the MNO holds the licence and the lawful-intercept obligation.** Market access becomes a commercial negotiation instead of a regulatory campaign.
- It is proven in this exact market: Sateliot runs wholesale-to-MNO with a patented store-and-forward roaming method; OQ already works with Deutsche Telekom IoT, KPN and Telefónica.

**Trade-off to state honestly:** wholesale means thin margins and no customer relationship. That is why the direct enterprise and government overlay matters — it is where the margin lives. Show both lines on the revenue chart.

---

## 5. Unit economics — the part they explicitly asked for

*Illustrative, order-of-magnitude, publicly-grounded. Label every assumption. The discipline of the model matters more to judges than the precision of the inputs.*

### 5.1 Cost side — a 90-satellite constellation

| Line | Assumption | Annual cost |
|---|---|---|
| Satellite build (12U–16U class, regenerative gNB + RF ISL) | €0.6M each | — |
| Launch (rideshare, e.g. Transporter) | €0.15M each | — |
| **All-in per satellite** | **~€0.75M** | — |
| **Initial deployment, 90 satellites** | | **~€68M capex** |
| **Replenishment** (5-yr life → 18 sats/yr) | 18 × €0.75M | **€13.5M/yr** |
| Ground segment (gateways, TT&C, sites, backhaul) | ~10 sites | €3M/yr |
| Network ops, NOC, conjunction management, staff | | €8M/yr |
| Spectrum, licensing, regulatory, legal | | €2M/yr |
| **Total annual operating cost at maturity** | | **~€26.5M/yr** |

Add optical cross-plane terminals on a subset (say 20 satellites at €0.5–1M each) and capex rises ~€10–20M — **which is exactly why file 04 recommends putting lasers only on a relay subset rather than all 90. The architecture choice is a business-case choice.** Make that link explicit; it is the kind of cross-dimensional reasoning the judges are looking for.

### 5.2 Revenue side — per connected device

| Segment | ARPU/device/yr | Devices needed to cover €26.5M/yr |
|---|---|---|
| Low-end asset tracking (wholesale) | €6 | **4.4 million** ❌ implausible near-term |
| Mid-tier IoT (energy, maritime sensors) | €36 | **740,000** 🟡 stretch |
| **Premium maritime / offshore monitoring** | **€120** | **220,000** 🟢 plausible |
| Defence / sovereign (per endpoint) | €1,000+ | **26,000** 🟢 very plausible |
| **Realistic blend** | **~€60** | **~440,000 devices** |

### 5.3 The three conclusions that make this a real business case

1. **A pure low-ARPU tracking play does not close.** 4.4 million devices is an order of magnitude beyond what any satellite IoT operator has. **Kill this option on your own slide** — demonstrating you can reject your own idea is worth more than any projection.
2. **A blended ~€60/device/yr portfolio needs ~440k devices at maturity.** That is ambitious but within an order of magnitude of what the market supports. State it as the target and the risk.
3. 🔑 **Defence and government break the arithmetic open.** At €1,000+ per endpoint, ~26,000 endpoints covers the entire operating cost. **This is why OQ is chasing Project Sentinel, LUXUAV and the EU 2 GHz governmental block — and your business case should say so explicitly.** The commercial IoT business provides scale, credibility and a functioning network; the government business provides the margin that funds Gen-2. Neither works alone.

### 5.4 Per-bit sanity check
A 90-satellite narrowband constellation carrying single-digit Mbps per satellite over served regions moves on the order of **tens of TB/year** fleet-wide. At €26.5M/yr that is **very roughly €1/MB** — around 1,000× the price of terrestrial mobile data.
**The lesson to state out loud: this business can never compete on price per bit. It only works where the alternative is *no connectivity at all*, or where the bit carries disproportionate value (a leak alarm, a vessel position, a distress message).** Selling per-bit is the wrong frame; sell per-device, per-asset-monitored, or per-mission. That sentence reframes the whole economic section and is the kind of thing an operator's CEO nods at.

---

## 6. Phased roadmap — each phase independently fundable

| Phase | Timing | What | Funding | Revenue engine |
|---|---|---|---|---|
| **0 — Today** | now | 12 satellites, bent-pipe + store-and-forward, S-band MSS, NB-IoT | Already funded (€25M EIB, EIC) | Enterprise IoT, oil & gas, Australia |
| **1 — Regenerative pathfinder** | 0–18 mo | 4–6 Gen-2 satellites with on-board full gNB (Rel-19) + **intra-plane RF ISL**. Prove Xn-over-ISL, on-board routing, in-orbit handover. Serve maritime IoT in international waters | ESA ARTES (BEAMSAT-5G precedent), EIC, Luxembourg defence | Maritime IoT + Project Sentinel |
| **2 — Service shell** | 18–42 mo | ~48 satellites (OQ's own stated Gen-2 target), continuous coverage at ε ≥ 10° across inhabited latitudes + shipping lanes; store-and-forward polar/remote | Series C + EIB + EU programmes | Wholesale MNO IoT at volume; enterprise |
| **3 — Mesh + sovereign D2D** | 42–72 mo | ~90 satellites; **optical cross-plane relay subset**; C-band/IMT D2D; **bid the EU 2 GHz governmental block; IRIS² interoperability** | EU institutional + defence | Government/defence margin; D2D emergency messaging as strategic asset |

**Each phase is a fundable story with its own revenue.** That is the structure European institutional funders (ESA, EIC, EIB) and a Series C investor both want, and it mirrors how OQ has actually financed itself so far. Point that out — it shows you understood the *company*, not just the problem.

---

## 7. Risk register

| Risk | Impact | Mitigation |
|---|---|---|
| EU 2 GHz timeline slips past 2029 | Removes the government-block prize | Don't put it on the Phase 1–2 critical path; it funds Phase 3 only |
| Thermal limit caps on-board processing | Forces a bigger, costlier bus | Duty-cycle the gNB over unserved regions; deployable radiators; size for a 12U–16U bus from the start |
| Optical terminal export control (ITAR) | Blocks defence sales, contradicts sovereignty pitch | European suppliers (Tesat, Mynaric) at design freeze |
| An MNO partner walks | Loses a market | Multi-partner from day one (Telefónica, KPN, DT already); aggregator channel in parallel |
| EPFD limits unchanged after WRC-27 | Constrains band options | Already assumed — don't build a case that needs relief |
| Competitor (Starlink D2C, Sateliot) reaches maritime IoT first | Erodes the anchor segment | Sovereignty + European data residency + standards-openness are defensible; price is not |
| Replenishment cost underestimated | Business case collapses | Modelled explicitly at €13.5M/yr — this is why it's in §5.1 |
| Rel-19 chipset ecosystem arrives late | Delays regenerative benefit | Phase 1 is only 4–6 satellites; Rel-17 service continues regardless |
