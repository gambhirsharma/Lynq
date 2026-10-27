// Builds the 10-minute pitch deck: node build.js ../lynq-ntn-pulse-pitch.pptx
// Needs pptxgenjs, react, react-dom, react-icons, sharp (NODE_PATH works).
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const lu = require("react-icons/lu");

const SKILL = process.env.PPTX_SKILL;
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));
const OUT = process.argv[2] || "../lynq-ntn-pulse-pitch.pptx";
const LOGO = path.join(__dirname, "../../02-brand/lynq-brand-kit/logos/orbital-link/icon/png/lynq-orbital-link-icon-dark-1024.png");

// Lynq brand, dark theme (02-brand/lynq-brand-kit/BRAND-GUIDE.md)
const HEX = {
  bg: "0E0E0E", surface: "1C1C21", card: "2F2F37", white: "FFFFFF", grey: "A0A0A8", dim: "6B6B73",
  cyan: "3FD0E0", orange: "FAA055", alert: "FF5A5F", ok: "5BD69A", violet: "9B8CFF", line: "3A3A42",
};
const THEME = {
  name: "Lynq Dark",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: HEX.bg, lt1: HEX.white, dk2: HEX.surface, lt2: HEX.grey,
    accent1: HEX.cyan, accent2: HEX.orange, accent3: HEX.alert, accent4: HEX.ok, accent5: HEX.violet, accent6: HEX.dim,
    hlink: HEX.cyan, folHlink: HEX.violet,
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.title = "Lynq NTN-Pulse: 10-minute pitch";
pres.author = "Team Lynq";
pres.company = "Team Lynq";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
// Dark deck: background is dk1, text is lt1
const BG = C.text1, TXT = C.background1, MUTED = C.background2, PANEL = C.text2;
const CYAN = C.accent1, ORANGE = C.accent2, ALERT = C.accent3, OK = C.accent4, VIOLET = C.accent5, DIM = C.accent6;

async function icon(name, color, px = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(lu[name], { color: "#" + color, size: px }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---------- layouts ----------
const FOOT = { y: 7.0, h: 0.3 };
pres.defineSlideMaster({
  title: "LYNQ_TITLE",
  background: { color: BG },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.35, w: 11.0, h: 1.6, fontSize: 54, bold: true, color: TXT, align: "left", valign: "bottom", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.05, w: 8.6, h: 1.2, fontSize: 24, color: MUTED, align: "left", valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "LYNQ_CONTENT",
  background: { color: BG },
  margin: [0.5, 0.6, 0.6, 0.6],
  objects: [
    { image: { x: 0.6, y: FOOT.y + 0.02, w: 0.26, h: 0.26, path: LOGO } },
    { text: { text: "LYNQ NTN-PULSE  ·  NEOSPACE EUROPE 2026", options: { x: 0.95, y: FOOT.y, w: 6, h: FOOT.h, fontSize: 10, color: DIM, charSpacing: 1, margin: 0, valign: "middle" } } },
    { text: { text: "CHALLENGE BY OQ TECHNOLOGY", options: { x: 7.4, y: FOOT.y, w: 4.9, h: FOOT.h, fontSize: 10, color: DIM, charSpacing: 1, align: "right", margin: 0, valign: "middle" } } },
    { placeholder: { options: { name: "kicker", type: "body", x: 0.6, y: 0.4, w: 12.1, h: 0.35, fontSize: 12, bold: true, color: CYAN, charSpacing: 2, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.75, w: 12.1, h: 0.7, fontSize: 30, bold: true, color: TXT, align: "left", margin: 0, valign: "top" }, text: "" } },
  ],
  slideNumber: { x: 12.35, y: FOOT.y, w: 0.4, h: FOOT.h, fontSize: 10, color: DIM, align: "right" },
});

// ---------- helpers ----------
let objN = 0;
const nm = (s) => `${s}-${++objN}`;
function content(section, kicker, title) {
  const s = pres.addSlide({ masterName: "LYNQ_CONTENT", sectionTitle: section });
  s.addText(kicker.toUpperCase(), { placeholder: "kicker" });
  s.addText(title, { placeholder: "title" });
  return s;
}
function card(s, x, y, w, h, fill = PANEL) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { color: HEX.line, width: 0.75 }, objectName: nm("card") });
}
function text(s, t, o) {
  s.addText(t, { isTextBox: true, margin: 0, color: TXT, fontSize: 14, valign: "top", objectName: nm("text"), ...o });
}
function seg(s, x1, y1, x2, y2, line) {
  s.addShape(pres.shapes.LINE, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1) || 0.001, h: Math.abs(y2 - y1) || 0.001,
    flipV: (y2 < y1) !== (x2 < x1), line, objectName: nm("link") });
}
function dot(s, cx, cy, r, color, outline) {
  s.addShape(pres.shapes.OVAL, { x: cx - r, y: cy - r, w: 2 * r, h: 2 * r, fill: outline ? { type: "none" } : { color }, line: { color, width: outline ? 1.5 : 0.5 }, objectName: nm("node") });
}
async function iconBadge(s, name, x, y, d, color) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: PANEL }, line: { color, width: 1.25 }, objectName: nm("icon-ring") });
  const p = d * 0.22;
  s.addImage({ data: await icon(name, color), x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, objectName: nm("icon") });
}
const chartText = { catAxisLabelColor: HEX.grey, valAxisLabelColor: HEX.grey, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
  dataLabelFontFace: "+mn-lt", titleFontFace: "+mn-lt", catAxisLabelFontSize: 12, valAxisLabelFontSize: 11, dataLabelFontSize: 13,
  titleFontSize: 13, titleColor: HEX.white, dataLabelColor: HEX.white, valGridLine: { color: HEX.line, size: 0.5 }, catGridLine: { style: "none" },
  catAxisLineShow: false, valAxisLineShow: false, showLegend: false, showTitle: true };

(async () => {
  // =============== 1. Title ===============
  pres.addSection({ title: "Opening" });
  {
    const s = pres.addSlide({ masterName: "LYNQ_TITLE", sectionTitle: "Opening" });
    // orbit motif
    s.addShape(pres.shapes.OVAL, { x: 7.6, y: -1.4, w: 7.6, h: 7.6, fill: { type: "none" }, line: { color: HEX.white, width: 1, transparency: 88 }, objectName: "orbit-outer" });
    s.addShape(pres.shapes.OVAL, { x: 8.8, y: -0.2, w: 5.2, h: 5.2, fill: { type: "none" }, line: { color: HEX.white, width: 1, transparency: 90 }, objectName: "orbit-inner" });
    dot(s, 9.05, 4.85, 0.08, CYAN); dot(s, 11.4, 6.2, 0.08, CYAN); dot(s, 13.0, 4.3, 0.08, HEX.white);
    seg(s, 9.05, 4.85, 11.4, 6.2, { color: CYAN, width: 2.5 });
    s.addImage({ path: LOGO, x: 0.8, y: 0.8, w: 0.7, h: 0.7, objectName: "logo" });
    text(s, "Lynq", { x: 1.65, y: 0.85, w: 3, h: 0.6, fontSize: 30, bold: true, valign: "middle" });
    s.addText("Lynq NTN-Pulse", { placeholder: "title" });
    s.addText([
      { text: "Every signal, the right path.", options: { italic: true, color: CYAN, breakLine: true } },
      { text: "Digital twin + policy engine for OQ's regenerative gNB-onboard LEO constellation", options: { fontSize: 18 } },
    ], { placeholder: "body" });
    text(s, "AnyPoint-NTN challenge  ·  Next-Gen Downstream  ·  NEOSPACE Europe 2026, Luxembourg", { x: 0.8, y: 5.9, w: 9, h: 0.35, fontSize: 13, color: MUTED });
    text(s, "Davoud Jokar  ·  Ines Bouissou  ·  Gambhir Sharma  ·  Maryam Amini", { x: 0.8, y: 6.3, w: 9, h: 0.35, fontSize: 13, color: DIM });
    s.addNotes(`[0:00–0:30]
Good morning. We are Team Lynq, pronounced "link". OQ asked for a gNB-onboard LEO constellation that can serve any point on Earth, and for three things: an architecture sized to a coverage and latency target, a regulatory pathway, and a first business case.

Our answer is Lynq NTN-Pulse: a digital twin and policy engine that sits on top of OQ's regenerative satellites and decides, for every single message, which path it should take. Our tagline says it: every signal, the right path.

In the next ten minutes: the problem, our architecture, latency and coverage numbers from our simulation, the regulatory pathway, the business case, and what we want to do next.`);
  }

  // =============== 2. Problem ===============
  pres.addSection({ title: "Problem" });
  {
    const s = content("Problem", "01 · The problem", "Bent-pipe satellites fail where offshore assets need them");
    const cols = [
      ["LuRadioTower", ALERT, "No gateway, no service", "A bent-pipe satellite only relays. If no ground gateway is in view at the same time as the terminal, the message waits or drops."],
      ["LuBan", ORANGE, "Gateway not allowed", "A gateway can be in view but blocked by national rules, data residency or licensing. Technically fine, legally unusable."],
      ["LuTriangleAlert", CYAN, "Mixed traffic, one queue", "A shutdown alarm and a 100 kB log file get the same treatment. Critical traffic should never wait behind bulk data."],
    ];
    for (let i = 0; i < 3; i++) {
      const x = 0.6 + i * 4.13, y = 2.0, w = 3.83, h = 3.15;
      card(s, x, y, w, h);
      await iconBadge(s, cols[i][0], x + 0.35, y + 0.35, 0.75, cols[i][1]);
      text(s, cols[i][2], { x: x + 0.35, y: y + 1.3, w: w - 0.7, h: 0.45, fontSize: 18, bold: true });
      text(s, cols[i][3], { x: x + 0.35, y: y + 1.8, w: w - 0.7, h: 1.25, fontSize: 14, color: MUTED });
    }
    card(s, 0.6, 5.45, 12.1, 1.2, C.text2);
    await iconBadge(s, "LuWind", 0.9, 5.65, 0.8, CYAN);
    text(s, [
      { text: "Who is hit hardest: ", options: { bold: true, color: CYAN } },
      { text: "offshore wind farms, oil & gas platforms, vessels and pipelines in the North Sea (~51–61°N), far from terrestrial cells, across five national sectors (UK, NO, DK, NL, DE)." },
    ], { x: 1.95, y: 5.6, w: 10.5, h: 0.9, fontSize: 16, valign: "middle" });
    s.addNotes(`[0:30–1:30]
Today most satellite IoT is bent-pipe. The satellite is a mirror: it only relays the signal down to a ground gateway. That creates three problems.

First, no gateway in view means no service. The terminal and a gateway must both see the same satellite at the same moment.

Second, a gateway can be in view but not allowed. National rules, data residency or licensing can forbid landing a given country's traffic there.

Third, all traffic is treated the same. A shutdown alarm queues behind a log file.

The people hit hardest are offshore operators: wind farms, platforms, vessels and pipelines in the North Sea, spread over five national sectors. That is our beachhead.`);
  }

  // =============== 3. Solution ===============
  {
    const s = content("Problem", "02 · Our answer", "NTN-Pulse picks a compliant path for every message");
    // orbit arc + path diagram
    s.addShape(pres.shapes.OVAL, { x: -2.0, y: 2.25, w: 17.3, h: 6.0, fill: { type: "none" }, line: { color: HEX.white, width: 1, transparency: 85 }, objectName: "orbit-arc" });
    const T = [1.3, 4.10], A = [3.0, 2.53], B = [5.6, 2.33], Cc = [8.2, 2.30], GB = [4.7, 4.10], GA = [9.5, 4.10], CL = [11.9, 4.10];
    seg(s, A[0], A[1], GB[0], GB[1], { color: HEX.dim, width: 1.75, dashType: "sysDot" });
    seg(s, T[0], T[1], A[0], A[1], { color: CYAN, width: 3 });
    seg(s, A[0], A[1], B[0], B[1], { color: CYAN, width: 3, dashType: "dash" });
    seg(s, B[0], B[1], Cc[0], Cc[1], { color: CYAN, width: 3 });
    seg(s, Cc[0], Cc[1], GA[0], GA[1], { color: CYAN, width: 3 });
    seg(s, GA[0], GA[1], CL[0] - 0.3, CL[1], { color: CYAN, width: 3 });
    [A, B, Cc].forEach((p) => dot(s, p[0], p[1], 0.12, CYAN));
    dot(s, 10.8, 2.62, 0.1, HEX.white);
    s.addShape(pres.shapes.RECTANGLE, { x: GA[0] - 0.14, y: GA[1] - 0.14, w: 0.28, h: 0.28, fill: { color: CYAN }, line: { color: CYAN, width: 1 }, objectName: "gw-ok" });
    s.addShape(pres.shapes.RECTANGLE, { x: GB[0] - 0.14, y: GB[1] - 0.14, w: 0.28, h: 0.28, fill: { type: "none" }, line: { color: HEX.dim, width: 2 }, objectName: "gw-blocked" });
    seg(s, GB[0] - 0.25, GB[1] + 0.25, GB[0] + 0.25, GB[1] - 0.25, { color: HEX.dim, width: 2 });
    s.addImage({ data: await icon("LuFactory", HEX.white), x: T[0] - 0.25, y: T[1] - 0.2, w: 0.5, h: 0.5, objectName: "terminal-icon" });
    s.addImage({ data: await icon("LuCloud", HEX.white), x: CL[0] - 0.3, y: CL[1] - 0.3, w: 0.6, h: 0.6, objectName: "cloud-icon" });
    const lab = (t, x, y, w, color = MUTED, align = "center") => text(s, t, { x, y, w, h: 0.3, fontSize: 12, bold: true, color, charSpacing: 1, align });
    lab("OFFSHORE TERMINAL", T[0] - 1.1, 4.50, 2.2);
    lab("ONBOARD gNB", A[0] - 1.0, 2.00, 2.0);
    lab("RF ISL", 3.8, 2.75, 1.4, CYAN);
    lab("OPTICAL ISL", 6.2, 1.85, 1.6, CYAN);
    lab("BLOCKED GW", GB[0] - 1.0, 4.50, 2.0, HEX.dim);
    lab("AUTHORISED GW", GA[0] - 1.1, 4.50, 2.2, CYAN);
    lab("5G CORE · CLOUD", CL[0] - 1.0, 4.50, 2.0);
    // traffic classes
    const cls = [
      ["CRITICAL", ALERT, "Alarms and shutdown commands. First uplink slot, first authorised path, this pass."],
      ["REGULAR", CYAN, "Telemetry, logs, files. Queued onboard and store-and-forwarded on a later pass (≤ 90 min)."],
      ["METADATA", VIOLET, "Status, position, policy tags. Tells the engine which gateway each asset may use."],
    ];
    for (let i = 0; i < 3; i++) {
      const x = 0.6 + i * 4.13, y = 5.0, w = 3.83, h = 1.7;
      card(s, x, y, w, h);
      dot(s, x + 0.45, y + 0.4, 0.09, cls[i][1]);
      text(s, cls[i][0], { x: x + 0.65, y: y + 0.24, w: 2.5, h: 0.32, fontSize: 14, bold: true, color: cls[i][1], charSpacing: 2 });
      text(s, cls[i][2], { x: x + 0.3, y: y + 0.7, w: w - 0.6, h: 1.0, fontSize: 14, color: MUTED });
    }
    s.addNotes(`[1:30–2:40]
Our answer is a software layer, NTN-Pulse. A digital twin models every satellite, gateway, link and queue; a policy engine assigns each message to a path.

Follow the cyan line. A platform sends a message to the gNB onboard the satellite overhead. The closest gateway is in view but blocked, for example a sector whose data may not land there. So instead of waiting, the satellite relays it over an RF link inside its plane, then an optical link across planes, down to an authorised gateway, and into the 5G core and cloud.

And because the gNB is onboard, the scheduler is in orbit too. Every message is sorted into three classes. Critical alarms go first, on the first authorised path, on this pass. Regular data like telemetry is stored onboard and forwarded within 90 minutes. Metadata tells the twin which gateway each asset may use.`);
  }

  // =============== 4. Architecture ===============
  pres.addSection({ title: "Technical" });
  {
    const s = content("Technical", "03 · Technical: architecture", "Regenerative gNB on every satellite, RF + optical mesh");
    const tiles = [
      ["~12 → 30", "satellites: 10 OQ + 2 ERMIS today, 30 planned"],
      ["3 × 10", "planes × satellites at ~500 km altitude"],
      ["10°", "minimum elevation, ~3,000 km footprint"],
      ["~6 / yr", "replacements at a 5-year design life"],
    ];
    for (let i = 0; i < 4; i++) {
      const x = 0.6 + (i % 2) * 2.95, y = 1.95 + Math.floor(i / 2) * 2.45, w = 2.75, h = 2.25;
      card(s, x, y, w, h);
      text(s, tiles[i][0], { x: x + 0.3, y: y + 0.4, w: w - 0.6, h: 0.7, fontSize: 34, bold: true, color: ORANGE });
      text(s, tiles[i][1], { x: x + 0.3, y: y + 1.2, w: w - 0.6, h: 0.75, fontSize: 13, color: MUTED });
    }
    const trades = [
      ["LuCpu", "Payload: full regenerative gNB", [
        ["Bent-pipe", "needs a gateway in view; can't serve open ocean"],
        ["Split gNB (2 / 7.2x)", "RRC still round-trips the feeder"],
        ["SWaP fix", "narrowband gNB, duty-cycling, rad-hard supervisor"],
      ]],
      ["LuRoute", "ISL: RF in-plane, optical cross-plane", [
        ["RF, every satellite", "static in-plane geometry, proven by Iridium"],
        ["Optical, relay subset", "no licence, EU suppliers, no ITAR"],
        ["Not all-optical", "IoT needs only single-digit Mbps per sat"],
      ]],
    ];
    for (let i = 0; i < 2; i++) {
      const x = 6.75, y = 1.95 + i * 2.45, w = 5.95, h = 2.25;
      card(s, x, y, w, h);
      await iconBadge(s, trades[i][0], x + 0.3, y + 0.25, 0.55, CYAN);
      text(s, trades[i][1], { x: x + 1.05, y: y + 0.3, w: w - 1.3, h: 0.45, fontSize: 18, bold: true, valign: "middle" });
      const runs = [];
      trades[i][2].forEach(([k, v], j) => runs.push(
        { text: k + ": ", options: { bold: true, color: TXT } },
        { text: v, options: { color: MUTED, breakLine: j < 2, paraSpaceAfter: 4 } }));
      text(s, runs, { x: x + 0.3, y: y + 0.95, w: w - 0.6, h: 1.2, fontSize: 13 });
    }
    s.addNotes(`[2:40–3:50]
The architecture. We start from OQ's real fleet, about 12 satellites today, ten OQ plus two ERMIS, and we size for the planned 30: three planes of ten at roughly 500 to 550 kilometres. At a 10-degree minimum elevation one footprint is about 3,000 kilometres wide, so one satellite in view covers the whole North Sea basin and every gateway around it.

The brief asked for two trade-offs.

Payload: we choose a full regenerative gNB. Bent-pipe cannot serve a user with no gateway in view, and a split gNB still keeps most of the RF power onboard while the RRC signalling round-trips to the ground. We keep power in check with a narrowband gNB and duty-cycling.

ISL: RF inside each plane, on every satellite, proven by Iridium for 25 years. Optical only across planes, on a subset of relay satellites: no spectrum licence, and European suppliers avoid ITAR. IoT needs only a few megabits, so all-optical isn't needed.`);
  }

  // =============== 5. Latency ===============
  {
    const s = content("Technical", "04 · Technical: latency", "ISL keeps alarms at ~100 ms even with a gateway down");
    card(s, 0.6, 1.95, 7.3, 4.7);
    s.addChart(pres.charts.BAR, [{ name: "Critical alarm median latency (s)", labels: ["Bent-pipe", "Regenerative, no ISL", "Regenerative + ISL"], values: [30.1, 35.1, 0.1] }], {
      x: 0.8, y: 2.1, w: 6.9, h: 4.4, barDir: "bar", chartColors: [HEX.dim, HEX.dim, HEX.cyan], barGapWidthPct: 60,
      title: "Median alarm latency to Frankfurt, seconds (30 satellites, Stavanger gateway offline)",
      showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0.0" s"', valAxisMaxVal: 40, valAxisLabelFormatCode: "0",
      catAxisOrientation: "maxMin", ...chartText, valGridLine: { color: HEX.line, size: 0.5 }, catGridLine: { style: "none" }, objectName: "latency-chart",
    });
    const stats = [
      ["~85 ms", "live alarm, platform → Frankfurt cloud (30 sats, all gateways up)", CYAN],
      ["75–110 ms", "mid-Atlantic platform → Frankfurt over the ISL mesh; bent-pipe: no service", ORANGE],
    ];
    stats.forEach(([n, l, col], i) => {
      const y = 1.95 + i * 1.55;
      card(s, 8.2, y, 4.5, 1.35);
      text(s, n, { x: 8.5, y: y + 0.15, w: 3.9, h: 0.6, fontSize: 32, bold: true, color: col });
      text(s, l, { x: 8.5, y: y + 0.75, w: 3.9, h: 0.55, fontSize: 12, color: MUTED });
    });
    card(s, 8.2, 5.05, 4.5, 1.6);
    text(s, "SERVICE TIERS", { x: 8.5, y: 5.2, w: 3.9, h: 0.3, fontSize: 12, bold: true, color: MUTED, charSpacing: 2 });
    [["Continuous", "< 150 ms", CYAN], ["Mesh-relayed", "< 250 ms", VIOLET], ["Store-and-forward", "≤ 90 min", C.background2]].forEach(([k, v, col], i) => {
      const y = 5.55 + i * 0.33;
      dot(s, 8.6, y + 0.14, 0.06, col);
      text(s, k, { x: 8.8, y, w: 2.3, h: 0.3, fontSize: 14, valign: "middle" });
      text(s, v, { x: 11.0, y, w: 1.4, h: 0.3, fontSize: 14, bold: true, color: col, align: "right", valign: "middle" });
    });
    s.addNotes(`[3:50–5:00]
Now the numbers. From our twin: 24 hours, 300 North Sea terminals, real orbits, link budgets and gateway rules.

With 30 satellites and all gateways up, a live alarm lands in the Frankfurt cloud in about 85 milliseconds, inside the continuous tier.

The chart is the interesting case. We take the Stavanger gateway offline. Norwegian-sector data is now only allowed to land at Svalbard. Bent-pipe and regenerative-without-ISL have to wait for a satellite that sees both the platform and Svalbard: the median alarm jumps to 30 to 35 seconds. With the ISL, the alarm simply relays north over the mesh and stays at about 100 milliseconds. Routing compliance was 100 percent in every scenario.

So the ISL is not just a speed feature. It is what makes sovereignty cheap.`);
  }

  // =============== 6. Coverage ===============
  {
    const s = content("Technical", "05 · Technical: coverage", "Orbit choice beats satellite count for the North Sea");
    card(s, 0.6, 1.95, 7.3, 4.7);
    s.addChart(pres.charts.BAR, [{ name: "Basin coverage", labels: ["12 sats, SSO (today)", "30 sats, SSO", "30 sats, 65° Walker"], values: [26, 61, 79] }], {
      x: 0.8, y: 2.1, w: 6.9, h: 4.4, barDir: "col", chartColors: [HEX.dim, HEX.grey, HEX.cyan], barGapWidthPct: 55,
      title: "Share of the day a satellite covers the North Sea basin (%)",
      showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0"%"', valAxisMaxVal: 100, valAxisMajorUnit: 25, valAxisLabelFormatCode: '0"%"', catAxisLabelRotate: 0,
      ...chartText, objectName: "coverage-chart",
    });
    text(s, "LONGEST COVERAGE GAP", { x: 8.2, y: 1.95, w: 4.5, h: 0.3, fontSize: 12, bold: true, color: MUTED, charSpacing: 2 });
    [["246 min", "12 sats today: passes, not coverage", HEX.dim], ["118 min", "30 sats, sun-synchronous planes", HEX.grey], ["3 min", "same 30 sats, 65° Walker delta", HEX.cyan]].forEach(([n, l, col], i) => {
      const y = 2.35 + i * 1.08;
      card(s, 8.2, y, 4.5, 0.93);
      text(s, n, { x: 8.45, y: y + 0.1, w: 1.9, h: 0.73, fontSize: 26, bold: true, color: col, valign: "middle" });
      text(s, l, { x: 10.35, y: y + 0.1, w: 2.2, h: 0.73, fontSize: 12, color: MUTED, valign: "middle" });
    });
    card(s, 8.2, 5.65, 4.5, 1.0);
    text(s, [
      { text: "75%", options: { bold: true, color: ORANGE, fontSize: 22 } },
      { text: " of alarms under 250 ms with the Walker delta (vs 59% on sun-synchronous)", options: { color: MUTED, fontSize: 13 } },
    ], { x: 8.45, y: 5.7, w: 4.05, h: 0.9, valign: "middle" });
    s.addNotes(`[5:00–6:00]
Coverage. With today's 12 satellites the basin is in view only about a quarter of the day, with gaps up to four hours. That is passes, not coverage. Alarms wait for the next pass, about seven minutes.

At 30, the in-plane RF ring closes and coverage rises to 61 percent. But the worst gap is still almost two hours.

Our most useful finding: keep the same 30 satellites, but fly them in a 65-degree Walker delta instead of sun-synchronous planes. Sun-synchronous orbits spread passes over the poles; 65 degrees concentrates them at North Sea latitudes. Coverage goes to 79 percent, the worst gap drops from 118 minutes to 3, and 75 percent of alarms land under 250 milliseconds.

So for this market, orbit design is worth more than extra satellites. That is the kind of decision the twin exists to make.`);
  }

  // =============== 7. Regulatory ===============
  pres.addSection({ title: "Regulatory" });
  {
    const s = content("Regulatory", "06 · Regulatory pathway", "Sovereignty is built into routing, starting in Luxembourg");
    const steps = [
      ["Luxembourg ILR / LSA", "Extend OQ's Nov-2025 concession to ISL and regenerative ops"],
      ["ITU BR via Luxembourg", "Priority filings: Art. 9 coordination, Art. 22 EPFD"],
      ["International waters", "No landing rights needed: earliest revenue"],
      ["North Sea regulators + MNOs", "UK, NO, DK, NL, DE for coastal coverage"],
      ["EC / CEPT", "S-band MSS (IoT) and C-band D2D spectrum"],
    ];
    const x0 = 0.6, gap = 2.47, cy = 2.3;
    seg(s, x0 + 0.3, cy, x0 + 4 * gap + 0.3, cy, { color: HEX.line, width: 2 });
    steps.forEach(([h, b], i) => {
      const x = x0 + i * gap;
      s.addShape(pres.shapes.OVAL, { x, y: cy - 0.3, w: 0.6, h: 0.6, fill: { color: i === 0 ? ORANGE : PANEL }, line: { color: ORANGE, width: 1.5 }, objectName: nm("step") });
      text(s, String(i + 1), { x, y: cy - 0.3, w: 0.6, h: 0.6, fontSize: 18, bold: true, align: "center", valign: "middle", color: i === 0 ? BG : ORANGE });
      text(s, h, { x, y: cy + 0.45, w: 2.3, h: 0.6, fontSize: 15, bold: true });
      text(s, b, { x, y: cy + 1.05, w: 2.25, h: 0.85, fontSize: 12, color: MUTED });
    });
    const cards = [
      ["LuShieldCheck", CYAN, "Data residency, lawful intercept", "The gNB knows identity, PLMN and verified location, so each flow lands only at an allowed gateway with local breakout. MNO keeps lawful intercept. 100% compliant in the twin."],
      ["LuScale", ORANGE, "Spectrum as a hard constraint", "ITU Art. 9 / Art. 22 EPFD limits, feeder-link masks and gateway exclusion zones are inputs to routing, not afterthoughts."],
      ["LuLock", VIOLET, "Export control and debris", "European optical ISL and gNB suppliers keep us outside ITAR/EAR. 5-year life, ~6 replacements a year, IADC deorbit compliance."],
    ];
    for (let i = 0; i < 3; i++) {
      const x = 0.6 + i * 4.13, y = 4.35, w = 3.83, h = 2.3;
      card(s, x, y, w, h);
      await iconBadge(s, cards[i][0], x + 0.3, y + 0.25, 0.55, cards[i][1]);
      text(s, cards[i][2], { x: x + 1.0, y: y + 0.25, w: w - 1.2, h: 0.55, fontSize: 15, bold: true, valign: "middle" });
      text(s, cards[i][3], { x: x + 0.3, y: y + 0.95, w: w - 0.6, h: 1.3, fontSize: 12, color: MUTED });
    }
    s.addNotes(`[6:00–7:15]
Regulation. The brief asks which authorities to engage first, and why.

One: Luxembourg, ILR and the Luxembourg Space Agency. OQ already holds a concession from November 2025; we extend it to ISL and regenerative operations.

Two: the ITU Radiocommunication Bureau, through Luxembourg, for priority filings: Article 9 coordination and the Article 22 EPFD limits that protect GSO systems.

Three: international waters. Offshore assets beyond territorial seas need no national landing rights, so this is where revenue can start earliest.

Four: the North Sea regulators and MNOs, UK, Norway, Denmark, the Netherlands and Germany, for coastal coverage. Five: EC and CEPT for spectrum.

The key idea is the bottom row. A regenerative gNB knows the user's identity, network and verified location. So we enforce data residency in the routing itself: each flow only lands at a gateway it is allowed to use, with local breakout, and the MNO keeps lawful intercept. In our twin, routing compliance was 100 percent in every scenario.`);
  }

  // =============== 8. Business case ===============
  pres.addSection({ title: "Economics" });
  {
    const s = content("Economics", "07 · Business case", "Start with North Sea offshore energy, priced per asset");
    card(s, 0.6, 1.95, 4.0, 4.7);
    await iconBadge(s, "LuWind", 0.9, 2.2, 0.75, CYAN);
    text(s, "First buyer", { x: 1.8, y: 2.3, w: 2.6, h: 0.55, fontSize: 20, bold: true, valign: "middle" });
    text(s, [
      { text: "European offshore energy operator or wind O&M provider (e.g. Equinor, Ørsted, Eni)", options: { breakLine: true, paraSpaceAfter: 8 } },
      { text: "Pain: blind spots, missed alarms, costly VSAT and fixed gateways", options: { breakLine: true, paraSpaceAfter: 8 } },
      { text: "Why first: international waters, sovereign-minded buyers, OQ's European funding focus" },
    ], { x: 0.9, y: 3.2, w: 3.45, h: 3.3, fontSize: 14, color: MUTED });

    card(s, 4.85, 1.95, 3.95, 4.7);
    text(s, "BREAK-EVEN", { x: 5.15, y: 2.2, w: 3.4, h: 0.3, fontSize: 12, bold: true, color: MUTED, charSpacing: 2 });
    text(s, "~€9M / yr", { x: 5.15, y: 2.55, w: 3.4, h: 0.7, fontSize: 36, bold: true, color: ORANGE });
    text(s, "opex for the North Sea network, incl. replenishment", { x: 5.15, y: 3.25, w: 3.4, h: 0.55, fontSize: 12, color: MUTED });
    text(s, [
      { text: "~75k assets", options: { bold: true, color: TXT, fontSize: 22, breakLine: true } },
      { text: "× €120 / yr IoT subscription", options: { color: MUTED, breakLine: true } },
      { text: "or", options: { color: DIM, breakLine: true } },
      { text: "~9k endpoints", options: { bold: true, color: TXT, fontSize: 22, breakLine: true } },
      { text: "× €1,000+ / yr sovereign / defence", options: { color: MUTED } },
    ], { x: 5.15, y: 4.0, w: 3.4, h: 2.5, fontSize: 13 });

    card(s, 9.05, 1.95, 3.65, 4.7);
    text(s, "REVENUE MODEL", { x: 9.35, y: 2.2, w: 3.1, h: 0.3, fontSize: 12, bold: true, color: MUTED, charSpacing: 2 });
    const rev = [["Integration fee", "per customer onboarding"], ["Subscription", "per asset and traffic class"], ["Priority QoS", "usage charge for critical tier"], ["MNO wholesale", "roaming for coastal coverage"]];
    rev.forEach(([k, v], i) => {
      const y = 2.65 + i * 0.85;
      dot(s, 9.45, y + 0.17, 0.06, CYAN);
      text(s, k, { x: 9.65, y, w: 2.9, h: 0.35, fontSize: 15, bold: true });
      text(s, v, { x: 9.65, y: y + 0.35, w: 2.9, h: 0.35, fontSize: 12, color: MUTED });
    });
    text(s, [{ text: "Per asset, never per byte: ", options: { bold: true, color: ORANGE } }, { text: "at ~€2–3/MB, byte pricing would kill adoption.", options: { color: MUTED } }],
      { x: 9.35, y: 5.85, w: 3.15, h: 0.6, fontSize: 12 });
    s.addNotes(`[7:15–8:30]
The business case. OQ asked for one viable segment first, not every segment at once.

Our first buyer is a European offshore energy operator or wind O&M provider, think Equinor, Ørsted or Eni. They have a real, expensive pain: blind spots, missed alarms, and dependence on VSAT and fixed gateways. They work in international waters and care about European sovereignty.

The unit economics. Running the North Sea network, including replacing satellites, costs about 9 million euros a year. We break even at about 75,000 offshore assets paying 120 euros a year, or at about 9,000 sovereign or defence endpoints at a thousand euros or more.

We price per asset, never per byte. At two to three euros per megabyte, byte pricing would kill adoption. Revenue comes from integration fees, per-asset subscriptions by traffic class, a usage charge for the priority tier, and MNO wholesale roaming along the coast.`);
  }

  // =============== 9. Benchmark ===============
  {
    const s = content("Economics", "08 · Benchmark", "We can't out-build the giants, so we out-position them");
    const hdr = (t) => ({ text: t, options: { bold: true, color: MUTED, fontSize: 12, fill: { color: BG }, charSpacing: 1 } });
    const row = (cells, hi) => cells.map((t, j) => ({ text: t, options: { fontSize: 13, color: hi ? (j === 0 ? CYAN : TXT) : (j === 0 ? TXT : MUTED), bold: j === 0 || hi, fill: { color: hi ? C.text2 : BG } } }));
    const rows = [
      [hdr("APPROACH"), hdr("EXAMPLE"), hdr("LATENCY / COVERAGE"), hdr("SOVEREIGNTY / COST")],
      row(["Bent-pipe NTN IoT", "Sateliot (~40 LEO)", "Waits for a gateway in view; store-and-forward", "EU, but Rel-17 bent-pipe only"]),
      row(["GEO NTN IoT", "Skylo", "~240 ms round trip, no polar coverage", "Rents someone else's satellites"]),
      row(["Regenerative direct-to-cell", "Starlink D2C, AST", "Low latency, huge ISL mesh", "US-controlled, billions in capex"]),
      row(["Proprietary RF mesh", "Iridium (66 sats)", "True global, proven since the 1990s", "Proprietary, never cheap"]),
      row(["Lynq NTN-Pulse on OQ", "~12 → 30 regen sats", "~85–100 ms alarms, 3-min worst gap (65° delta)", "EU-sovereign routing, 3GPP-open, per-asset"], true),
    ];
    s.addTable(rows, { x: 0.6, y: 2.0, w: 12.1, colW: [2.9, 2.4, 3.6, 3.2], rowH: 0.62, valign: "middle", margin: [0, 0.12, 0, 0.12],
      border: { type: "solid", pt: 0.75, color: HEX.line }, objectName: "benchmark-table" });
    card(s, 0.6, 5.95, 12.1, 0.7);
    await iconBadge(s, "LuShieldCheck", 0.75, 6.02, 0.56, ORANGE);
    text(s, [{ text: "Our edge: ", options: { bold: true, color: ORANGE } }, { text: "European sovereignty, data residency by design, and open 3GPP standards for buyers who will not route through US networks." }],
      { x: 1.5, y: 6.0, w: 11.0, h: 0.6, fontSize: 14, valign: "middle" });
    s.addNotes(`[8:30–9:15]
OQ asked us to benchmark against three families: bent-pipe NTN IoT, GEO NTN IoT, and regenerative direct-to-cell.

Sateliot is the closest analogue: wholesale to MNOs, store-and-forward, but still Rel-17 bent-pipe. Skylo owns no satellites and runs over GEO: about 240 milliseconds round trip and no polar coverage. Starlink and AST have already built the mesh this challenge describes, at a scale and capital level nobody here can match.

We are not trying to out-build any of them. We out-position them: European sovereignty, data residency enforced in routing, and open 3GPP standards, for offshore and institutional buyers who will not route their traffic through US networks.`);
  }

  // =============== 10. Risks & next steps ===============
  pres.addSection({ title: "Close" });
  {
    const s = content("Close", "09 · Risks and next steps", "De-risk with one paid pilot: a wind-farm alarm use case");
    const risks = [
      ["Payload", "Final power, compute, radiation and RAN limits may differ", "Payload-independent policies with cloud/gateway fallback"],
      ["ISL / regulatory", "ISL, gateway and spectrum choices may change", "Simulate both ISL types; ITU and national rules as hard constraints"],
      ["Adoption", "Customers may resist new terminals or uncertain SLAs", "One alarm use case, measured TCO, a paid pilot with SLA targets"],
    ];
    text(s, "RISK", { x: 0.6, y: 1.95, w: 2, h: 0.3, fontSize: 12, bold: true, color: MUTED, charSpacing: 2 });
    text(s, "MITIGATION", { x: 4.3, y: 1.95, w: 3, h: 0.3, fontSize: 12, bold: true, color: MUTED, charSpacing: 2 });
    risks.forEach(([k, r, m], i) => {
      const y = 2.35 + i * 1.47;
      card(s, 0.6, y, 7.2, 1.3);
      text(s, k, { x: 0.85, y: y + 0.18, w: 3.2, h: 0.35, fontSize: 15, bold: true, color: ALERT });
      text(s, r, { x: 0.85, y: y + 0.55, w: 3.2, h: 0.65, fontSize: 12, color: MUTED });
      text(s, m, { x: 4.3, y: y + 0.18, w: 3.3, h: 1.0, fontSize: 13, valign: "middle" });
    });
    card(s, 8.1, 1.95, 4.6, 4.7);
    await iconBadge(s, "LuRocket", 8.4, 2.2, 0.7, ORANGE);
    text(s, "Next steps", { x: 9.3, y: 2.3, w: 3.2, h: 0.5, fontSize: 20, bold: true, valign: "middle" });
    text(s, [
      { text: "Phase 2 (here): live twin of one offshore corridor at 12 and 30 sats, bent-pipe vs regenerative", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
      { text: "Validate the 65° Walker delta with OQ's launch plan", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
      { text: "Paid pilot with one North Sea operator: latency, availability, delivery targets", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
      { text: "Orbit-aware fleet updates: 1.2 h with ISL vs 21 h without", options: { bullet: true } },
    ], { x: 8.4, y: 3.15, w: 4.05, h: 3.35, fontSize: 14, color: MUTED });
    s.addNotes(`[9:15–9:45]
The risks are honest ones. The final payload limits may differ, so our policies are payload-independent and fall back to the ground. ISL and spectrum choices may change, so the twin simulates both and treats regulation as a hard constraint. And customers may resist new terminals, so we start with one alarm use case and a paid pilot with real SLA targets.

Next steps: in this Phase 2 we demo the live twin. Then we validate the 65-degree orbit with OQ's launch plan, and run a paid pilot with one North Sea operator. With the ISL, a software update reaches all 30 satellites in about an hour, versus 21 without.`);
  }

  // =============== 11. Closing ===============
  {
    const s = pres.addSlide({ masterName: "LYNQ_TITLE", sectionTitle: "Close" });
    s.addShape(pres.shapes.OVAL, { x: 7.6, y: -1.4, w: 7.6, h: 7.6, fill: { type: "none" }, line: { color: HEX.white, width: 1, transparency: 88 }, objectName: "orbit-outer" });
    s.addShape(pres.shapes.OVAL, { x: 8.8, y: -0.2, w: 5.2, h: 5.2, fill: { type: "none" }, line: { color: HEX.white, width: 1, transparency: 90 }, objectName: "orbit-inner" });
    s.addImage({ path: LOGO, x: 0.8, y: 0.8, w: 0.7, h: 0.7, objectName: "logo" });
    text(s, "Lynq", { x: 1.65, y: 0.85, w: 3, h: 0.6, fontSize: 30, bold: true, valign: "middle" });
    s.addText("Every signal, the right path.", { placeholder: "title" });
    s.addText("Thank you. Questions?", { placeholder: "body" });
    const take = [["~85 ms", "alarms to the cloud", CYAN], ["3 min", "worst North Sea gap", CYAN], ["100%", "routing compliance", ORANGE]];
    take.forEach(([n, l, col], i) => {
      const x = 0.8 + i * 2.9;
      text(s, n, { x, y: 5.3, w: 2.7, h: 0.65, fontSize: 32, bold: true, color: col });
      text(s, l, { x, y: 5.95, w: 2.7, h: 0.35, fontSize: 14, color: MUTED });
    });
    s.addNotes(`[9:45–10:00]
To sum up: alarms reach the cloud in about 85 milliseconds, the right orbit cuts the worst North Sea gap to three minutes, and every flow lands only where it is allowed to. Every signal, the right path. Thank you, we're happy to take questions, and to show the live dashboard.`);
  }

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
