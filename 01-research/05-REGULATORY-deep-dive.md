# 05 — Regulatory Deep Dive

> OQ asked for *"a regulatory pathway sketch that identifies which jurisdictions and authorities must be engaged **first**, and **why**."*
> The word doing the work is **first**. They want a **sequence with a critical path**, not an inventory of regulators.

---

## 1. The five separate permissions you need (people conflate these)

| # | Permission | Granted by | What it authorises |
|---|---|---|---|
| 1 | **ITU frequency filing + coordination** | Your national administration → ITU BR | The right to use frequencies/orbits internationally, protected from later filers |
| 2 | **National space activity licence** | Your flag state (Luxembourg, for OQ) | The right to *operate a spacecraft* — liability, debris, insurance |
| 3 | **Spectrum authorisation in each served country** | National regulator (BNetzA, Ofcom, ARCEP, FCC…) | The right to radiate *into* that territory |
| 4 | **Telecom licence / market access ("landing rights")** | National telecom regulator | The right to *sell a service* there |
| 5 | **Export control clearance** | EU Dual-Use / ITAR-EAR | The right to build it with those parts and sell it to those customers |

A team that separates these cleanly is already ahead of most.

---

## 2. Where OQ already stands (use this — it's your head start)

| Permission | OQ status |
|---|---|
| ITU filings | ✅ **Priority ITU filings held via Luxembourg** — internationally coordinated frequencies and orbits |
| Space activity licence | ✅ Luxembourg, March 2023 |
| Spectrum holdings | ✅ **60 MHz of MSS S-band rights**; Luxembourg 5G test licence (2021) |
| Service concession | ✅ **Luxembourg concession for satellite 5G IoT *and* D2D, Nov 2025** — one of the first in Europe. Covers two MSS bands (one global/complementary with terrestrial mobile, one ITU-Region-specific), a band under ITU review for a WRC agenda item for satellite IoT, and a terrestrial mobile band |
| Terrestrial-spectrum-from-space | 🟡 Demonstrated with Telefónica Germany (Jun 2026) — trial, not commercial authorisation |
| EU 2 GHz MSS | 🟡 Intends to apply under the new EU procedure |
| C-band | 🟡 Pursuing FCC auction participation |

**Strategic reading:** OQ is one of the best-positioned small operators in Europe on paper permissions and one of the weakest on *market access breadth*. Their CEO named **"obtaining additional landing rights across countries"** as one of three 2026 priorities. **Your regulatory pathway should therefore be a landing-rights strategy, not a spectrum strategy.** They already largely solved spectrum.

---

## 3. The sequenced pathway (this is the deliverable)

### Phase 0 — Protect what you have (continuous, starts now)
- **ITU milestone compliance.** Filings carry bring-into-use deadlines; miss them and priority evaporates. With a phased constellation, sequencing launches to hit milestones is a *design constraint*, not an afterthought. **Name this.**
- **Article 9 coordination** with incumbent GSO and NGSO operators in your bands, ongoing.

### Phase 1 — Home base and the anchor customer (months 0–12)
**Authority: Luxembourg (ILR + Luxembourg Space Agency) — and it's already done.**
*Why first:* it is the flag state, the filing administration, the space-licence issuer, a shareholder via the Luxembourg Space Sector Development Fund, and the first defence customer (Project Sentinel). Nothing moves without it, and everything else is easier once Luxembourg has said yes. Extend the Nov 2025 concession to cover ISL operations and regenerative payloads explicitly — **an ISL mesh is arguably a new category of service and you do not want to discover that later.**

### Phase 2 — The EU regulatory prize (months 0–36, but the *filing* window is now)
**Authority: European Commission (DG CONNECT / DG DEFIS) + CEPT/ECC + national regulators.**

The **2 GHz MSS band proceeding** is the highest-value regulatory event in OQ's world and the timeline is public:

| Date | Event |
|---|---|
| 27 May 2026 | EC adopts proposed regulation for an **EU-level selection procedure** for 2 GHz MSS |
| May 2027 | Viasat and EchoStar authorisations expire (2-year extension available on request, rights frozen — no expansion, no transfer) |
| 2027–2028 | Regulation adopted |
| 2028–2029 | Selection procedures run |
| ~2029 | New authorisations granted |

The proposal splits the spectrum into **three equal blocks**, with **one-third reserved for governmental use** — critical communications, security and defence — **to be provided by an EU operator and integrated with IRIS²**. The remaining capacity is for commercial services including D2D and IoT.

> 🔑 **This is the pivot of the whole regulatory story.** There is a defined, dated, EU-level process that will hand a European operator a governmental D2D spectrum block, integrated with a €10B+ EU flagship. OQ has said it intends to apply and views the proceeding as *"very positive in terms of enabling European players."* **Any regulatory pathway you propose that does not put this on the critical path is missing the point.** And note the architectural implication: if you want that block, your system must be **IRIS²-interoperable**, which is an argument for standards-compliance and for European-sourced ISL hardware.

Also in Phase 2: work through **CEPT/ECC** for harmonised European conditions so you license once and operate across the EU, rather than 27 times.

### Phase 3 — High-value, low-friction markets (months 6–30)
Sequence by *ratio of revenue to regulatory pain*, not by market size:

1. **International waters and airspace.** 🔑 **No national licence required outside territorial seas.** Maritime IoT and vessel-tracking can be served under flag-state and ITU rules alone. *This is the single most under-used regulatory fact in NTN business cases: it is a large, well-funded market you can serve legally on day one with zero landing rights.* Put it first.
2. **Your own investors' and subsidiaries' jurisdictions**: Luxembourg, Greece (OQ Technology Hellas, ERMIS, Hellenic Space Center), Saudi Arabia (Wa'ed Ventures/Aramco — investor *and* customer), Rwanda, Australia. Relationship-led, fast, and OQ already has entities there.
3. **MNO-partner jurisdictions**: Germany (Telefónica), Netherlands (KPN), and Deutsche Telekom's footprint. 🔑 **Partnering with an incumbent MNO converts a market-access problem into a commercial negotiation** — the MNO already holds the spectrum and the licence, and it has the regulatory relationships. You become an extension of *their* network. This is the fastest route to lawful market access that exists.
4. **US**: the FCC's **SCS framework** is the world's only mature D2D regime (600/700/800 MHz, PCS 1850–1995 MHz) and the FCC approved further spectrum-sharing and D2D frameworks in May 2026. High value, but requires a US MNO partner and exposes you to ITAR considerations.

### Phase 4 — The hard jurisdictions (months 24+)
India, China, Russia, and states with strict data-localisation regimes. **Deliberately deprioritise these and say so.** Being explicit about where you will *not* operate initially is a mark of seriousness, not weakness.

---

## 4. The contradiction OQ planted — and how to answer it

> *"several administrations require local traffic routing for lawful intercept and data sovereignty, which is at odds with a pure ISL-mesh architecture."*

The conflict: an ISL mesh can carry a citizen's traffic out of their country through space to a gateway elsewhere. That defeats both **lawful intercept** (police access under warrant, a licence condition almost everywhere) and **data sovereignty/GDPR-style residency rules**.

**Most teams will note this and move on. Answer it instead. Three mechanisms, layered:**

**(a) Policy-based routing with a regulatory-domain-aware forwarding plane.**
Because the satellite hosts a full gNB, it knows the UE's identity, its registered PLMN and its geographic position (via Rel-18 network-verified UE location). Routing is therefore a **policy decision made in orbit**, not a physical accident. Define a per-country policy: *"traffic originating from UEs registered to a German PLMN within German territory must egress at an EU gateway and traverse a German-hosted UPF."* The mesh is then used for **resilience and reach**, not for arbitrary transit. **Frame the mesh as policy-constrained, not unconstrained — this single sentence dissolves the objection.**

**(b) Distributed regional gateways + local core breakout.** Terminate the user plane regionally. Traffic transits the mesh only as far as the nearest *policy-compliant* gateway, not the nearest gateway. This costs gateways, which is a real economic line item — own it.

**(c) The MNO-partnership shortcut.** Under an SCS-style arrangement the *MNO* is the licensed operator and owns the lawful-intercept obligation on its own core. You hand traffic to them. **You make it their compliance problem, and they already have the systems built.** This is by far the cheapest answer and it is a reason to prefer the wholesale business model on regulatory grounds, not just commercial ones — a nice cross-dimensional argument that judges reward.

> **The line to say out loud:** *"A regenerative gNB doesn't make sovereignty harder — it makes it enforceable. A bent-pipe satellite is a dumb mirror that can't tell whose traffic it's carrying. A gNB in orbit knows exactly who the user is, where they are, and which jurisdiction's rules apply, and can route accordingly. We're proposing a jurisdiction-aware mesh."*

That reframes OQ's stated objection into an argument *for* the architecture. It is the strongest single move available in this challenge.

---

## 5. EPFD and the GSO incumbents

- **Article 22 EPFD limits** cap NGSO interference into GSO systems. The limits were adopted provisionally at **WRC-97**, revised at **WRC-2000**, and are based on 1990s GSO characteristics and theoretical NGSO systems that were never built.
- **WRC-27 (Shanghai)** will consider ITU-R studies on revising them, but WRC-23 deliberately framed this as **"without regulatory consequences at WRC-27 itself"**, and language in the WRC-23 minutes blocks the Article 9.1 back door. **Translation: do not build a business case that depends on EPFD relief. It is not coming before 2031.**
- The incumbents (SES, Viasat, Intelsat) will defend the limits. Note that SES is a **co-investor in OQ** via the Luxembourg Space Sector Development Fund — a delicate position worth a sentence.
- **WRC-27 Agenda Item 1.5** addresses regulatory measures against unauthorised NGSO earth-station operation — relevant if your devices are mobile across borders.
- **Practical mitigation:** S-band MSS at 2 GHz is not the Ku/Ka band where the EPFD fight is fiercest, and **optical ISLs are entirely outside the EPFD regime**. Both are arguments for the architecture proposed in file 04.

---

## 6. Export control

- **EU Dual-Use Regulation (2021/821)** covers satellite and NTN/gNB technology.
- Any **US-origin component** can pull the system under **ITAR/EAR**, constraining who you may sell to and which nationals may touch the technology.
- 🔑 **Concrete design consequence:** the optical ISL terminal is the highest-risk item. Choosing **Tesat (Germany)** or **Mynaric (Germany)** over **CACI (US)** is a *regulatory* decision with a technical cost, and it is fully aligned with OQ's sovereignty positioning. Saying this in your architecture section shows you understand that regulation constrains the bill of materials, not just the licence application.
- Defence customers (Project Sentinel, LUXUAV, NATO-grade resilience) make this sharper, not softer.

---

## 7. Debris and orbital safety

- **IADC guidelines**, tightening national de-orbit deadlines (the 25-year rule is moving toward 5 years in several jurisdictions), mandatory conjunction screening and collision-avoidance.
- Design consequence: **550–600 km decays naturally in years; 1,200 km takes centuries.** Altitude selection is a compliance decision as much as a coverage one.
- OQ's Tiger satellites already carry **electric propulsion for deployment, formation flying and EOL disposal** — cite it.
- With ~90 satellites, conjunction management is a staffed, recurring operational cost. Put a line in the budget.

---

## 8. One-slide summary: the critical path

```
NOW ────────────────────────────────────────────────────────────────▶ 2029
 │
 ├─ Luxembourg: extend Nov-2025 concession to cover ISL + regenerative   [0-6 mo]  ◀ gating
 ├─ ITU: maintain filing priority, hit bring-into-use milestones         [continuous] ◀ gating
 ├─ EU 2 GHz MSS: position for the governmental block + IRIS² interop    [file 2027-28, award ~2029] ◀ the prize
 ├─ International waters: serve maritime IoT with NO landing rights      [0-6 mo]  ◀ first revenue
 ├─ MNO partners (DE, NL): convert market access into commercial deals   [6-24 mo]
 ├─ Subsidiary jurisdictions (GR, SA, AU, RW): relationship-led access   [6-30 mo]
 ├─ US FCC SCS: with a US MNO partner                                    [18-36 mo]
 └─ Deprioritised: IN, CN, RU, strict-localisation states                [not before 2029]

Export control: European ISL terminals selected at design freeze         [gating on BOM]
Debris: 550-600 km shell chosen for natural decay compliance             [gating on design]
```

**The two genuinely gating items are Luxembourg's concession scope and the ITU milestone clock.** Everything else can run in parallel. Lead your regulatory section with that sentence — it is precisely the "which first, and why" that OQ asked for.
