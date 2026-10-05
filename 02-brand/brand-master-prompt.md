# Master prompt — Lynq brand theme & logo (for Claude Design)

Copy everything below the line into Claude Design.

---

You are a senior brand and visual identity designer. Create a **logo and a complete visual theme** for our team **Lynq** and its product **Lynq NTN-Pulse**. We will use them at the NEOSPACE Europe 2026 Challenge (19–20 October 2026, Luxembourg) on a 2-page proposal, a pitch deck, a live demo dashboard and a team badge/poster.

## 1. Who we are

- **Team name:** Lynq, pronounced "link".
- **Product:** Lynq NTN-Pulse is a digital twin and policy engine for a constellation of LEO satellites that each carry a 5G base station (gNB). It decides how every piece of industrial traffic travels: immediately, relayed satellite-to-satellite, processed at the edge, or stored for later. It also routes each flow only through gateways that are legal for that user's jurisdiction.
- **Challenge sponsor:** OQ Technology (Luxembourg), a 5G satellite operator. Category: Next-Gen Downstream.
- **First customers:** offshore energy and wind-farm operators; later maritime, drones and defence.
- **Team:** Davoud Jokar (systems & digital twin), Ines Bouissou (NTN modelling), Gambhir Sharma (cloud & APIs), Maryam Amini (business & regulation).
- **Tagline options (propose your best, or improve these):**
  - "Every signal, the right path."
  - "Sovereign connectivity, from orbit."
  - "Any point. Right path. Right rules."

## 2. Ideas the brand should express

1. **Link / connection.** The name "Lynq" means links: satellite-to-satellite links, links to the ground, and linking industry to 5G.
2. **Pulse / heartbeat.** A live, monitored network that always knows its state, with priority alarms that always get through.
3. **Intelligent routing.** Paths chosen by policy, shown as a mesh with one highlighted path.
4. **Trust and sovereignty.** European, compliant and secure. It should feel credible to regulators, defence users and energy companies, not like a consumer app.
5. **Space + ocean.** Orbits above, offshore platforms and sea below.

**Personality:** precise, calm, trustworthy, quietly futuristic. The overall look should be close to OQ Technology's own website (dark, cinematic, orange accent; see §4.1). Think aerospace engineering or a mission-control display, not sci-fi. Avoid anything cartoonish, crypto-looking or gamer-style.

## 3. Logo requirements

Deliver **3 distinct logo concepts**. For each one give a short rationale (2–3 sentences). Then fully develop the one you recommend.

Possible directions (explore, don't copy literally):
- **A. Orbital link:** the "q" or "y" in "Lynq" formed by an orbit arc or by two connected nodes (satellite ↔ satellite).
- **B. Pulse path:** a heartbeat or pulse line that becomes a routing path through a small node mesh.
- **C. Mesh monogram:** a compact "L" or "Lq" mark built from 3–4 nodes and links, like an ISL constellation seen from above.

Constraints:
- **Wordmark:** "Lynq" set in a clean geometric or grotesk sans. Consider a custom detail on the "q" as the brand hook.
- **Symbol/icon:** must work on its own at **16 px (favicon)** and **24 px (slide footer)**. Keep it simple: at most 4 nodes, no thin hairlines that disappear when small.
- **Lockups:**
  - horizontal (icon + "Lynq")
  - stacked
  - product lockup "Lynq **NTN-Pulse**"
  - icon only
- **Variants:** full colour on dark, full colour on light, single-colour black, single-colour white.
- Must reproduce well in **flat vector**: no gradients required for legibility, no photographic effects, no 3D. A subtle gradient version for digital use is allowed as an extra.
- Must sit comfortably **next to** the OQ Technology logo on a dark slide (compatible style and weight), while being clearly different from it and from Starlink, ESA and Iridium. Do not use a dot with radiating arcs (that is OQ's mark) or a generic swoosh-around-a-globe.
- Clear-space rule and minimum-size rule.

## 4. Theme / visual system

### 4.1 Base the theme on OQ Technology's website (https://www.oqtec.com/)

Our work is for OQ Technology's challenge, so the theme should **feel like part of the OQ family**: the same dark, premium, space look. It must still be clearly **our own team identity**, not a copy of OQ's brand. Reference points taken from oqtec.com:

- **Backgrounds:** near-black, not navy: `#0E0E0E`, `#101010`, `#1C1C21`, with raised cards in `#2F2F37` → `#0B0B0B` gradients and subtle gradient borders.
- **Text:** white `#FFFFFF`; secondary text in grey `#999999` or white at 40–70 % opacity; muted body `#353535` on light backgrounds.
- **Signature accent:** warm orange / amber: `#FAA055` (main), `#F4A968`, `#FAA55F`, light tint `#FACC83`. Use it on buttons, highlights and key numbers, with a soft inner glow (e.g. `inset 0 -4px 4px rgba(244,169,104,.25)`).
- **Headings:** large and clean, often with a **grey-to-white horizontal gradient** (`linear-gradient(91deg, #999 1%, #FFF 99%)`).
- **Fonts used on oqtec.com:** **Urbanist** (headings/UI), **Satoshi** (body), **Pragati Narrow** (condensed labels). Use Urbanist + Satoshi or close equivalents, plus a monospace (e.g. JetBrains Mono or IBM Plex Mono) for telemetry and numbers.
- **Shapes:** rounded corners (16 px cards, 8 px small elements, fully rounded pill buttons), soft black-to-transparent fades at section edges, large planet/Earth-from-orbit imagery, thin circular orbit outlines as background decoration, and EU + Luxembourg flags as sovereignty cues.
- **Mood:** cinematic, dark, calm, premium, with a lot of negative space.

**How to stay distinct from OQ:**
- The OQ logo is white "OQ" lettering with an **orange dot and radiating signal arcs**. **Do not** use radiating arcs from a dot, and do not use orange as the main colour of our logo mark.
- Keep OQ's dark base and orange as a **shared accent**. Add **one Lynq-specific secondary colour** (e.g. a cool cyan/teal such as `#3FD0E0`, or propose a better one) for ISL links, the "pulse" and our data paths. On a slide next to OQ material, the result should read as "OQ-compatible team", not "OQ itself".
- Never place the OQ logo inside our logo. Use it only in "Challenge by OQ Technology" credit lines.

### 4.2 Colour palette (propose exact HEX values, check contrast to WCAG AA)
- **Base:** OQ-style near-black backgrounds and white/grey text (see 4.1).
- **Shared accent:** OQ orange `#FAA055` family for calls to action and highlighted numbers.
- **Lynq accent:** one cool secondary colour for links, the pulse line and the policy-compliant path.
- **Alert colour:** priority alarms need a colour that is **not** the brand orange, e.g. a clear red/coral. Otherwise alarms and ordinary highlights look the same.
- **Neutrals:** 4–5 greys, tuned for both the dark dashboard and a white A4 document.
- **Data-viz set:** 4–6 colours that stay distinguishable for colour-blind viewers, for traffic classes: alarm, control, telemetry, video, bulk. Also 3 colours for the service tiers: Continuous, Mesh-relayed, Store-and-forward. They must read well on `#0E0E0E`.
- **Dark theme** (primary: deck, demo, badge) matching oqtec.com. **Light theme** (2-page PDF, print): white page, near-black text, orange and Lynq-accent highlights, same fonts.

### 4.3 Typography
- Headings: **Urbanist** (as on oqtec.com). Body: **Satoshi** (or Inter as fallback). Numbers and telemetry: a monospace.
- A type scale for A4 documents (body 10–11 pt, so a dense 2-page proposal stays readable) and for 16:9 slides (large headings with the grey-to-white gradient, OQ-style).

**Graphic language:**
- Motifs: orbit arcs, node-and-link meshes, a thin pulse line, subtle coordinate or grid lines.
- Icon style: line icons with consistent stroke weight, for satellite, gateway, offshore platform, wind turbine, ship, shield/sovereignty, cloud, alarm.
- Rules for diagrams: how satellites, ISL links (RF vs optical as solid vs dashed), gateways and the "policy-compliant path" highlight are drawn.

## 5. Deliverables

1. The 3 logo concepts with rationale, then the full recommended logo system (all lockups and variants) as **SVG**.
2. A **one-page brand sheet**: logo, clear space, palette with HEX/RGB, typography, do's and don'ts.
3. Applied mock-ups:
   - **2-page proposal header/footer** (A4, light): title "Lynq NTN-Pulse — a jurisdiction-aware regenerative NTN for offshore operations", team names, section heading style.
   - **Pitch-deck title slide and one content slide** (16:9, dark).
   - **Dashboard header bar** for the digital-twin demo (dark), showing the logo, a live "pulse" status indicator and example traffic-class colour chips.
   - **Team badge / sticker** (square or circular).
4. Design tokens as **CSS variables** (colours, fonts, spacing, radii) so we can reuse them in our web dashboard.
5. One **side-by-side check**: our title slide next to a mock "Challenge by OQ Technology" credit, to show the two brands look compatible but distinct.

## 6. Process

- First show the 3 concepts side by side and wait for our choice before building the full system.
- Keep everything editable and vector-based.
- If a requirement conflicts with good design, tell us and propose a better option.
