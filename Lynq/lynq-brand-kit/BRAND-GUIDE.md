# Lynq — Brand Guide v1.0
Team **Lynq** (pronounced "link") · Product **Lynq NTN-Pulse** · NEOSPACE Europe 2026 Challenge, Luxembourg · Challenge by OQ Technology

---

## 1. Tagline
**Primary:** *Every signal, the right path.*
Alternates: *Sovereign connectivity, from orbit.* (policy/regulator audiences) · *Any point. Right path. Right rules.* (technical slides)

## 2. Logo
Two approved marks. Use **one per document** — don't mix them on the same page.

| Mark | Use it for |
|---|---|
| **Orbital link** (`logos/orbital-link`) | Primary identity: proposal, deck, badge, website header, favicon |
| **Pulse path** (`logos/pulse-path`) | Live product surfaces: NTN-Pulse dashboard, status pages, loading/“live” states (`animated/lynq-pulse-path-live.svg`) |

If you need to choose only one, choose **Orbital link**.

### Files
```
logos/<mark>/icon/        icon only (SVG + 1024px PNG)
logos/<mark>/horizontal/  icon + "Lynq"            ← default lockup
logos/<mark>/stacked/     icon over "Lynq"         ← square formats, badge
logos/<mark>/product/     "Lynq | NTN-Pulse"       ← product materials
favicon/<mark>/           favicon.svg + 16/32/48/180/512 PNG
```
Each lockup comes in 4 variants:
- `-dark`  full colour for dark backgrounds (white + cyan #3FD0E0)
- `-light` full colour for light backgrounds (#0E0E0E + teal #0B8A9A)
- `-black` single colour black
- `-white` single colour white

> **Font note:** lockup SVGs use live Urbanist text and load it from Google Fonts. Before sending to print or opening in Illustrator/Figma, install Urbanist (fonts.google.com/specimen/Urbanist) and **convert text to outlines**.

### Clear space
Keep empty space around the logo equal to **½ the icon height** on all sides. Nothing (text, edges, other logos) enters this zone.

### Minimum size
- Icon only: **16 px** on screen / **5 mm** in print
- Horizontal lockup: **80 px wide** / **22 mm**
- Product lockup: **160 px wide** / **40 mm**

### Placing Lynq next to OQ Technology
- Put the OQ logo only in a credit line: **"Challenge by OQ Technology"**, bottom-right or footer.
- Match the height of the two logos. Separate them with a thin 1 px divider at 16 % white, or with at least 2× clear space.
- Never put the OQ logo inside or touching the Lynq logo.

### Don'ts
- Don't recolour the mark orange. Orange belongs to OQ; it's our shared accent, not our logo colour.
- Don't add radiating arcs, glows, 3D effects or drop shadows.
- Don't stretch, rotate or outline the logo, and don't swap the wordmark font.
- Don't place the colour version on busy photos. Use the white version with a dark scrim.
- Don't use cyan #3FD0E0 on white. Use the `-light` files, which use teal #0B8A9A.

## 3. Colour
### Dark theme (deck, dashboard, badge, website)
| Role | HEX | RGB | Notes |
|---|---|---|---|
| Background | #0E0E0E | 14,14,14 | main canvas |
| Background 2 | #101010 | 16,16,16 | alternate sections |
| Surface | #1C1C21 | 28,28,33 | panels |
| Card | #2F2F37 → #0B0B0B | gradient | 1 px border rgba(255,255,255,.08) |
| Text | #FFFFFF | 255,255,255 | 19.4:1 |
| Text secondary | #999999 | 153,153,153 | 7.0:1 AA |
| **Lynq Cyan** | #3FD0E0 | 63,208,224 | links, pulse, compliant path · 11.2:1 |
| **OQ Orange** (shared) | #FAA055 | 250,160,85 | CTAs, key numbers · 10.0:1 |
| Orange tint | #FACC83 | 250,204,131 | hover, subtle fills |
| **Alert** | #FF5A5F | 255,90,95 | priority alarms ONLY · 6.3:1 |
| OK / healthy | #5BD69A | 91,214,154 | status only |

### Light theme (2-page proposal, print)
| Role | HEX | Notes |
|---|---|---|
| Page | #FFFFFF | |
| Text | #0E0E0E | body |
| Text muted | #353535 | 12.6:1 |
| Caption | #6B6B73 | 5.3:1 AA |
| Teal (graphics) | #0B8A9A | logo, lines, diagrams |
| Teal (text) | #087F8E | 4.7:1 AA |
| Orange (text/numbers) | #B45F12 | 4.6:1 AA. Use #FAA055 for fills only |
| Alert | #D1343A | 4.9:1 |
| Rules/borders | #D6D6DB | |
| Panel fill | #F2F2F4 | |

### Neutrals
#0E0E0E · #1C1C21 · #353535 · #6B6B73 · #999999 · #D6D6DB · #F2F2F4 · #FFFFFF

### Data-viz: traffic classes
Colour-blind safe on #0E0E0E. **Always pair colour with a label or shape**, especially for alarm.
| Class | HEX | Shape |
|---|---|---|
| Alarm | #FF5A5F | ▲ triangle |
| Control | #E8D25A | ◆ diamond |
| Telemetry | #56B4E9 | ● circle |
| Video | #D78BC0 | ■ square |
| Bulk | #8A8A94 | ▬ bar |

### Data-viz: service tiers
| Tier | HEX | Line |
|---|---|---|
| Continuous | #3FD0E0 | solid |
| Mesh-relayed | #9B8CFF | solid, with node dots |
| Store-and-forward | #B8C4CC | dotted |

## 4. Typography
- **Urbanist** 600: headings, UI, wordmark (Google Fonts)
- **Satoshi** 400/500/700: body (Fontshare; fallback Inter)
- **JetBrains Mono** 400/500: telemetry, numbers, labels (uppercase, +10 % tracking)

### A4 proposal scale (light)
| Style | Font | Size / leading |
|---|---|---|
| Title | Urbanist 600 | 22 pt / 26 pt |
| H1 section | Urbanist 600 | 14 pt / 18 pt, teal numeral "01" |
| H2 | Urbanist 600 | 11.5 pt / 15 pt |
| Body | Satoshi 400 | 10 pt / 14 pt |
| Caption, table | Satoshi 400 | 8.5 pt / 11 pt |
| Label | JetBrains Mono 500 | 7.5 pt caps, +10 % tracking |
Margins 18 mm · 12-column grid · 4 mm gutter.

### 16:9 slide scale (1920×1080, dark)
| Style | Font | Size |
|---|---|---|
| Display / title | Urbanist 600, grey→white gradient | 120 px |
| H1 | Urbanist 600, gradient | 72 px |
| H2 | Urbanist 600 | 48 px |
| Body | Satoshi 400, white 70 % | 28–32 px |
| Big number | JetBrains Mono 500, orange | 96 px |
| Label / footer | JetBrains Mono 500 caps | 20–24 px |
Heading gradient: `linear-gradient(91deg, #999 1%, #FFF 99%)`. Use it on headings only, never on body text.

## 5. Shapes and layout
- Radii: 16 px cards · 8 px small elements · pill buttons
- Primary button: orange #FAA055, text #0E0E0E, `inset 0 -4px 4px rgba(244,169,104,.25)`
- Secondary button: transparent, 1 px border at 16 % white, white text
- Leave plenty of empty space. Fade section edges from black to transparent.
- Decoration: thin circular orbit outlines (1 px, 6 % white), subtle coordinate grid (1 px, 4 % white)
- Sovereignty cues: small EU and Luxembourg flags, only in credit or footer lines

## 6. Graphic language and diagrams
| Element | How to draw it |
|---|---|
| Satellite | filled circle node Ø 8–10 px, white |
| Gateway (ground) | square node 10 px, white outline 2 px |
| User terminal / platform | line icon, 2 px stroke |
| ISL, optical | **solid** 2 px, white 40 % |
| ISL, RF | **dashed** 2 px (6/4), white 40 % |
| Feeder / service link | solid 2 px, grey #6B6B73 |
| **Policy-compliant path** | **solid 3 px cyan #3FD0E0**, round caps, nodes on the path turn cyan |
| Blocked / non-compliant gateway | gateway in #6B6B73 with a 2 px diagonal strike |
| Priority alarm flow | coral #FF5A5F, 3 px, ▲ marker |
| Pulse line | thin 2 px cyan trace; may animate on screen |

Icons: 24 px grid, 2 px stroke, round caps and joins, no fills. Set: satellite, gateway, offshore platform, wind turbine, ship, shield, cloud, alarm. Lucide or Phosphor (regular) match this style.

## 7. Using the tokens
Link `tokens/lynq-tokens.css` in any web page or dashboard:
```html
<link rel="stylesheet" href="tokens/lynq-tokens.css">
<body style="background:var(--lynq-bg);color:var(--lynq-text);font-family:var(--lynq-font-body)">
  <h1 class="lynq-h-gradient" style="font-family:var(--lynq-font-heading)">Every signal, the right path.</h1>
  <button class="lynq-btn">Open live demo</button>
</body>
```
For light pages, add `class="lynq-light"` on `<html>` or `<body>`.
For favicons: `<link rel="icon" href="favicon/orbital-link/favicon.svg">` + `<link rel="apple-touch-icon" href="favicon/orbital-link/favicon-180.png">`.

## 8. Quick checklist before you publish
- [ ] Only one Lynq mark style per document
- [ ] Correct variant for the background (dark / light / mono)
- [ ] Clear space and minimum size respected
- [ ] Orange for CTAs and numbers, cyan for paths, coral for alarms only
- [ ] Text contrast meets AA (see tables above)
- [ ] OQ logo only in the "Challenge by OQ Technology" credit
