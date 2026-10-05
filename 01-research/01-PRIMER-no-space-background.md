# 01 — Primer: Everything in the OQ Challenge, Explained From Zero

*You do not need any space or telecom background to read this. Each section builds on the last. Terms in **bold** are the ones that appear in the challenge brief.*

---

## Part A — The problem in plain language

### A1. Why mobile coverage stops

A mobile phone talks to a **base station** — the box of electronics on a mast that your phone connects to. Its range is a few hundred metres in a city, maybe 30 km in flat countryside. To cover a country you need tens of thousands of them, each needing land, a power supply, a fibre connection back to the operator, and planning permission.

That economic model works where people are dense. It fails everywhere else. The result:

- Roughly **20% of Earth's landmass** has terrestrial mobile coverage.
- The oceans (71% of the surface) have essentially none.
- Poles, deserts, jungle, mountain, airspace over water: nothing.

So a ship's cargo sensor, a pipeline valve in the Sahara, a hiker in the Alps, or a buoy in the Atlantic simply cannot be reached by a normal cellular network. This is the gap satellites are now being pointed at.

### A2. Two different jobs people confuse

| | **IoT / M2M** | **D2D / D2C (direct-to-device / direct-to-cell)** |
|---|---|---|
| Who talks | A sensor, tracker, meter | A human's ordinary smartphone |
| Data volume | Bytes to kilobytes, minutes or hours apart | Kilobytes to megabytes, interactive |
| Tolerance to delay | Very high (hours is fine) | Low (a text can wait minutes; a call cannot) |
| Radio difficulty | Easy — narrow, slow, repeatable signal | Hard — needs far more satellite power/antenna |
| Who does it today | OQ, Sateliot, Skylo, Iridium, Globalstar | Starlink Direct-to-Cell, AST SpaceMobile, Lynk, (OQ entering) |

OQ started in column 1 and is moving into column 2. **This challenge sits at the intersection of both** — "serving any point on Earth" with a full 5G base station in orbit covers both cases.

---

## Part B — Orbits and constellations

### B1. LEO, MEO, GEO

| | Altitude | Orbital period | One-way signal delay | Sats for global coverage |
|---|---|---|---|---|
| **LEO** (Low Earth Orbit) | 300–2,000 km (typically 500–600) | ~90–100 min | ~2–7 ms | Dozens to thousands |
| **MEO** | ~8,000–20,000 km | 6–12 h | ~40–70 ms | ~10–30 |
| **GEO** (Geostationary) | 35,786 km | 24 h — appears *fixed* in the sky | ~120 ms (240 ms round trip) | 3 for near-global (no poles) |

**Why LEO for 5G:** 5G's timing rules were designed for a base station a few km away. GEO's 240 ms round trip breaks many of them and makes conversation awkward. LEO's few milliseconds is survivable. **The cost of LEO:** a satellite at 550 km moves at ~7.6 km/s and is only above your horizon for a few minutes, so you need *many* of them, and you are constantly handing users from one to the next.

### B2. Key geometry terms

- **Elevation angle (ε)**: how high above your local horizon the satellite is. 90° = straight overhead, 0° = on the horizon. Low elevation = longer path through the atmosphere, more obstruction from buildings/trees, weaker signal. NTN designs usually assume a **minimum elevation of 10°–30°**. *This single number drives constellation size more than anything else* (see file 04).
- **Footprint**: the patch of ground a satellite can serve at any instant. At 550 km with 10° minimum elevation it is roughly 3,300 km across; at 30° minimum elevation only ~1,600 km across.
- **Orbital shell / plane**: satellites are organised into rings ("planes"). A **shell** is a set of planes at the same altitude and inclination.
- **Inclination**: the tilt of the orbit relative to the equator. 53° covers where most people live but never the poles. ~87–90° (**polar / Sun-synchronous**) covers everything including the poles, but wastes capacity over empty polar regions.
- **Walker constellation**, written `T/P/F`: T satellites, P planes, F phasing. E.g. Starlink shell 1 is `1584/72/1` at 550 km, 53°. **Walker Star** (near-polar, planes spread over 180°) gives true global coverage — Iridium's 66 satellites are the classic example. **Walker Delta** (planes over 360°, inclined) is more efficient for mid-latitudes.
- **Revisit time**: if you *don't* have continuous coverage, how long until a satellite comes back over you. With ~10 satellites this is measured in hours — fine for a sensor, useless for a phone call.

### B3. The ground segment

- **Gateway / feeder link**: the big dish on the ground that connects the satellite to the operator's core network and the internet. The satellite↔gateway radio path is the **feeder link**.
- **Service link / access link**: the satellite↔user-device radio path.
- **TT&C** (Telemetry, Tracking and Command): the separate, small, very reliable link used to keep the satellite alive — health data down, commands up. Even a fully autonomous constellation needs this.

> **The core problem the challenge names:** a satellite can only pass your traffic to the internet when it can see a gateway. Over the middle of the Pacific, it can't. So either you build gateways everywhere (impossible — it's ocean), you fly enough satellites that one is always over a gateway *and* over the user simultaneously, or you let satellites talk to each other and relay the traffic to one that *can* see a gateway. That third option is the **inter-satellite link**, and it is the heart of this use case.

---

## Part C — The 5G vocabulary

### C1. 3GPP, releases, and why they matter

**3GPP** (3rd Generation Partnership Project) is the international consortium that writes the actual specifications for 2G/3G/4G/5G. If your chip follows 3GPP, it interoperates with everyone's network. Work is bundled into numbered **Releases**, frozen on a schedule.

| Release | Frozen | What it added for satellites |
|---|---|---|
| **Rel-15/16** | 2018–2020 | Baseline 5G NR. Terrestrial only. |
| **Rel-17** | 2022 | 🔑 **NR-NTN and IoT-NTN**: satellites formally become part of 5G. Doppler/delay pre-compensation, extended timing advance, ephemeris broadcast. **Transparent (bent-pipe) payloads only.** This is what OQ, Sateliot and Skylo run today. |
| **Rel-18** | 2024 | NTN enhancements: coverage, mobility, network verified UE location, above-2-GHz bands for NR-NTN. |
| **Rel-19** | **Dec 2025** | 🔑🔑 **Regenerative payload — a full gNB on the satellite.** Plus native inter-satellite links (Xn over ISL), on-board routing, and **store-and-forward**. *This is the standards event that makes this challenge possible.* |
| **Rel-20** | ~2027 | 5G-Advanced final phase + 6G studies; deeper NTN integration. |
| **Rel-21** | ~2028+ | First normative 6G. |

**Why this matters for your pitch:** the challenge is not speculative fiction. 3GPP froze the regenerative architecture nine months before this event. You are designing the *first commercial exploitation* of a just-standardised capability. Say that out loud.

### C2. The network boxes

- **UE** (User Equipment) — the phone, sensor or modem.
- **gNB** — the 5G base station ("g" for gNodeB, the 5G successor to 4G's eNB). **Putting a gNB on a satellite is the entire subject of this challenge.**
- **5GC / 5G Core** — the brain on the ground: authentication, subscriber database, session management, routing to the internet.
- **Interfaces** (the standard "cables" between boxes):
  - **Uu** — UE ↔ gNB (the radio link).
  - **NG** — gNB ↔ 5G Core.
  - **Xn** — gNB ↔ gNB (peer base stations, used for handover and coordination). 🔑 **Rel-19 lets Xn run over an inter-satellite link.**
  - **F1** — inside a split gNB, between its two halves (below).

### C3. NB-IoT vs NR — the two flavours

- **NB-IoT** (Narrowband IoT): a deliberately tiny, rugged version of cellular. 180 kHz channels, single-tone uplink, heavy repetition, ~10-year battery life, ~100 kbps at best, often far less. **Because it is narrow and repetitive, it closes a link to a small satellite with modest power.** This is OQ's and Sateliot's foundation.
- **NR** (New Radio): full 5G. Wide channels, high throughput, low latency. **Needs vastly more satellite EIRP and antenna area** — this is why AST SpaceMobile's satellites unfold antennas the size of a tennis court while OQ's fit in a shoebox.

### C4. Three ways to build a satellite payload

This is the single most important technical choice in the challenge.

```
(1) TRANSPARENT / BENT-PIPE          satellite = mirror
    UE ──Uu──▶ [sat: amplify+shift] ──▶ gateway ──▶ gNB ──▶ 5GC
    • Simple, low power, radiation-tolerant, cheap, flight-proven
    • Needs a gateway in view AT THE SAME TIME as the user → coverage = gateway footprint
    • Every signal makes a double hop (up-down-up-down) → more latency
    • This is 3GPP Rel-17, and what essentially every commercial NTN runs today

(2) SPLIT gNB (e.g. option 2, or 7.2x)   satellite = half a base station
    UE ──Uu──▶ [sat: gNB-DU] ──F1 over feeder──▶ [ground: gNB-CU] ──▶ 5GC
    • DU (Distributed Unit) = radio + physical layer, on the satellite
    • CU (Central Unit) = the higher protocol layers (incl. RRC), on the ground
    • Sounds like a nice compromise BUT: the DU is where most of the power and
      complexity lives anyway, and RRC signalling still has to cross the feeder
      link constantly → latency and a hard gateway dependency remain
    • 3GPP debated this for four meetings and rejected it for Rel-19

(3) REGENERATIVE / FULL gNB IN SPACE     satellite = a real base station
    UE ──Uu──▶ [sat: complete gNB] ──Xn over ISL──▶ [other sats] ──NG──▶ 5GC
    • Satellite decodes, schedules, terminates HARQ, does beam management itself
    • Native Xn over inter-satellite links → inter-satellite handover, on-board
      routing, "network in space"
    • Enables STORE-AND-FORWARD: carry the data until a gateway is in view
    • Can even terminate UE-to-UE calls entirely in orbit
    • Cost: far more on-board processing → power, heat, radiation exposure, mass
    • 🔑 3GPP Rel-19 (Dec 2025) chose THIS
```

**HARQ** (Hybrid Automatic Repeat reQuest) is 5G's rapid retransmission mechanism. In a bent-pipe design the acknowledgement has to travel all the way to the ground gNB and back, so the round trip is doubled; with a gNB on board, it terminates in orbit. Same for the **random access** procedure a device uses to first attach. This is a concrete, quotable performance argument for regenerative.

### C5. The physics you must compensate for

Because the base station is moving at 7.6 km/s, three things break:

1. **Doppler shift** — the frequency you receive is not the frequency transmitted. At 2 GHz and LEO velocities, tens of kHz of shift — far more than a normal cellular receiver tolerates. Fixed by **pre-compensation**: the satellite broadcasts its **ephemeris** (its predicted position and velocity) so the device can calculate and cancel the shift itself. *OQ holds granted US patents on exactly this — frequency and timing synchronisation.*
2. **Propagation delay and its variation** — 5G's **timing advance** mechanism assumed a few km. NTN needed an **extended timing advance** and a broadcast common delay.
3. **Handover churn** — a satellite is overhead for only a few minutes, so every user is handed over constantly. With a gNB in space, handovers can happen satellite-to-satellite over Xn rather than via the ground.

### C6. Antennas and beams

- **Phased array**: an antenna made of many small elements whose signals are electronically combined, so the beam can be steered and shaped *without moving anything*. Essential when you are flying over users at 7.6 km/s.
- **Multi-beam**: one satellite paints many separate spot beams on the ground, reusing frequencies between distant beams to multiply capacity.
- **Earth-fixed vs Earth-moving beams**: either the beams stay pointed at a fixed patch of ground while the satellite flies over (steering constantly, fewer cell changes for the user), or they sweep along with the satellite (simpler, but the user's "cell" changes every few seconds). Rel-17 supports both. *OQ's ESA **BEAMSAT-5G** project, started Feb 2026, is precisely about this.*
- **EIRP** (Effective Isotropic Radiated Power): how much power you effectively put toward the user. Higher EIRP = more reach = more solar panel, more heat.
- **G/T**: a figure of merit for a receiver (antenna gain ÷ system noise). Higher = better at hearing a weak phone.

---

## Part D — Inter-satellite links (ISL)

The satellites talk to each other, forming a mesh network in orbit.

### D1. Optical vs RF

| | **Optical (laser) ISL** | **RF ISL (Ka / V / W band)** |
|---|---|---|
| Throughput | Multi-Gbps to 100 Gbps | Typically tens to hundreds of Mbps, up to a few Gbps |
| Pointing | Very hard — microradian **PAT** (Pointing, Acquisition, Tracking); the beam is a pencil | Much easier — wider beam |
| Spectrum licence | **Not required** (optical is unregulated) — a real regulatory advantage | Required; ITU coordination, interference risk |
| Interception | Extremely hard (pencil beam) — a security selling point | Easier to intercept/jam |
| SWaP | Heavier, more power, more cost; smallest units ~1.5U/1.7 kg (e.g. Tesat SCOT20, ~100 Mbps), LEO-mesh class ~12 kg for 10 Gbps (SCOT80) | Lighter and cheaper at low rates |
| Maturity | Now industrial: SpaceX flies 3–4 terminals per Starlink (~9,000 satellites by mid-2026, >5,000 terminals, 100 Gbps class); Tesat opened a ~100 units/month line in Aug 2024; Mynaric CONDOR Mk3; CACI CICADA/SkyLight for CubeSats (150 Mbps @ 2,000 km in a low-SWaP unit) | Mature but less deployed for mesh |

### D2. Topology

- **Same-plane (intra-plane) links**: neighbours in the same ring. Geometrically *easy* — the relative position barely changes, so pointing is nearly static.
- **Cross-plane (inter-plane) links**: to satellites in neighbouring rings. Geometrically *hard* — relative geometry changes constantly, and near the poles in a Walker Star the "seam" (where counter-rotating planes meet) has satellites closing at double orbital velocity, which usually forces you to break the link entirely.
- A classic **"+Grid"** mesh gives each satellite 4 links: fore, aft, port, starboard. Iridium has done this with RF since the 1990s; Starlink does it with lasers today.

### D3. Store-and-forward

If there is no path to a gateway right now — polar, mid-ocean, or the mesh is thin — a regenerative satellite can **buffer the data on board and deliver it on a later pass**. Latency becomes minutes to hours. Useless for a phone call; perfectly fine for a container tracker reporting twice a day. Rel-19 standardises this for IoT UEs. Sateliot has a patented Store & Forward roaming method; OQ operates in the same regime today with ~12 satellites.

> **The strategic insight:** store-and-forward and ISL mesh are *alternatives* that trade cost against latency. ISL mesh = expensive, instant. Store-and-forward = nearly free, delayed. **A serious answer to this challenge uses both, matched to the service.**

---

## Part E — Spacecraft engineering constraints

- **SWaP** (Size, Weight and Power) — the fundamental budget. A **6U CubeSat** (roughly a large shoebox, 10×20×30 cm) masses ~8–12 kg and generates tens of watts orbit-average. An **ESPA-class smallsat** (100–200 kg) manages hundreds of watts. A regenerative gNB is a *computer* running full-time, so it eats into this hard.
- **Thermal dissipation** — in vacuum you cannot convect heat away; you can only radiate it. Every watt the processor burns must leave through a radiator panel, which costs area and mass. This, not raw power, is often what caps on-board processing.
- **Radiation tolerance** — space radiation flips bits (SEU, single-event upset) and degrades silicon over years (TID, total ionising dose). Radiation-hardened processors run roughly a decade behind commercial ones in performance-per-watt. The pragmatic middle path is commercial (COTS) parts with watchdogs, ECC memory and redundancy.
- **Design life and replenishment** — a LEO smallsat typically has a 5–7 year design life; atmospheric drag and radiation set the limit. A constellation of N satellites with a 5-year life needs **N/5 replacements launched every year, forever**. This is the number most student business cases forget. It is also why the *unit* cost of a satellite matters more than the total programme cost.
- **TRL** (Technology Readiness Level, 1–9): 1 = idea, 4 = validated in the lab, 6 = demonstrated in a relevant environment, 9 = flight-proven in operation. The brief says **TRL 4–6**: the building blocks (NR-NTN waveform, optical ISL terminals) are proven separately, but nobody has flown *a global mesh of full gNBs*. That is the gap you are asked to close.

---

## Part F — The regulatory world

### F1. ITU — who gets to use which frequencies

The **ITU** (International Telecommunication Union, a UN agency) coordinates global spectrum via the **Radio Regulations**, updated at the **World Radiocommunication Conference (WRC)** every ~4 years (next: **WRC-27**, Shanghai).

- You cannot file with the ITU directly. You file **through a national administration** — for OQ, Luxembourg. That country then "owns" the filing and defends it. This is a large part of why satellite companies choose the jurisdiction they do.
- **Article 9** — the coordination procedure: publish your intended system, then negotiate with every operator whose system you might interfere with.
- **Article 22 / EPFD** (Equivalent Power Flux Density) — hard limits on how much interference a **non-geostationary (NGSO)** constellation may cause to **geostationary (GSO)** systems. The limits date from WRC-97/2000, designed around 1990s assumptions, and the GSO incumbents (SES, Viasat, Intelsat) fight hard to keep them while NGSO operators want them revisited. **WRC-27 is studying them**, with the outcome deliberately framed as "without regulatory consequences at WRC-27 itself."
- **Milestones**: a filing is not forever. You must bring a proportion of your constellation into use on a schedule (the ITU milestone regime) or lose the rights. This creates real deployment pressure.
- **Spectrum types relevant here:**
  - **MSS (Mobile Satellite Service)** — spectrum allocated to satellites for mobile users. The **2 GHz MSS band (1980–2010 / 2170–2200 MHz)** is the one that matters in Europe. OQ states it holds **60 MHz of MSS S-band rights**.
  - **IMT spectrum** — the ordinary terrestrial mobile bands your phone already uses, licensed to MNOs nationally. Using it from space is the "**SCS**" model below.

### F2. How to serve an ordinary phone — two doors

1. **MSS band, phone must support it.** Clean regulatory story, but handsets must implement the NTN band (Rel-17 n255/n256 etc.). Chip support is arriving (Nordic Semiconductor, Qualcomm, MediaTek).
2. **Terrestrial MNO spectrum from space — "Supplemental Coverage from Space" (SCS).** Any existing phone works, because it is already on that band. But you need a *partnership with an operator in each country*, and national regulatory permission. The US **FCC** created a formal SCS framework (600/700/800 MHz, PCS 1850–1995 MHz). Europe has no equivalent single framework yet — it is done country by country. **OQ's Telefónica Germany trial (June 2026) is exactly this model.**

### F3. Landing rights and the ISL paradox

Radio spectrum authorisation is not enough — you also need a **telecom licence / market access ("landing rights") in every country you serve**. Here is the trap the brief flags explicitly:

> A pure ISL mesh can carry a user's traffic out of their country, through space, and into a gateway somewhere else entirely. Many states require **local traffic breakout** for **lawful intercept** (police access under warrant) and **data sovereignty**. *That requirement is in direct conflict with the architecture that makes "any point on Earth" possible.*

This is the single most interesting regulatory tension in the challenge, and most teams will miss it. (See file 05 for how to answer it.)

### F4. The rest

- **Space debris / orbital safety**: IADC guidelines, tightening de-orbit deadlines (the 25-year rule is moving toward 5 years), conjunction screening and collision-avoidance obligations. For a large constellation this is a recurring operational cost, not a checkbox.
- **Export control**: satellite and gNB technology can fall under the **EU Dual-Use Regulation**; any US-origin component can drag the whole system into **ITAR/EAR**. Concretely: choosing a US laser terminal can constrain who you may sell to.
- **National space licence**: separate from telecom. Luxembourg granted OQ its Space Activity Licence in March 2023 and a full **concession for satellite-based 5G IoT and D2D services in November 2025**.

---

## Part G — The money

### G1. Where revenue comes from

- **Wholesale / roaming with MNOs** — you are not the retail brand. The MNO's subscriber roams onto your satellite network; the MNO pays you per device or per byte. Low friction, low margin, fast scale. *This is Sateliot's and largely OQ's model.*
- **Direct IoT subscription** — you sell connectivity to the enterprise (a mining company, a shipping line) yourself. Higher margin, higher sales cost.
- **Government / defence / institutional contracts** — large, sticky, high-margin, slow to win, and increasingly driven by *sovereignty* (a European government wanting a European, non-US-dependent network). OQ has explicitly positioned here: a Luxembourg defence contract ("Project Sentinel"), the LUXUAV drone partnership, and the EU's IRIS² and 2 GHz MSS proceedings.

### G2. Cost drivers

| Driver | Why it hurts |
|---|---|
| Payload complexity | Regenerative gNB + ISL terminals raise per-satellite cost several-fold over bent-pipe |
| Constellation size | Continuous global coverage is a steep function of minimum elevation angle (see file 04) |
| Launch + replenishment | Not a one-off. ~N/5 satellites per year, forever |
| Ground gateways | Sites, land, licences, backhaul, staff — in many jurisdictions |
| Spectrum access | Either ITU filings and coordination, or revenue share with MNOs |

### G3. The discipline they asked for

> *"reason about unit economics per connected device or per bit rather than assume an unconstrained budget."*

Meaning: pick a unit (a connected device-year, or a delivered megabyte), and show cost and revenue *in that unit*, including replenishment. A satellite IoT device might be worth €1–5/month; a D2D emergency-messaging subscriber a few cents/month across a huge base; a government contract millions per year for a handful of users. These are wildly different businesses and they cannot all be served by one architecture at once. **Choosing is the deliverable.**

---

## Part H — Fast glossary

| Term | Meaning |
|---|---|
| 3GPP | Body that writes the 5G specifications |
| ARPU | Average Revenue Per User |
| Bent-pipe | Satellite as a dumb mirror; = transparent payload |
| CU / DU | Central Unit / Distributed Unit — the two halves of a split gNB |
| D2D / D2C | Direct-to-Device / Direct-to-Cell |
| EIRP | Effective Isotropic Radiated Power — transmit strength |
| Ephemeris | Predicted satellite position/velocity, broadcast to devices |
| EPFD | Equivalent Power Flux Density — the NGSO-into-GSO interference limit |
| Feeder link | Satellite ↔ ground gateway |
| gNB | 5G base station |
| GSO / NGSO | Geostationary / Non-geostationary satellite orbit |
| G/T | Receiver figure of merit |
| HARQ | 5G's fast retransmission mechanism |
| IMT | Terrestrial mobile spectrum |
| ISL | Inter-Satellite Link |
| ITU | UN agency coordinating global spectrum |
| LEO | Low Earth Orbit |
| MNO | Mobile Network Operator |
| MSS | Mobile Satellite Service spectrum |
| NB-IoT | Narrowband IoT — the small, rugged cellular flavour |
| NR | New Radio — full 5G |
| NTN | Non-Terrestrial Network |
| PAT | Pointing, Acquisition, Tracking (for laser links) |
| Regenerative | Satellite processes and decodes; hosts a gNB |
| SCS | Supplemental Coverage from Space (terrestrial spectrum used from orbit) |
| Service link | Satellite ↔ user device |
| SWaP | Size, Weight and Power |
| TRL | Technology Readiness Level (1–9) |
| TT&C | Telemetry, Tracking and Command |
| UE | User Equipment (phone/sensor) |
| Walker | Standard constellation geometry notation T/P/F |
| WRC | World Radiocommunication Conference |
| Xn | Interface between two gNBs — over ISL in Rel-19 |
