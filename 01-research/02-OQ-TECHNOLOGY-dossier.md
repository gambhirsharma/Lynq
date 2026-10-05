# 02 — OQ Technology: Company Dossier

*Compiled 18 September 2026 from public sources. See `09-SOURCES.md`. Figures are as reported; where sources conflict I say so.*

---

## 1. Snapshot

| | |
|---|---|
| **Legal name** | OQ Technology S.à r.l. |
| **Founded** | 2016, Luxembourg |
| **Founder & CEO** | Omar Qaise |
| **HQ** | Leudelange / Luxembourg |
| **Offices** | Luxembourg, Greece (OQ Technology Hellas — also a manufacturing site), Saudi Arabia, Rwanda, Australia (Sydney, opened Oct 2025) |
| **What it is** | A **satellite mobile network operator**. Not a satellite manufacturer by origin, not a hardware vendor — a *telecom operator whose towers are in orbit*, using standard 3GPP cellular protocols. |
| **Satellites in orbit** | **12** (per CEO, June 2026); 10 as of the Feb 2026 EIB announcement |
| **Core claim** | First company in the world to deliver standardised 3GPP NB-IoT connectivity from LEO satellites |
| **Current positioning** | *"A trusted, sovereign partner in D2D for European governments"* — European alternative to Starlink/AST |

---

## 2. Timeline

| Date | Event |
|---|---|
| 2016 | Founded in Luxembourg by Omar Qaise |
| 2018 | **12 patents filed** (same priority date) covering cellular-over-satellite |
| 2019–2020 | **TIGER-1**: with GomSpace on GOMX-4A/4B (6U). **26 in-orbit NB-IoT experiments**; two-way link to standard cellular devices demonstrated |
| 2021 | **Tiger-2** launched (NanoAvionics 6U) — world's first commercial nanosat delivering 5G NB-IoT coverage. Luxembourg **5G frequency test licence**; **first European 5G Satellite Test Lab** opened in Leudelange |
| 2022 | **Tiger-3**. **Series A ≈ €13M**. First USPTO patent granted |
| Dec 2022 | Two further USPTO patents: **frequency synchronisation** and **timing synchronisation** |
| Mar 2023 | Luxembourg **Space Activity Licence** granted. Announced growth from 3 → 10 satellites |
| May 2023 | **First commercial contract, ~€1M**, with an oil & gas customer |
| Jun–Aug 2023 | **Tiger-4** launched; **MACSAT** (LuxIMPULSE IOD pathfinder, NanoAvionics) prepared |
| 2024 | **MACSAT** in-orbit demonstration. Selected for **CASSINI Business Accelerator**. GSMA corporate member |
| Oct 2024 | **Series B convertible**: Luxembourg Space Sector Development Fund (SES + Luxembourg state), **Wa'ed Ventures (Aramco)**, **Phaistos Investment Fund (Greece)**. Series B target €35–40M |
| Early 2025 | **EIC Accelerator**: €2.5M grant + up to €15M equity |
| 2025 | **5NETSAT** launched as a project — "Europe's first direct-to-mobile satellite mission" (emergency SMS / broadcast alerts to unmodified 5G smartphones). Partnership with **KPN**. Australia subsidiary opened |
| **Nov 2025** | 🔑 **Luxembourg government concession** for satellite-based 5G IoT **and D2D** services — one of the first in Europe. Covers three band categories: two MSS bands (one global/complementary with terrestrial mobile, one ITU-Region-specific), a band under ITU review for WRC agenda items for satellite IoT, and a terrestrial mobile band |
| Nov 2025 | **Europe's first direct-to-mobile emergency broadcast message from space** |
| Dec 2025 | **Nordic Semiconductor** — standard off-the-shelf NB-IoT module connected to a fully integrated LEO satellite network |
| Jan 2026 | Partnerships with **Eseye** and **Monogoto** (IoT connectivity/eSIM channel plays) |
| **Feb 2026** | 🔑 **€25M EIB venture debt under InvestEU** (~$29–30M). Supports deployment of **>20 small satellites**, including the first **C-band D2D satellite**, slated for mid-2026 |
| Mar 2026 | **ESA × GSMA Foundry Excellence Award 2026** for Direct-to-Device connectivity |
| Mar 2026 | **ERMIS-1 and ERMIS-2 launched** on SpaceX Transporter-16 (Vandenberg, 30 Mar 2026), **built by OQ Technology Hellas** — Greek national programme with NKUA and the Hellenic Space Center. Used with the OQ fleet for 5G NTN IoT + D2D emergency broadcast |
| Apr 2026 | 🔑 **BEAMSAT-5G** — €1M ESA ARTES contract, OQ as prime, kicked off 3 Feb 2026: **5G beamforming** toward industrialisation |
| May 2026 | **LUXUAV partnership** — 5G NTN for UAV and **defense** applications |
| **Jun 2026** | 🔑 **Telefónica Germany D2D demonstration** — Europe's first using **terrestrial IMT spectrum from space**, "digitally sovereign" framing. Mecklenburg-Western Pomerania. Two-way text + voice messaging to standard smartphones |
| Jun 2026 | 🔑 **Europe's first drone video transmission over a 3GPP NTN LEO network using MSS S-band** (with Airbus). 3GPP NTN IoT modem in the drone, onboard edge compression, narrowband satellite uplink, European cloud |
| Sep 2026 | First Australian project: smart forest monitoring |

---

## 3. The fleet

| Series | Builder | Form factor | Notes |
|---|---|---|---|
| TIGER-1 | GomSpace (hosted on GOMX-4A/4B) | 6U | Experimental; 26 NB-IoT experiments |
| Tiger-2, -3 | NanoAvionics | 6U | First commercial NB-IoT-from-LEO |
| Tiger-4, -7, -8 | Kongsberg NanoAvionics | 6U | Electric propulsion for deployment, formation flying, EOL disposal |
| Tiger-5, -6 | Space Inventor (Denmark) | — | |
| MACSAT | NanoAvionics | 6U | LuxIMPULSE IOD; OQ's own 5G payload on 3GPP Rel-17 + in-house "cell tower stack" |
| 5NETSAT | — | — | D2D / direct-to-mobile mission |
| ERMIS-1, -2 | **OQ Technology Hellas (in-house)** | — | Launched Mar 2026; Greek national programme with NKUA/HSC |

**Payload approach:** OQ supplies the 5G payload itself — standard 3GPP Rel-17, plus OQ's **in-house developed "cell tower stack"**. This matters: OQ is not just buying a modem, it has its own base-station software in orbit. They are also **vertically integrating manufacturing** via the Greek subsidiary — payload development, AIT — explicitly to control quality and de-risk supply chains.

**Generation 2 (stated plan):** **48 satellites within 18–24 months** of mid-2026, supporting **both 5G NR and IoT** on the same platform, addressing D2D and NTN IoT simultaneously. Gen-2 is also where live drone video streaming (vs. today's compressed store-and-send) is targeted.

---

## 4. Spectrum position — their biggest strategic asset

OQ has assembled a **multi-band** strategy, which is unusual for a company this size.

| Band | Status | Use |
|---|---|---|
| **MSS S-band (~2 GHz)** | **60 MHz of rights held**; used operationally today (IoT, drone video demo) | Standardised NTN band (Rel-17). "Highly contested in Europe" |
| **C-band** | Pursuing FCC auction participation; **first C-band D2D satellite launching mid-2026** | "Compatible with current smartphones" |
| **IMT / terrestrial mobile** | Demonstrated live with Telefónica Germany (Jun 2026) | SCS-style: works with *any* existing handset |
| **European 2 GHz MSS** | Intends to apply under the new EU selection procedure | Sees the EC proceeding as "very positive in terms of enabling European players" |
| **Luxembourg concession (Nov 2025)** | Granted | Rights to operate using **OQ's priority ITU filings** under internationally coordinated frequencies and orbits |

> 🔑 **"Priority ITU filings"** is the phrase to remember. OQ filed early through Luxembourg. In a first-come-first-coordinated system, that is a durable moat, and it is why a Luxembourg-flagged operator can credibly propose a global system.

---

## 5. Intellectual property

- **12 patents filed in 2018**, all with the same priority date, subsequently granted.
- **Granted (USPTO):**
  - Frequency synchronisation for satellite cellular
  - Timing synchronisation for satellite cellular
  - "Wake-up" smart power-saving for satellite IoT devices
- **Pending (US + EU), as last publicly reported:**
  - IoT device localisation
  - 🔑 **Inter-satellite link technology** — described as keeping different base stations aware of each other and record-keeping of terminal devices connectable to different base stations
  - Satellite system design and network architecture for cellular IoT between satellites and ground stations

> 🔑 **Directly relevant to this challenge.** OQ has a *pending patent on ISL for a cellular constellation*, framed around inter-base-station awareness and device registration — i.e. exactly the Xn-over-ISL and mobility-context problem Rel-19 later standardised. **They are not asking this question idly. They already believe they have IP in this space and want to see how far the concept can be pushed.** Any proposal that treats ISL as a pure comms pipe and ignores the *signalling/context-transfer* problem will underwhelm them.

---

## 6. R&D projects and "published" work

OQ is an operator, not an academic group. There is **no significant peer-reviewed publication record under the OQ Technology affiliation** — searches of arXiv/IEEE surface adjacent academic work (NB-IoT-over-LEO synchronisation, resource allocation, NTN surveys) from universities and other vendors, not from OQ. Their public technical output is: **patents, ESA project deliverables, 3GPP participation, and press-released in-orbit demonstrations.**

Known funded R&D:

| Project | Funder | Focus |
|---|---|---|
| **MACSAT** | LuxIMPULSE / ESA | In-orbit 5G IoT pathfinder + 5G-IoT user equipment |
| **CREST-5G** | ESA ARTES 4.0, SPL "Space for 5G/6G and Sustainable Connectivity" | System-level assessment of **C-band TDD** for 5G NTN satellite D2D |
| **BEAMSAT-5G** | ESA ARTES, **€1M**, OQ prime, KO 3 Feb 2026 | **Beamforming** for next-gen satellite networks; path to industrialisation |
| **5NETSAT** | EIC Accelerator (€2.5M grant + up to €15M equity), CORDIS project 101218718 | Direct-to-mobile: emergency SMS and broadcast alerts to unmodified 5G phones |
| **Project Sentinel** | Luxembourg government (defence) | Drone-to-satellite connectivity and **interference mitigation** using 5G/NTN |

**Standards:** OQ participates in 3GPP and is a GSMA corporate member. ESA's 5G/6G white-paper series (incl. the Sept 2024 *5G Space-Based Infrastructure* white paper) is the community they publish into.

> **How to use this in a pitch:** cite CREST-5G, BEAMSAT-5G and Sentinel by name. It shows you did more than read their homepage, and it tells them your proposal plugs into work they are already funded to do.

---

## 7. Partnerships and channel

| Partner | Type |
|---|---|
| **Telefónica Germany (O2)** | MNO — D2D trial on terrestrial spectrum, "sovereign European approach" |
| **KPN** | MNO — satellite-backed 5G IoT |
| **Deutsche Telekom IoT** | MNO — global satellite 5G IoT |
| **Nordic Semiconductor** | Chipset — standard NB-IoT module onto OQ's network |
| **Airbus** | Drone/S-band NTN demonstration |
| **Eseye, Monogoto** | IoT connectivity / eSIM aggregators — channel to enterprise |
| **LUXUAV** | UAV + defence |
| **Aramco (Wa'ed Ventures)** | Investor **and** customer (oil & gas) |
| **Kongsberg NanoAvionics, Space Inventor, GomSpace, EmTroniX** | Spacecraft supply |
| **NKUA / Hellenic Space Center** | Greek national programme (ERMIS) |
| **ESA, Luxembourg Space Agency, EIB, EIC** | Institutional backing |

---

## 8. Funding stack

| Round | Amount | Source |
|---|---|---|
| Series A (2022) | ~€13M | Space/telecom investors |
| Series B convertible (Oct 2024) | Undisclosed | Luxembourg Space Sector Development Fund (SES + state), Wa'ed Ventures (Aramco), Phaistos (Greece) |
| Series B target | €35–40M | Ongoing |
| EIC Accelerator (2025) | €2.5M grant + up to €15M equity | European Innovation Council |
| **EIB venture debt (Feb 2026)** | **€25M** (~$29–30M) | InvestEU |

**Reading:** OQ is a well-supported but *capital-constrained* operator. Total disclosed funding is on the order of €60–80M. For comparison, AST SpaceMobile and Starlink operate at 10–100× this scale. **This is the single most important fact for your business case: any architecture you propose must be affordable for a company with tens, not thousands, of millions of euros.** A 500-satellite laser-meshed constellation is not a proposal to OQ — it is a proposal *past* OQ.

---

## 9. Strategic reading — what OQ is actually trying to become

1. **The sovereign European D2D operator.** Every 2026 press release uses the word "sovereign". The EU is simultaneously (a) expanding IRIS² to 348 satellites with first launches pulled forward to 2029, and (b) restructuring the **2 GHz MSS band**, proposing to split it into three blocks, one reserved for **governmental/defence use by an EU operator integrated with IRIS²**. Current holders Viasat and EchoStar expire May 2027; regulation expected 2027/28, selection 2028/29, new authorisations ~2029. **OQ is positioning to be that EU operator, or a component of it.**
2. **Standards-native, not proprietary.** Their entire differentiation is that an off-the-shelf 3GPP chip works on their network with no vendor lock-in. They will reject any proposal requiring custom waveforms or bespoke devices.
3. **Narrowband first, broadband later.** They win on low-SWaP, low-cost satellites serving low-bitrate traffic. They do not compete with AST on megabits.
4. **Vertically integrating.** In-house payload stack, in-house AIT in Greece — reducing dependence on suppliers' timelines.
5. **Defence and dual-use is the emerging margin.** Project Sentinel, LUXUAV, drone video, interference mitigation, European cloud. Government money is what closes the funding gap between €80M raised and a Gen-2 constellation.

### What this means for your proposal

| They will like | They will reject |
|---|---|
| Standards-compliant (Rel-17→19) evolution paths | Proprietary waveforms or bespoke handsets |
| Phased deployment starting from 12 satellites | "Build 400 satellites and then…" |
| Narrowband / IoT / messaging as the anchor | Broadband-to-handset ambitions |
| Store-and-forward used deliberately, not apologetically | Assuming full mesh everywhere from day one |
| European sovereignty, EU funding hooks, IRIS² adjacency | US-component-heavy designs (ITAR exposure) |
| Spectrum realism grounded in their actual holdings (S-band, C-band, IMT-via-MNO) | "We'll get spectrum somehow" |
| Defence/government as first revenue | Consumer mass-market fantasies |
