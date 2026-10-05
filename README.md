<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="02-brand/lynq-brand-kit/logos/orbital-link/horizontal/lynq-orbital-link-horizontal-dark.svg">
    <img alt="Lynq" src="02-brand/lynq-brand-kit/logos/orbital-link/horizontal/lynq-orbital-link-horizontal-light.svg" width="320">
  </picture>
</p>

<h3 align="center">Lynq NTN-Pulse</h3>
<p align="center"><em>Every signal, the right path.</em></p>

<p align="center">
  <a href="03-proposal/current/final.pdf"><b>📄 Read the proposal (PDF)</b></a> ·
  <a href="01-research/00-START-HERE.md">Research pack</a> ·
  <a href="02-brand/lynq-brand-kit/BRAND-GUIDE.md">Brand guide</a>
</p>

---

Team **Lynq**'s entry for the **NEOSPACE Europe 2026** challenge set by **OQ Technology**:
*AnyPoint-NTN: Global gNB-Onboard LEO Constellation for Ubiquitous 5G NR-NTN* (category: Next-Gen Downstream).

| | |
|---|---|
| **Event** | NEOSPACE Europe 2026, 19–20 October 2026, Luxexpo The Box, Luxembourg |
| **Sponsor** | OQ Technology S.à r.l. (Luxembourg) |
| **Product** | Lynq NTN-Pulse: digital twin and policy engine for a regenerative gNB-onboard LEO constellation |
| **Status** | Phase 1 proposal finished (2 pages). Phase 2 is the on-site simulation in Luxembourg |

## What is Lynq NTN-Pulse?

Today's satellite IoT mostly uses *bent-pipe* satellites. They only relay signals, so a ground gateway has to be in view.
If that gateway is out of view, blocked, overloaded or restricted by national rules, the service drops.
Offshore wind farms, oil and gas platforms, vessels and pipelines are hit hardest.

OQ is moving to **regenerative** satellites, which run a full 5G base station (gNB) in orbit.
That lets traffic route over inter-satellite links (ISLs) or wait onboard until the next pass.
It also makes the network much harder to run.

NTN-Pulse is the software layer for that network:

- **Digital twin.** Models satellites, coverage, gateway visibility, feeder and ISL state, terminals, traffic demand and onboard compute. Sized for today's ~12 satellites and the planned 30.
- **Policy engine.** Assigns each traffic class to a path (deliver now, relay over ISL, process at the edge, or store and forward) based on QoS, latency, reliability, data residency and cost.
- **Sovereignty built into routing.** Sends each flow only to a gateway that is allowed to receive it, with local user-plane breakout. ITU and national rules are treated as hard constraints.
- **NTN dashboard.** Shows timing, handovers, link budgets, queues, predicted outages and routing decisions.

### Design point

| Parameter | Value |
|---|---|
| Constellation | **~12 → 30** satellites (10 OQ + 2 ERMIS in orbit today; 30 planned) |
| Payload | **Full regenerative gNB** on every satellite |
| ISL | **RF** within each orbital plane, **optical** between planes on a subset of relay satellites |
| Minimum elevation | **10°** |
| Service tiers | Continuous **<150 ms** · Mesh-relayed **<250 ms** · Store-and-forward **≤90 min** |
| First market | North Sea offshore energy and maritime operations (~51–61°N) |
| Pricing | Per asset, not per byte. Break-even at ~75k assets × €120/yr, or ~9k sovereign endpoints × €1,000+/yr |

The full reasoning is in the [proposal](03-proposal/current/final.md): technical, regulatory and business angles, plus risks and next steps.

## Repository layout

```
.
├── 00-challenge-brief/        Official OQ use-case brief (.docx original + .md conversion)
├── 01-research/               Research pack (18 Sep 2026). Start with 00-START-HERE.md
├── website/                 Static one-page site for Vercel. See website/README.md
├── 02-brand/
│   ├── lynq-brand-kit/        Logos, favicons, CSS tokens. Start with BRAND-GUIDE.md
│   ├── brand-master-prompt.md Prompt used to generate the brand
│   └── Lynq brand identity system.zip   Original brand-kit download
└── 03-proposal/
    ├── current/               ★ The proposal to submit (.pdf, .docx, .doc, .html, .md)
    │   └── build-src/         .docx build script, logo and data-path figure
    ├── working-notes/
    │   ├── 01-condense-to-2-pages/   3-page working PDF → 2-page final: review and diffs
    │   └── 02-fleet-30-update/       Fleet size 10 → 30 satellites: change notes and patches
    └── history/               Every earlier version, oldest first
```

### Research pack

If you have no space or telecom background, read [`01-research/01-PRIMER-no-space-background.md`](01-research/01-PRIMER-no-space-background.md) first.

| # | File | Topic |
|---|---|---|
| 01 | [Primer](01-research/01-PRIMER-no-space-background.md) | Every term in the brief explained from zero |
| 02 | [OQ dossier](01-research/02-OQ-TECHNOLOGY-dossier.md) | The sponsor: fleet, funding, spectrum, strategy |
| 03 | [Challenge decoded](01-research/03-CHALLENGE-decoded.md) | What OQ is really asking for and how it will be judged |
| 04 | [Technical](01-research/04-TECHNICAL-deep-dive.md) | Architecture, constellation sizing, ISL trade, link and SWaP budgets |
| 05 | [Regulatory](01-research/05-REGULATORY-deep-dive.md) | ITU, EPFD, MSS spectrum, landing rights, lawful intercept, export control |
| 06 | [Business case](01-research/06-BUSINESS-CASE.md) | Segments, unit economics, revenue model |
| 07 | [Competitors](01-research/07-COMPETITIVE-LANDSCAPE.md) | Starlink D2C, AST, Lynk, Sateliot, Skylo, Iridium, Kepler, IRIS² |
| 08 | [Our proposal (research draft)](01-research/08-OUR-PROPOSAL.md) | First answer to the three expected outcomes |
| 09 | [Sources](01-research/09-SOURCES.md) | Bibliography |

## Proposal version history

All versions are in `03-proposal/`.

| Version | Folder | Date | Changes |
|---|---|---|---|
| v1 | `history/v1-2026-09-27-first-draft/` | 27 Sep | First team draft, review report, constellation change, v2 in md/html/pdf/docx plus a dark theme |
| v2 | `history/v2-2026-09-28-branded-redesign/` | 28 Sep | Branded layout and real satellite count |
| — | `working-notes/01-condense-to-2-pages/working-pdf.pdf` | 28 Sep | 3-page working PDF used as the starting point for condensing |
| v3 | `history/v3-2026-09-28-condensed-8.6pt/` | 28 Sep | First 2-page version, 8.6 pt body |
| v4 | `history/v4-2026-09-28-10pt/` | 28 Sep | 10 pt body, team roles added |
| v5 | `history/v5-2026-09-28-fleet-core-patch/` | 28 Sep | Core fleet-30 patch applied |
| v5b | `history/v5b-2026-09-28-pre-fleet-backup/` | 28 Sep | Backup taken just before the final fleet edits |
| v6 | `history/v6-2026-09-28-10-sats/` | 28 Sep | "10 → 30 satellites" wording |
| **current** | `current/` | 28 Sep | "~12 → 30 satellites" (10 OQ + 2 ERMIS) |

## Website

`website/` holds a static one-page site with the proposal summary, team and contact form.
To deploy it on Vercel, set Root Directory to `website`, with no build step. See [`website/README.md`](website/README.md).

## Rebuilding the .docx

The Word version is generated with [`docx`](https://www.npmjs.com/package/docx) for Node.js.

```bash
cd 03-proposal/current/build-src
npm install docx            # one-time
node build.js ../final.docx
```

Run it from `build-src/`, because `build.js` loads `logo.png` and `fig.png` from the working directory.

## Team

| Name | Role |
|---|---|
| Davoud Jokar | Systems and digital twin |
| Ines Bouissou | NTN modelling and optimisation |
| Gambhir Sharma | Cloud, APIs and deployment |
| Maryam Amini | TCO, pricing, regulation and first-buyer case |

## Notes

- Files were reorganised (moved, not edited). Some older notes still use their original paths. For example, `review.md` refers to `../working-pdf.pdf`, which is now in the same folder, and `team-proposal-report.md` refers to `research/…`, which is now `01-research/…`.
- The challenge brief in `00-challenge-brief/` belongs to OQ Technology and NEOSPACE. It is included here only for reference.
