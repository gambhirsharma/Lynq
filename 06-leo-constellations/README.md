# 06 — LEO Constellation Market Report

> Who runs LEO constellations today: revenue, satellites in orbit, latency, customer base and coverage.
> **Compiled:** 19 October 2026. Figures move fast; every number has a source in §6 and an "as of" date.
> **How to read the confidence column:** **A** = company filing / earnings release · **B** = reputable trade press or Wikipedia citing filings · **C** = third-party tracker or aggregator, not independently confirmed.

---

## 1. Summary table

| Operator | Segment | Satellites (in orbit, working) | Revenue (latest) | Customers | Latency | Coverage | Conf. |
|---|---|---|---|---|---|---|---|
| **Starlink** (SpaceX) 🇺🇸 | Broadband + D2C | ~11,100 working (Sep–Oct 2026); ~13,000 launched | **$11.4B** (FY2025, Connectivity segment, 61% of SpaceX's $18.7B); ~$15.9B forecast 2026 | **10.3M** (31 Mar 2026, S-1); ~12M (Jun 2026) | ~25–60 ms typical; Ookla median 45 ms (Q1 2025) | ~160–164 countries & territories; D2C in ~22 | A/B |
| **Eutelsat OneWeb** 🇫🇷🇬🇧 | Broadband, B2B/government only | 654 Gen-1 (~150 kg each) | **€297M** LEO revenue (FY to 30 Jun 2026, +69.5%), ~¼ of group €1.24B | Wholesale: telcos, maritime, aero, government, rail (no consumer retail) | <70 ms (marketed); 50–70 ms (tracker) | Global incl. poles (polar orbits) | A/B |
| **Iridium** 🇺🇸 | Voice, narrowband data, IoT | 66 active, cross-linked (plus spares) | **$871.7M** (FY2025); Q2 2026 $225.2M | **2.627M** billable subs (30 Jun 2026) | Not published in this pass (see §4) | Truly global, pole to pole | A |
| **Globalstar** 🇺🇸 (Apple-backed) | Messaging, IoT, Apple Emergency SOS | ~24 2nd-gen; C-3 refresh (48 + 6 spares) pending | **$273.0M** (FY2025, +9%); Q2 2026 $64.8M | Apple iPhone users (85% of capacity reserved for Apple) + IoT | Not published | Near-global, gateway-dependent (bent pipe) | A/C |
| **Amazon Leo** (Kuiper) 🇺🇸 | Broadband | **396** operational (of 3,232 planned) | Pre-revenue | Enterprise beta only; no commercial service yet | Not yet measured | Beta: US, UK, FR, DE, CA planned | B/C |
| **AST SpaceMobile** 🇺🇸 | Broadband direct-to-phone | ~12–13 BlueBirds (BB7 lost/being deorbited) | **$14.7M** Q1 2026; FY2026 guidance $150–200M | MNO partners (AT&T, Verizon, Vodafone, Rakuten); beta only | Not yet measured | Non-continuous; continuous needs ~45–60 sats (H1 2027) | A/B |
| **Guowang** (China SatNet) 🇨🇳 | State broadband | 204 LEO (+3 high-orbit, 27 test) as of Sep 2026; ~13,000 planned | Not disclosed | Not disclosed; no mature public service | — | Domestic/early | B |
| **Qianfan / Spacesail** 🇨🇳 | Commercial broadband | 162–218 (sources disagree; 218 per MIIT, Jul 2026); ~15,000 planned | Not disclosed | Early international MoUs; no mature service | — | Early | B/C |
| **Telesat Lightspeed** 🇨🇦 | Enterprise / government broadband | 0 (first pathfinders ~Dec 2026); 198 ordered, 156 funded | Pre-revenue (Telesat's GEO revenue is declining) | Backlog with enterprise/government | — | Global service from 2027 (once 96 sats up) | B |
| **IRIS²** 🇪🇺 | Sovereign secure connectivity | 0; 348 planned (330 LEO + 18 MEO) | ~€15.6B programme cost | EU governments + commercial | — | Service from 2029 | B |
| **Sateliot** 🇪🇸 | 5G NB-IoT NTN (Rel-17), store & forward | Small fleet; 5 more on Transporter-18 (planned 29 Sep 2026) | Not disclosed (2030 target ~$1B, old projection) | MNO roaming (Telefónica, Deutsche Telekom) | Store & forward: minutes, not ms | Intermittent, global over time | B/C |
| **OQ Technology** 🇱🇺 | 5G NTN IoT → D2D | ~10–12 | Not disclosed | MNO roaming (KPN, Deutsche Telekom), energy/maritime IoT | Intermittent | Intermittent global; D2D targeted end-2026 | B |
| **Lynk Global** 🇺🇸 (merging with Omnispace) | D2D SMS | 5–6 | Not disclosed | MNO partners | — | Service mid-2027; 640 more planned | B |

---

## 2. Market shape in three numbers

1. **Starlink is almost the whole market.** ~11,100 working satellites against ~650 for OneWeb and ~400 for Amazon Leo. That is roughly two-thirds or more of all active satellites in orbit. Its $11.4B 2025 revenue is ~13× all of Iridium's.
2. **ARPU is falling while subscribers double.** Starlink subscribers went from ~6M (Jun 2025) to ~12M (Jun 2026), but average revenue per user fell from $99/month (2023) to $86 (Q1 2025) to $66 (Q1 2026). Growth comes from cheaper plans and emerging markets.
3. **Satellite IoT is small and fragmented.** ~7M connections in 2025, ~€390M connectivity revenue, 44 operators of which only 17 offer commercial service. The forecast is 42M connections / ~€2.0B by 2030 (43% CAGR).

---

## 3. Operator notes

### Starlink (SpaceX)
- **Fleet:** ~11,100 working in Sep–Oct 2026 (McDowell via azmth.space; CelesTrak active catalog 11,151 on 18 Oct 2026). About 9,600 as of the 31 Mar 2026 S-1 cut-off. Laser ISLs on all current satellites.
- **Revenue:** Connectivity segment $11.4B revenue and $4.4B operating income in FY2025 (S-1). That made Starlink SpaceX's profit engine.
- **Customers:** 2.3M (2023) → 4.4M (2024) → 8.9M (end 2025) → 10.3M (31 Mar 2026, S-1) → ~12M (Jun 2026). Quilty projects 16.8M by end of 2026. Segments: consumer, maritime, aviation, enterprise, government (Starshield).
- **Direct-to-Cell:** T-Mobile "T-Satellite" has been commercial since July 2025, on ~650 D2C satellites in ~22 countries. The ~10M D2C user figure is secondary and unconfirmed. SpaceX bought EchoStar's AWS-4/H-Block spectrum (deal valued at up to $17B; FCC approved May 2026). Next-generation "Starlink Mobile" satellites are due in 2027.
- **Latency:** Ookla median was 45 ms in Q1 2025, with a vendor-claimed ~33 ms US peak-hour median in early 2026 (weakly sourced). An academic study using RIPE Atlas data found higher medians (~80 ms in 2024) because it measures differently. **Treat "25–60 ms" as the realistic range.**

### Eutelsat OneWeb
- **Fleet:** 654 Gen-1 satellites at ~1,200 km in polar orbits. Eutelsat has ordered 440 next-gen satellites from Airbus (a further 229-satellite / ~€1B batch extends launches to 2034; how that batch relates to the 440 is unclear).
- **Revenue:** FY2025-26 LEO revenue was €297M (+69.5%), about a quarter of group revenue. Guidance for FY2026-27 is only slight overall growth with flat margins.
- **Customers:** Wholesale only, sold through telcos and distributors: maritime (e.g. Station Satcom), aviation, rail (Kymeta, Hughes terminals), government and military (Ukraine is a major driver) and Arctic users (Tusass/Greenland, Northern Canada).
- **Latency:** <70 ms marketed. Its higher orbit gives a slightly higher physical floor than Starlink's.
- **Strategic note:** OneWeb is Europe's only operating LEO broadband fleet and is a core partner in IRIS² (~€2B Eutelsat commitment).

### Iridium
- **Fleet:** 66 operational Iridium NEXT satellites at ~780 km, with RF cross-links. It has been the reference ISL mesh since the late 1990s.
- **Revenue:** $871.7M in FY2025 ($634.0M service, $156.6M engineering, $81.1M equipment). Q2 2026 was $225.2M (+4%).
- **Customers:** 2.627M billable subscribers (30 Jun 2026, +6% YoY), driven by commercial IoT (+9%). The US government is an anchor customer.
- **Corporate:** Rocket Lab agreed on 28 Jun 2026 to acquire Iridium, closing expected mid-2027. Iridium has stopped giving guidance.

### Globalstar
- **Fleet:** ~24 second-generation satellites. The C-3 constellation (48 + 6 spares, ~35 gateways; MDA prime, Rocket Lab buses) is delayed. The first 9-satellite Falcon 9 batch was slated for mid-2026 but its launch is not confirmed.
- **Revenue:** $273.0M in FY2025 (record, +9%). Q2 2026 was $64.8M with record commercial IoT activations.
- **Customers:** Effectively Apple. Apple holds 20% of Globalstar, has committed up to $1.5B, funds 95% of the refresh and has 85% of capacity reserved. The rest is IoT (SPOT, asset trackers).

### Amazon Leo (formerly Project Kuiper)
- **Fleet:** 396 operational (398 launched on 15 flights) of 3,232 planned. The next launch is Vulcan LV-01 with 45 satellites, NET 29 Oct 2026.
- **Status:** Amazon missed its mid-2026 service target. The FCC granted a conditional waiver (5 Jun 2026) of the July 2026 half-constellation (1,616) milestone. Enterprise beta is intermittent, and Amazon says service will start late 2026 or early 2027. Bundling with Prime is reported.

### AST SpaceMobile
- **Fleet:** ~12–13 BlueBirds. BB7 was stranded by a New Glenn upper-stage issue and is being deorbited (insured). BB14–16 are at the Cape.
- **Revenue:** $14.7M in Q1 2026, mostly gateway deliveries and US government work. FY2026 guidance is $150–200M.
- **Customers:** MNOs (AT&T, Verizon, Vodafone, Rakuten). US beta will have non-continuous coverage. Continuous service has slipped to H1 2027 and needs ~45 satellites.

### China: Guowang and Qianfan
- Guowang has 204 LEO satellites (Sep 2026) toward ~13,000. Qianfan has 162–218 toward ~15,000.
- Both launch steadily on Long March 5B/6/6A/8/8A, but neither has a mature public service yet. Revenue and customers are not disclosed.

### Telesat Lightspeed, IRIS², and IoT/D2D niche players
- **Telesat Lightspeed:** 198 ordered from MDA, 156 funded. First pathfinders ~Dec 2026 on Falcon 9 (14 launches contracted). Global service is due in 2027 once 96 satellites are up. Telesat is in talks with its GEO debtholders.
- **IRIS²:** Implementation agreement signed Aug 2026. 348 satellites, ~€15.6B, service from 2029. Only ~€2.4B of EU money is firmly committed so far.
- **Sateliot / OQ / Lynk:** Fleets of tens of satellites or fewer. They earn MNO roaming and IoT revenue rather than consumer revenue. Deutsche Telekom's multi-orbit IoT roaming (Feb 2026) uses both Sateliot and OQ. Lynk is merging with Omnispace, with service due mid-2027.

---

## 4. Latency: physics, not marketing

Where no measured figure exists, the physical floor is a useful bound. A bent-pipe round trip (user → sat → gateway → sat → user) is at least `4 × altitude / c`:

| Orbit | Altitude | Physical RTT floor (zenith) | Real-world typical |
|---|---|---|---|
| Starlink LEO | ~550 km | ~7 ms | 25–60 ms (routing, scheduling, ground backhaul) |
| OneWeb LEO | ~1,200 km | ~16 ms | <70 ms marketed |
| Iridium LEO | ~780 km | ~10 ms | No verified figure found; ISL multi-hop and voice codec add significant delay |
| MEO (O3b mPOWER) | ~8,000 km | ~107 ms | ~150 ms class |
| GEO (Skylo, Inmarsat, Viasat) | 35,786 km | ~477 ms | ~600 ms+ |
| Store & forward IoT (Sateliot, OQ today) | LEO | n/a | Minutes to hours, depending on pass and gateway geometry |

> The floors above are first-principles calculations, not measurements. Slant range at low elevation can add 2–3× to the space segment.

---

## 5. What this means for Lynq / OQ

- **Broadband scale is settled.** Starlink has ~17× OneWeb's fleet and growing ARPU pressure. Nobody under ~$10B of capital competes there. This supports positioning NTN-Pulse in IoT/D2D and sovereignty, not throughput (consistent with `01-research/07-COMPETITIVE-LANDSCAPE.md`).
- **IoT revenue pools are small but real.** Iridium's IoT growth (+9% subs) and the ~€390M → €2B satellite IoT forecast are the benchmark revenue pool. OQ and Sateliot compete for the MNO-roaming slice of it.
- **Europe has a gap until 2029.** OneWeb is the only operating European LEO system, and IRIS² arrives in 2029 at the earliest. A regenerative 5G NTN operator that interoperates with IRIS² fills that window.
- **Store-and-forward latency is the weak point** against Starlink D2C and Iridium. Lynq's ISL routing and policy engine directly attacks it, and §4 gives the numbers to cite.

---

## 6. Sources

**Starlink / SpaceX**
- [Starlink — Wikipedia](https://en.wikipedia.org/wiki/Starlink)
- [SpaceX's IPO Filing Gives First Look Into Company's Financials — Via Satellite (20 May 2026)](https://www.satellitetoday.com/finance/2026/05/20/spacexs-ipo-filing-gives-first-look-into-companys-financials/)
- [6 Charts on SpaceX's Pre-IPO Financials — Morningstar](https://www.morningstar.com/stocks/6-charts-spacexs-s-1-financials)
- [SpaceX S-1 breakdown — Mostly Metrics](https://www.mostlymetrics.com/p/spacex-ipo-s1-breakdown)
- [SpaceX Revenue by Segment — Midgard Finance](https://www.midgardfinance.com/research/spacex/)
- [Starlink Statistics 2026 — Axis Intelligence](https://axis-intelligence.com/starlink-statistics/)
- [Starlink is SpaceX's cash machine, but the maths is getting harder — The Next Web](https://thenextweb.com/news/starlink-is-spacexs-cash-machine-but-the-maths-is-getting-harder)
- [How Many Starlink Satellites Are in Orbit? (Oct 2026) — azmth.space](https://azmth.space/answers/how-many-starlink-satellites)
- [How Many Starlink Satellites Are in Orbit as of October 9 — HighSpeedInternet](https://www.highspeedinternet.com/resources/how-many-starlink-satellites-are-in-orbit-october-9-2026)
- [SpaceX Plans Starlink Mobile Service — MacRumors (5 Aug 2026)](https://macrumors.com/2026/08/05/starlink-mobile-service)
- [Starlink Economics in 2026 — PDP Spectra](https://pdpspectra.com/blog/spacex-starlink-economics-2026)
- [Starlink speeds and latency — Orbital Radar](https://orbitalradar.com/satellite-internet/speeds-and-latency)
- [IFIP Networking 2025 paper on Starlink latency](https://dl.ifip.org/db/conf/networking/networking2025/1571125226.pdf)

**Eutelsat OneWeb**
- [OneWeb broadband satellites help lift LEO revenues 69.5% at Eutelsat — ISPreview (Aug 2026)](https://www.ispreview.co.uk/index.php/2026/08/oneweb-broadband-satellites-help-lift-leo-revenues-69-5-percent-at-eutelsat.html)
- [Eutelsat sees revenue growth as OneWeb expands — The Star (7 Aug 2026)](https://www.thestar.com.my/tech/tech-news/2026/08/07/starlink-rival-eutelsat-sees-revenue-growth-in-2027-on-oneweb-momentum)
- [Eutelsat buys another 229 satellites for OneWeb — DCD](https://www.datacenterdynamics.com/en/news/eutelsat-buys-another-229-satellites-for-oneweb-from-airbus-for-1bn/)
- [Eutelsat and Tusass expand partnership (Greenland) — Business Wire](https://www.businesswire.com/news/home/20251001454225/en/Eutelsat-and-Tusass-Expand-Strategic-Partnership-to-Bring-Resilient-LEO-Connectivity-to-Greenland)
- [OneWeb Satellite Network — Ground Control](https://www.groundcontrol.com/?p=29646)

**Iridium / Globalstar**
- [Iridium Q2 2026 results — SEC 8-K](https://www.sec.gov/Archives/edgar/data/0001418819/000141881926000046/pressreleaseq22026.htm)
- [Iridium Reports 4% Revenue Growth in Q2 Amid Rocket Lab Acquisition — Via Satellite](https://www.satellitetoday.com/finance/2026/07/22/iridium-reports-4-revenue-growth-in-q2-amid-rocket-lab-acquisition-deal/)
- [Iridium Announces 2025 Results — Seeking Alpha PR](https://seekingalpha.com/pr/20397311)
- [Globalstar Q4 and FY2025 Results — Seeking Alpha PR](https://seekingalpha.com/pr/20417442)
- [Globalstar orders another SpaceX launch — Via Satellite](https://www.satellitetoday.com/connectivity/2025/07/07/globalstar-orders-another-spacex-launch-for-constellation-refresh/)
- [Globalstar Q3: MDA satellites delayed — Via Satellite](https://www.satellitetoday.com/connectivity/2025/11/07/globalstar-q3-no-comment-on-report-of-potential-sale-mda-satellites-are-delayed)
- [iPhones may soon use satellite connections indoors — Computerworld](https://www.computerworld.com/article/3827951/iphones-may-soon-be-able-to-use-satellite-connections-indoors.html)

**Amazon Leo / AST / Telesat / China / IRIS² / IoT**
- [Amazon Leo — Wikipedia](https://en.wikipedia.org/wiki/Amazon_Leo) · [List of Amazon Leo launches](https://en.wikipedia.org/wiki/List_of_Amazon_Leo_launches)
- [Amazon Leo enough satellites to start service — GeekWire](https://www.geekwire.com/2026/amazon-leo-atlas-ula-launch-satellites/)
- [Vulcan Amazon Leo LV-01 — Space Launch Schedule](https://www.spacelaunchschedule.com/launch/vulcan-vc6l-amazon-leo-lv-01/)
- [AST SpaceMobile Q1 2026 Results](https://feeds.issuerdirect.com/news-release.html?newsid=7605011367480241&symbol=ASTS)
- [AST revenue nears $15m — Mobile World Live](https://www.mobileworldlive.com/ast-spacemobile/ast-revenue-nears-15m-bird-launches-gather-pace/)
- [AST reaches 13 BlueBirds — GCN](https://gcn.com/ast-spacemobile-bluebird-satellites-orbit/20491/)
- [BlueBird Tracker — Orbital Nodes](https://orbitalnodes.ai/bluebird/)
- [Telesat: Lightspeed pathfinders late 2026 — Space Intel Report](https://www.spaceintelreport.com/?p=108397)
- [Telesat advances toward 2026 Lightspeed launch — SpaceQ](https://spaceq.ca/telesat-advances-toward-2026-lightspeed-launch-as-geo-revenues-decline-but-guidance-holds-steady/)
- [Guowang — Wikipedia](https://en.wikipedia.org/wiki/Guowang)
- [China megaconstellation launches (Apr 2026) — Cislunar Space](https://cislunarspace.cn/en/space-news/2026/04/2026-04-10-china-megaconstellation-launches/)
- [Long March 6 launches 18 Qianfan satellites — Cislunar Space](https://cislunarspace.cn/en/space-news/2026/07/2026-07-01-qianfan-18-satellites-long-march-6/)
- [IRIS² — Wikipedia](https://en.wikipedia.org/wiki/IRIS%C2%B2)
- [Commission accelerates IRIS² deployment — EUSPA](https://www.euspa.europa.eu/newsroom-events/news/commission-accelerates-iris2-deployment-enhanced-security-and-expanded)
- [Europe increases IRIS² project size — Advanced Television](https://www.advanced-television.com/2026/08/10/europe-increases-iris2-project-size/)
- [Satellite IoT subscribers to hit 42M by 2030 — TelecomLead](https://telecomlead.com/?p=127985)
- [OQ Technology targets D2D services — Light Reading](https://www.lightreading.com/satellite/satellite-startup-oq-technology-targets-d2d-services-in-late-2026)
- [OQ Technology secures $30M from Europe — SpaceNews](https://spacenews.com/oq-technology-secures-30-million-from-europe-for-satellite-to-smartphone-expansion/)
- [Sateliot](https://sateliot.space/) · [Lynk Global promises service in 2027 — Advanced Television](https://www.advanced-television.com/2026/04/14/lynk-global-promise-service-in-2027/)
