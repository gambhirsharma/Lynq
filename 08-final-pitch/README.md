# Final pitch: NEOSPACE Europe 2026

The deck Team Lynq presented to the jury in Luxembourg (19–20 October 2026): a 10-minute pitch and 10 minutes of Q&A.

| File | What it is |
|---|---|
| [`Lynq-NTN-Pulse-final-pitch.pdf`](Lynq-NTN-Pulse-final-pitch.pdf) | **The deck shown on the day.** 15 main slides, 1 divider and 4 backups (21 pages) |
| [`deck.md`](deck.md) | Text source for every slide: on-slide content, speaker notes and script. Slide NN is PDF page NN+1 |
| [`script.md`](script.md) | Word-for-word spoken script with timings, the speaker for each slide, and a Q&A cue card |
| [`pitch-template.md`](pitch-template.md) | The blank NEOSPACE fill-in sheet we started from |
| [`earlier-draft-11-slides/`](earlier-draft-11-slides/) | Earlier 11-slide pitch for the Phase 1 North Sea design (superseded) |

## Slide map

| # | Slide | Section | Backed by |
|---|---|---|---|
| 00 | Title | | |
| 01 | The problem | Technology | [`07-constellation-optimization`](../07-constellation-optimization/README.md) |
| 02 | Our solution | Technology | [`DESIGN-7x16.md`](../07-constellation-optimization/DESIGN-7x16.md) |
| 03 | How it works | Technology | [`04-simulation/HOW-IT-WORKS.md`](../04-simulation/HOW-IT-WORKS.md) |
| 04 | Technical architecture | Technology | [`04-simulation/FLEET-OPS.md`](../04-simulation/FLEET-OPS.md) |
| 05 | Feasibility and maturity (TRL 3 → 5) | Technology | [`results/report.md`](../07-constellation-optimization/results/report.md), [`04-simulation`](../04-simulation/README.md) |
| 06 | Prior art (IP) and benchmark | Technology | [`01-research/07`](../01-research/07-COMPETITIVE-LANDSCAPE.md), [`06-leo-constellations`](../06-leo-constellations/README.md) |
| 07 | Market and customers | Business model | [`01-research/06`](../01-research/06-BUSINESS-CASE.md) |
| 08 | Value and revenue | Business model | |
| 09 | Regulation and standards | Technology | [`01-research/05`](../01-research/05-REGULATORY-deep-dive.md) |
| 10 | Costs and economics | Business model | [`costmodel.py`](../07-constellation-optimization/costmodel.py) |
| 11 | Funding request and use (€450k) | Business model | |
| 12 | R&D roadmap | Implementation plan | |
| 13 | Team, partners and risks | Implementation plan | [`DESIGN-7x16.md` §2, §6](../07-constellation-optimization/DESIGN-7x16.md) |
| 14 | Next steps | Implementation plan | |
| 15 | Thank you | | |
| 16–20 | Backup: 7×16 design, KubeEdge layer, cost per design, references | Q&A | |

Every constellation number in the deck can be regenerated with
`07-constellation-optimization/design_detail.py 16` (see [`DESIGN-7x16.md`](../07-constellation-optimization/DESIGN-7x16.md#how-to-verify)).
