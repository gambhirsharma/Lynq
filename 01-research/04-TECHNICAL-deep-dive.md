# 04 — Technical Deep Dive

*All numbers below are computed from first principles with the method shown, so you can defend or re-derive them. They are order-of-magnitude design aids, not a substitute for STK/orbital simulation.*

---

## 1. Payload architecture trade

### 1.1 The three options, scored

| Criterion | Bent-pipe (transparent) | Split gNB (CU on ground) | **Regenerative (full gNB)** |
|---|---|---|---|
| 3GPP status | Rel-17 ✅ deployed | Considered, **rejected** for Rel-19 | **Rel-19, frozen Dec 2025** ✅ |
| Gateway dependency | **Total** — coverage = gateway footprint ∩ user footprint | High — F1/RRC signalling still crosses the feeder link constantly | **Low** — only for NG to the core, and that can route via ISL |
| ISL support | None meaningful | Proprietary, non-standard | **Native Xn over ISL** |
| Store-and-forward | No | No | **Yes (Rel-19 for IoT UEs)** |
| Latency | Double hop; HARQ and random access round-trip to the ground | RRC round trips to ground CU | HARQ/RACH terminate **in orbit** |
| UE-to-UE in orbit | No | No | **Yes** |
| On-board processing | Minimal (filter, amplify, frequency shift) | DU: RF + PHY — i.e. most of the power anyway | Full stack |
| Power / thermal | Low | High (DU dominates) | High |
| Radiation risk | Low | High | High |
| Per-satellite cost | Low | High | Highest |

**Why 3GPP rejected the split:** the DU holds the RF and physical layer — where most of the complexity and power consumption live — so moving only the CU to the ground saves little, while RRC termination on the ground forces constant F1 traffic across the feeder link. You pay the regenerative price and keep the bent-pipe dependency. The debate ran across four TSG RAN meetings; CU/DU support started near 40% and collapsed to consensus for the full gNB by Dec 2023.

### 1.2 The recommendation to make

**Do not choose one. Choose a hybrid, and say why.**

- **Regenerative full gNB** is the right target architecture and is now the standardised one. Argue it on three grounds: (a) it is the only option that removes the feeder-link coverage constraint; (b) HARQ/RACH terminating in orbit is a measurable latency and capacity win; (c) it is where the standard, and therefore the chipset ecosystem, is going.
- **But** the *payload* should be **band- and mode-graded**: a narrowband NB-IoT/NR-light gNB is a few-watts-to-tens-of-watts software load that fits a smallsat today. A full wideband NR gNB with a large phased array is a hundreds-of-watts-to-kilowatt problem that changes the spacecraft class entirely.
- **Design conclusion:** put a **full regenerative gNB for narrowband services** on every satellite from Gen-2, and keep a **transparent wideband path** in parallel for high-rate traffic where a gateway is in view. This is cheap (the transparent path is a repeater), and it means you never have to fly the kilowatt-class digital payload.

---

## 2. Constellation sizing — with the arithmetic

### 2.1 The geometry

For satellite altitude `h` and minimum user elevation angle `ε`:

```
Earth-central half-angle:   ψ = arccos( (Re/(Re+h)) · cos ε ) − ε          [Re = 6371 km]
Ground footprint radius:    r = Re · ψ            (ψ in radians)
Slant range:                d = √( (Re·sin ε)² + 2·Re·h + h² ) − Re·sin ε
Spherical cap solid angle:  Ω = 2π(1 − cos ψ)
Ideal (perfect-tiling) N:   N_ideal = 4π / Ω
Practical N:                N ≈ 2 × N_ideal
```

**Where the ×2 comes from:** spherical caps cannot tile a sphere without overlap, and a real Walker-Star "streets of coverage" layout wastes more. **Sanity check against reality:** Iridium at h = 780 km, ε ≈ 8.2° gives ψ = 19.9° and N_ideal = 33.4. Iridium flies **66**. Packing efficiency = **0.51**, i.e. exactly a factor of ~2. The heuristic is calibrated against a flying system — say that when challenged.

### 2.2 The results table (compute this yourselves in the room; it takes 10 lines of Python)

| Altitude | Min elevation | ψ (°) | Footprint radius (km) | Slant range (km) | One-way delay (ms) | N_ideal | **N practical** |
|---|---|---|---|---|---|---|---|
| 550 km | **10°** | 14.97 | 1,664 | 1,815 | 6.05 | 59 | **~118** |
| 550 km | 20° | 10.12 | 1,125 | 1,294 | 4.31 | 129 | ~257 |
| 550 km | 25° | 8.46 | 941 | 1,123 | 3.75 | 184 | ~368 |
| 550 km | **30°** | 7.14 | 793 | 993 | 3.31 | 258 | **~516** |
| 600 km | 10° | 15.84 | 1,761 | 1,932 | 6.44 | 53 | ~105 |
| 600 km | 30° | 7.68 | 853 | 1,075 | 3.59 | 223 | ~446 |
| 1,200 km | 10° | 24.03 | 2,672 | 3,131 | 10.44 | 23 | **~46** |
| 1,200 km | 30° | 13.22 | 1,470 | 1,999 | 6.67 | 75 | ~151 |

### 2.3 The four conclusions to draw from that table

1. **Minimum elevation angle is the whole ballgame.** At 550 km, going from 10° to 30° multiplies the constellation by **4.4×**. Every degree you can shave off ε through better antenna design, more repetitions, or accepting lower availability is worth millions of euros. *Constellation cost is driven by a radio design parameter, not by an orbital one.* This is the single best insight to open your technical section with.
2. **Altitude buys coverage cheaply — and costs you elsewhere.** 1,200 km at 10° needs **~46** satellites vs ~118 at 550 km: a 2.5× saving. But: longer slant range (3,131 km → ~10.4 ms, and +4.8 dB of path loss vs 550 km), you sit inside the inner Van Allen belt's lower edge (worse radiation, shorter electronics life), and **de-orbit from 1,200 km takes centuries without propulsion** — a debris-compliance dealbreaker under tightening rules. 1,200 km is the "cheap" answer that a good judge will attack. *You can still use it — as a sparse high shell dedicated to ISL relay and store-and-forward, where latency doesn't matter and the satellites carry propulsion — but you must address de-orbit head-on.*
3. **Nobody serious closes global continuous coverage at 30° with a startup budget.** ~500 satellites. Don't.
4. **Narrowband IoT tolerates low elevation far better than voice.** Repetition and long transmission time intervals buy back link margin, so NB-IoT can work at ε = 10° where a voice call could not. This is precisely why an OQ-shaped company should anchor on narrowband.

### 2.4 A defensible design point

> **Two shells, graded service.**
>
> **Shell A (service shell):** 550–600 km, **~60°–70° inclination Walker Delta + a small polar sub-shell**, ~70–90 satellites at maturity, ε ≥ 10°. Gives continuous or near-continuous service across the inhabited and economically active latitudes and the busy shipping lanes, with a thin polar capability. Every satellite: regenerative narrowband gNB + intra-plane ISL.
>
> **Shell B (relay/trunk shell, optional, Phase 3):** sparse, higher, carrying the cross-plane optical links and acting as the backhaul spine — fewer, more expensive satellites doing the expensive job, so you don't need a laser terminal on all 90.
>
> **Everywhere else and in the interim:** **store-and-forward**, with a published, contractual latency SLA (e.g. "≤ 90 min at ε ≥ 10° above 60° latitude").

Why this wins: it turns "any point on Earth" from a binary claim into a **tiered service catalogue**, which is what an operator actually sells and what makes the business case close.

---

## 3. ISL design

### 3.1 Optical vs RF — the honest trade for a smallsat operator

| | Optical | RF (Ka/V/W) |
|---|---|---|
| Throughput | 100 Mbps (1.5U class, e.g. Tesat SCOT20, 1.7 kg) → 10 Gbps (SCOT80, ~12 kg) → 100 Gbps (Starlink class, Mynaric Mk3.1 roadmap) | Tens–hundreds of Mbps typical |
| Mass/power | Higher; the small units exist but are the exception | Lower at low rates |
| Cost | High (though Tesat's Backnang line, opened Aug 2024, runs at ~100 units/month — prices are falling) | Lower |
| **Spectrum licence** | **None needed** ⭐ | **Required**; ITU coordination; interference into other systems |
| Security | Pencil beam — very hard to intercept or jam ⭐ | Interceptable/jammable |
| Pointing | Microradian PAT; hard, especially cross-plane | Easy |
| Export control | Many terminals are US-origin → **ITAR/EAR exposure** ⚠️ | More European options |
| Maturity | Industrial. >5,000 terminals flying on Starlink at 100 Gbps class, >99% link uptime | Flight-proven since Iridium (1990s) |

### 3.2 The decision, and the argument for it

**For a narrowband 5G NTN operator, the throughput argument for optical is irrelevant — and the other three arguments are decisive.**

Do the maths out loud: a satellite serving NB-IoT over a 1,664 km-radius footprint with, say, 10,000 concurrently active devices at a few hundred bits per transaction is carrying **single-digit Mbps of user traffic**. Even generous D2D messaging loads stay well under 50 Mbps. **A 10 Gbps laser terminal is 1000× oversized for the payload it would carry.**

So the correct ISL choice is driven by:
- **Regulatory:** optical needs no spectrum licence. For a company whose scarcest asset is spectrum, moving the backhaul out of the licensed domain entirely is strategically valuable — and it sidesteps EPFD scrutiny on the crosslinks.
- **Security/sovereignty:** for the defence and government segment OQ is chasing, an un-interceptable, un-jammable backhaul is a *feature you can charge for*.
- **Export control:** favour European terminals (Tesat, Mynaric) to stay out of ITAR. **Say this explicitly — OQ's entire pitch is European sovereignty, and an ITAR-encumbered laser terminal would poison it.**

**Recommendation:** **RF ISL intra-plane** (cheap, easy pointing, geometry is nearly static, sufficient for narrowband) **+ low-SWaP optical cross-plane** on a subset of satellites (the ones that need to bridge planes and reach gateways), European-sourced. This is a genuinely differentiated answer — most teams will pick one or the other.

### 3.3 Topology

- **Intra-plane (same-plane) links:** relative geometry is essentially fixed → near-static pointing, trivially maintainable, permanent. **Always do these.**
- **Inter-plane (cross-plane) links:** relative geometry sweeps continuously; near the **seam** of a Walker Star (where counter-rotating planes meet) closing velocities double and links must be dropped. Plan for **intermittent** cross-plane links and a routing protocol that tolerates predictable topology changes.
- **Classic "+Grid":** 4 links per satellite (fore/aft/port/starboard). Iridium has run this in RF since the 1990s; Starlink runs it optically today with 3–4 terminals per satellite.

**In-plane hop latency** (orbital circumference / satellites per plane, at c):

| Satellites per plane (h=550 km) | Hop distance | Hop delay |
|---|---|---|
| 20 | 2,174 km | 7.25 ms |
| 30 | 1,450 km | 4.84 ms |
| 60 | 725 km | 2.42 ms |

A transcontinental path of ~8–10 hops therefore costs **~25–60 ms** of ISL transit. Add 2 × ~6 ms for the up/down links. **Total ~40–75 ms end-to-end across a continent — comparable to or better than terrestrial fibre over the same distance**, because light in vacuum is ~50% faster than in glass. That is a legitimate, quotable selling point and it belongs in your latency budget.

### 3.4 The part OQ actually cares about: signalling, not bandwidth

Recall from the dossier: OQ's pending ISL patent is framed around *"keeping different base stations aware of each other and record-keeping of terminal devices being connectable to the different base stations."*

That is not a data-plane problem. It is the **mobility and context problem**: when a UE is handed from satellite 1 to satellite 2 every few minutes, the UE context, security keys and buffered data must move too. Rel-19's answer is Xn over ISL. **A proposal that addresses UE context transfer, buffer forwarding during handover, and how routing tables are maintained across a predictably-but-constantly-changing topology will land far better than one that only quotes Gbps.**

Concretely, mention:
- **Xn-C over ISL** for handover preparation and context transfer between satellite gNBs.
- **Deterministic routing** — the topology is *not* random; it is precisely predictable from ephemeris. You can pre-compute routing tables for the next N minutes on the ground and upload them, instead of running a reactive protocol. This is a huge simplification and a real design decision.
- **Buffer forwarding** so in-flight data follows the UE across a satellite handover instead of being dropped.

---

## 4. Link budget (narrowband, S-band ~2 GHz)

```
Free-space path loss:  FSPL = 32.45 + 20·log₁₀(f_MHz) + 20·log₁₀(d_km)   [dB]
Thermal noise:         N = −174 + 10·log₁₀(BW_Hz) + NF                    [dBm]
```

| Case | Value |
|---|---|
| FSPL @ 2 GHz, 993 km (ε=30°, h=550) | **158.4 dB** |
| FSPL @ 2 GHz, 1,815 km (ε=10°, h=550) | **163.6 dB** |

### 4.1 Uplink — handset/sensor → satellite
Assume UE EIRP 23 dBm (standard cellular power class 3), NB-IoT single-tone 3.75 kHz, satellite NF 2 dB, 3 dB of polarisation/body/implementation loss.

| Slant range | Satellite antenna gain | SNR |
|---|---|---|
| 993 km (ε=30°) | 18 dBi | +15.9 dB |
| 993 km | 24 dBi | +21.9 dB |
| **1,815 km (ε=10°)** | **18 dBi** | **+10.6 dB** |
| 1,815 km | 24 dBi | +16.6 dB |

**Conclusion: the NB-IoT uplink closes comfortably even at 10° elevation with a modest satellite antenna.** This is the physical reason OQ's business exists on 6U CubeSats. It is also the reason you can design for ε = 10° and cut your constellation by 4× (§2.3).

### 4.2 Downlink — satellite → device
180 kHz NB-IoT carrier, UE NF 7 dB, 3 dB losses:

| Slant range | Target SNR | Required satellite EIRP |
|---|---|---|
| 993 km | −6 dB (heavy repetition) | 11.0 dBW |
| 993 km | 0 dB | 17.0 dBW |
| **1,815 km** | **−6 dB** | **16.2 dBW** |
| 1,815 km | 0 dB | 22.2 dBW |
| 1,815 km | +4 dB | 26.2 dBW |

**Conclusion: ~16–26 dBW EIRP (40–400 W equivalent radiated) covers narrowband D2D at 10° elevation.** Achievable on a smallsat with a modest phased array. Compare with wideband voice/data to handsets, which is why AST SpaceMobile unfolds antenna arrays of hundreds of square metres. **State the contrast — it justifies the narrowband strategy in one line.**

*Caveat to state openly: these are clear-sky, line-of-sight budgets with no shadowing, scintillation or multipath margin. Real designs add 3–10 dB. The conclusions (narrowband closes easily; wideband-to-handset does not) survive that margin comfortably.*

---

## 5. SWaP, thermal, radiation, lifetime

### 5.1 Platform classes

| Class | Mass | Orbit-average power | Can host |
|---|---|---|---|
| 6U CubeSat (OQ today) | 8–12 kg | tens of W | Narrowband regenerative gNB, small antenna, RF ISL |
| 12U–16U | 20–30 kg | 50–150 W | Above + modest phased array + small optical terminal |
| ESPA-class smallsat (100–200 kg) | 100–200 kg | 200 W–1 kW | Multi-beam phased array, multiple ISL terminals, wideband |
| AST BlueBird class | 1,000+ kg | multi-kW | Broadband direct-to-handset |

**OQ's Gen-2 (48 satellites, both NR and IoT) implies a step up from 6U.** Your proposal should name a class and defend it. A 12U–16U or small ESPA-class bus is the credible landing zone: enough power for a regenerative gNB plus a phased array plus one or two ISL terminals, without leaving the rideshare launch economics that make OQ affordable.

### 5.2 The constraint people forget: thermal, not power

In vacuum there is no convection. Every watt the digital payload burns must be **radiated** away through panel area. A regenerative gNB is a general-purpose computer running continuously, unlike a bent-pipe's analogue chain. **Radiator area, not solar array area, is frequently the binding constraint on how much on-board processing a smallsat can host.** Saying this shows real engineering maturity — most teams cite power and stop.

Mitigations worth naming: duty-cycling the gNB (it only needs to be fully active over served regions — over empty ocean it can throttle), using the eclipse portion of the orbit for heavy processing, and deployable radiators.

### 5.3 Radiation

- **SEU** (single-event upsets, bit flips) and **TID** (cumulative dose degradation).
- Rad-hard processors run roughly **a decade behind** commercial silicon in performance-per-watt — a real problem when you want to run a 5G stack.
- **The practical answer, which is what industry actually does:** COTS processors with watchdogs, ECC memory, scrubbing, and redundancy, accepting a shorter design life and periodic reboots — paired with a small rad-hard supervisor that can always recover the spacecraft. Mention this by name; it's the difference between a textbook answer and an engineering answer.
- At 1,200 km you are entering the inner radiation belt's lower reaches — another reason the "cheap high shell" is not free.

### 5.4 Design life and replenishment — put this in the business case

- LEO smallsat design life: **5–7 years** (drag, radiation, component wear).
- A constellation of **N** satellites with a **5-year** life requires **N/5 satellites built, launched and commissioned every year, in perpetuity.**
- For N = 90: **18 satellites per year, forever.** At an all-in €0.5–1.5M per smallsat including launch, that is **€9–27M/year of pure maintenance** before you have served a single customer.
- **This number must appear in your business case.** It is the single most common omission and the easiest thing for a mentor to kill a pitch with.

### 5.5 Debris and orbital safety

- 550–600 km: natural decay in **years** without propulsion. ✅ Compliant with tightening de-orbit rules by default.
- 1,200 km: decay in **centuries**. ⚠️ Requires reliable propulsion and a disposal plan, and invites regulatory challenge.
- Budget for: conjunction screening, collision-avoidance manoeuvres (propellant), end-of-life passivation, and IADC/national compliance reporting. With ~90 satellites this is an **operational cost line**, not a checkbox.
- OQ's existing Tiger satellites already carry **electric propulsion for deployment, formation flying and EOL disposal** — cite this, it shows their fleet is already designed for compliance.

---

## 6. Latency budget — a worked example to put on a slide

**Scenario: a sensor mid-Atlantic to a customer's cloud in Frankfurt, no gateway in view.**

| Segment | Delay |
|---|---|
| UE → satellite (ε = 10°, h = 550 km) | 6.1 ms |
| Intra-plane ISL, ~8 hops @ 30 sats/plane | ~39 ms |
| Cross-plane hop ×2 | ~10 ms |
| Satellite → gateway (Europe) | 6.1 ms |
| Gateway → 5G core → customer cloud (terrestrial) | 5–20 ms |
| Processing/scheduling/queuing (regenerative, on-board) | 10–30 ms |
| **Total one-way** | **~75–110 ms** |

Compare: **bent-pipe with no gateway in view = ∞ (no service)**, or store-and-forward at **minutes to hours**. That contrast is the entire value proposition of the ISL mesh, expressed in one table. Lead with it.
