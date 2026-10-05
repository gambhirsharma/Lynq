# 07 — Competitive Landscape

> OQ asked teams to benchmark against *"bent-pipe NTN IoT constellations, regenerative direct-to-cell systems, and GEO-based NTN IoT."* This file gives you the comparison set.

---

## 1. The map

```
                    NARROWBAND (IoT / messaging)        BROADBAND (to handset)
                    ────────────────────────────        ──────────────────────
  LEO, many sats    Sateliot  (~40, Rel-17, S&F)        Starlink Direct-to-Cell
                    OQ Technology (12 → 48)             AST SpaceMobile (BlueBird)
                    Lynk (10, SMS)                      Amazon Leo
                    Iridium (66, proprietary→NTN)
                    Globalstar / Apple

  GEO / MEO         Skylo (over Viasat/Inmarsat L-band) Viasat, SES
                    Omnispace (S-band)
```

**OQ sits in the top-left quadrant and is trying to add a European-sovereign D2D capability without moving to the top-right.** Your proposal should respect that.

---

## 2. The competitors that matter

### Sateliot 🇪🇸 — the closest analogue
- ~40 LEO satellites, **3GPP Rel-17 NB-IoT NTN**, sun-synchronous.
- **Patented Store & Forward** two-step authentication method enabling standard MNO roaming adapted to LEO NTN.
- Cloud-native virtualised 5G core (Magma on AWS).
- **Wholesale-to-MNO model**; first 5G roaming connection from space with Telefónica (2023). Applied to the FCC for US operation.
- **Why it matters:** this is the business model OQ competes with directly, and it validates wholesale-roaming + store-and-forward as commercially real. **Benchmark against them, don't ignore them.** Your differentiation is regenerative/Rel-19 and ISL — Sateliot is still Rel-17 bent-pipe with S&F.

### Skylo 🇺🇸 — the asset-light contrarian
- **Owns no satellites.** Runs Rel-17 NTN service over Viasat/Inmarsat **GEO** L-band.
- Two-way messaging; deep chipset partnerships (Qualcomm, MediaTek); already in shipping phones.
- **Why it matters:** proof that you can win the D2D messaging market **without a constellation at all**. It is the strongest argument *against* building what this challenge proposes. **Address it head-on:** Skylo's GEO latency (~240 ms round trip) and lack of polar coverage are real, and it depends on someone else's satellites — no sovereignty, no control. But if a team doesn't mention Skylo, they haven't done the landscape.

### AST SpaceMobile 🇺🇸 — the opposite architecture
- ~200+ large satellites planned; FCC approval for 248. Targets **~30 Mbps 5G to unmodified smartphones**. Huge unfoldable phased arrays.
- Needs **~45–60 satellites overhead** for continuous service, targeted by end-2026. MNO spectrum via AT&T, Vodafone.
- **Why it matters:** the cautionary tale. Broadband-to-handset requires a spacecraft class and a capital stack (billions) that OQ does not have. **Explicitly rejecting AST's segment is a strength of your proposal, not a gap.**

### Starlink Direct-to-Cell 🇺🇸 — the elephant
- ~9,000 satellites by mid-2026, 3–4 optical terminals each, >5,000 laser terminals flying at 100 Gbps class with >99% link uptime.
- Already operational D2C messaging with T-Mobile and others.
- **Why it matters:** they have *already built* the ISL mesh this challenge describes, at a scale nobody can match. **You cannot out-build them. You can only out-position them:** European sovereignty, EU data residency, standards openness without vendor lock-in, and institutional/defence customers who will not buy American. **This is exactly OQ's stated strategy, and your proposal should reinforce it rather than pretend the gap doesn't exist.**

### Lynk 🇺🇸
- ~10 satellites, direct-to-smartphone SMS over terrestrial MNO spectrum. Small, early, similar scale to OQ.

### Iridium 🇺🇸 — the proof that ISL works
- **66 satellites, 780 km, polar, with a fully operational RF cross-link mesh since the late 1990s.** True global coverage including poles.
- **Why it matters:** cite it as the existence proof for the mesh architecture *and* as the calibration point for your constellation-sizing maths (file 04 §2.1). It also shows the model's limits: ~30 years of operation, and it has never been cheap.

### Kepler Communications 🇨🇦 — the data-relay-as-a-service play
- First commercial demonstration of **SDA-compatible optical inter-satellite links** on orbit; partnerships with Skyloom/Axiom.
- **Why it matters:** an alternative to building your own mesh — **buy transit on someone else's optical relay network.** Worth one line in your trade study as a genuine make-vs-buy option, and it is a cheap way to get Phase 3 capability without Phase 3 capex.

### IRIS² 🇪🇺 — not a competitor, a gravitational field
- EU flagship after Galileo and Copernicus. Implementation agreement with the SpaceRISE consortium signed **7 Aug 2026**, expanded to **348 satellites** (330 LEO + 18 MEO), first launches pulled forward to **2029**.
- Governmental, defence, emergency services + commercial broadband.
- **Why it matters:** the EU's 2 GHz MSS proposal reserves a third of the band for **governmental use by an EU operator integrated with IRIS²**. **IRIS² is the thing OQ wants to be adjacent to, not compete with.** Design for interoperability and say so.

### Omnispace 🇺🇸
- S-band NTN, 2 GHz MSS. A direct spectrum-neighbour and potential coordination counterparty for OQ.

---

## 3. Where OQ can actually win — the four defensible positions

1. **European sovereignty.** The only European commercial operator with flying 5G NTN satellites, priority ITU filings via Luxembourg, a national concession for D2D, European manufacturing (Greece) and an EU institutional funding stack (ESA, EIC, EIB). **In a market where the alternatives are American, this is not marketing — it is a procurement requirement for EU governments.**
2. **Standards purity.** Off-the-shelf 3GPP chips work on OQ's network with no vendor lock-in — and they have demonstrated it with Nordic Semiconductor. Lynk and AST both need more bespoke arrangements.
3. **Multi-band optionality.** MSS S-band (60 MHz held) + C-band (first D2D satellite mid-2026) + IMT-via-MNO (Telefónica). Very few operators of this size have three independent routes to a handset.
4. **Early-mover IP.** 12 patents from a 2018 priority date covering synchronisation, power saving, localisation and **inter-satellite links for cellular constellations** — filed years before Rel-19 standardised the architecture.

## 4. Where OQ cannot win — say this out loud
- **Capacity per bit.** Starlink and AST win on throughput, always.
- **Capital scale.** ~€80M vs billions.
- **Consumer brand.** Apple/Globalstar and T-Mobile/Starlink own the consumer D2D narrative.
- **Launch cadence.** Dependent on rideshare.

**A proposal that names all four of these and then designs around them will be more convincing than one that claims OQ can beat Starlink.**
