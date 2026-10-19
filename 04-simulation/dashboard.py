"""Lynq NTN-Pulse dashboard.   streamlit run dashboard.py"""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ntnpulse import config as cfg
from ntnpulse.engine import Simulation

# Categorical slots validated (dataviz validate_palette.js, dark, surface #1C1C21): all checks pass.
SLOT = ("#1FA3B2", "#D9772A", "#8B70E6")
MODE_COLOR = dict(zip(("regen_isl", "regen", "bent_pipe"), SLOT))
CLASS_COLOR = dict(zip(("critical", "metadata", "regular"), SLOT))
CLASS_SYMBOL = {"critical": "triangle-up", "metadata": "diamond", "regular": "circle"}
BG, SURFACE, TEXT, MUTED, GRID = "#0E0E0E", "#1C1C21", "#FFFFFF", "#999999", "#2F2F37"
OK, ALERT = "#5BD69A", "#FF5A5F"

st.set_page_config(page_title="Lynq NTN-Pulse", page_icon="🛰️", layout="wide")
st.markdown(f"""<style>
  [data-testid="stMetric"] {{ background:{SURFACE}; border:1px solid rgba(255,255,255,.08);
                              border-radius:12px; padding:14px 16px; }}
  [data-testid="stMetricLabel"] p {{ color:{MUTED}; }}
</style>""", unsafe_allow_html=True)


def style(fig: go.Figure, height=360, **kw) -> go.Figure:
    fig.update_layout(
        height=height, paper_bgcolor=SURFACE, plot_bgcolor=SURFACE, font=dict(color=TEXT, family="Urbanist, sans-serif"),
        margin=dict(l=56, r=24, t=48, b=48), hovermode=kw.pop("hovermode", "x unified"),
        legend=dict(orientation="h", y=1.02, yanchor="bottom", x=0, bgcolor="rgba(0,0,0,0)"), **kw)
    fig.update_xaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    return fig


# --- sidebar --------------------------------------------------------------------------
st.sidebar.title("Lynq NTN-Pulse")
st.sidebar.caption("Digital twin of a regenerative gNB-onboard LEO constellation over the North Sea.")

PRESETS = {
    "112 (7x16 design, 700 km, 87 deg)": cfg.CONSTELLATIONS[112],
    "12 (today, sun-synchronous)": cfg.CONSTELLATIONS[12],
    "30 (planned, sun-synchronous)": cfg.CONSTELLATIONS[30],
    "30 (65 deg Walker delta)": cfg.Constellation("delta-30", 3, 10, inclination_deg=65.0, raan_spread_deg=360.0),
    "60 (sun-synchronous)": cfg.CONSTELLATIONS[60],
}
preset = st.sidebar.selectbox("Constellation", [*PRESETS, "Custom"], index=0)
base = PRESETS.get(preset, cfg.CONSTELLATIONS[112])
with st.sidebar.expander("Orbit parameters", expanded=preset == "Custom"):
    planes = st.number_input("Planes", 1, 16, base.planes)
    per_plane = st.number_input("Satellites per plane", 1, 30, base.sats_per_plane)
    alt = st.slider("Altitude (km)", 400, 1200, int(base.altitude_km), 25)
    inc = st.slider("Inclination (deg)", 45.0, 100.0, base.inclination_deg, 0.1,
                    help="97.6 = sun-synchronous (OQ today). 60-70 = Walker delta service shell from the research pack.")
    pattern = st.radio("Plane spacing", ["Walker star (180 deg)", "Walker delta (360 deg)"],
                       index=int(base.raan_spread_deg > 180), horizontal=True)
    phasing = st.number_input("Phasing F", 0, 20, base.phasing)
    cross_isl = st.radio("Cross-plane ISL", ["optical", "rf"], index=int(base.cross_isl == "rf"), horizontal=True)
    optical_every = st.number_input("Cross-plane ISL on every Nth satellite", 1, 10, base.optical_every)
    link_seam = st.checkbox("Link last plane back to first (seam)", base.link_seam)
const = cfg.Constellation(f"{planes}x{per_plane}", int(planes), int(per_plane), float(alt), float(inc),
                          raan_spread_deg=180.0 if pattern.startswith("Walker star") else 360.0,
                          phasing=int(phasing), optical_every=int(optical_every), cross_isl=cross_isl,
                          link_seam=link_seam)

compare = st.sidebar.toggle("Compare all three payload modes", value=True)
mode = st.sidebar.radio("Payload mode", cfg.MODES, index=2, format_func=cfg.MODE_LABELS.get, disabled=compare)
blocked = st.sidebar.multiselect("Gateways offline / not authorised", [g.name for g in cfg.GATEWAYS])
load = st.sidebar.slider("Traffic load (x baseline)", 0.5, 20.0, 1.0, 0.5)
terminals = st.sidebar.slider("Offshore terminals", 50, 1000, 300, 50)
hours = st.sidebar.slider("Simulated hours", 2, 48, 12)
step = st.sidebar.select_slider("Time step (s)", [5, 10, 20, 30, 60], 10)
seed = st.sidebar.number_input("Random seed", 0, 9999, 7)

modes = list(cfg.MODES) if compare else [mode]
scenarios = {m: cfg.Scenario(const, m, frozenset(blocked), load, terminals, hours * 3600, float(step), int(seed))
             for m in modes}


@st.cache_data(show_spinner=False, max_entries=24)
def simulate(sc: cfg.Scenario):
    r = Simulation(sc).run()
    return r.summary(), r.by_class(), r.records, r.series, r.dropped


results = {}
bar = st.progress(0.0, "Simulating...")
for k, (m, sc) in enumerate(scenarios.items()):
    results[m] = simulate(sc)
    bar.progress((k + 1) / len(scenarios), f"Simulated {cfg.MODE_LABELS[m]}")
bar.empty()

# --- header + KPIs ----------------------------------------------------------------------
st.title("Every signal, the right path.")
st.caption(f"{const.size} satellites ({planes} planes x {per_plane}) at {alt} km, {inc} deg - "
           f"{terminals} offshore terminals - {hours} h - load x{load:g}"
           + (f" - offline: {', '.join(blocked)}" if blocked else ""))

focus = "regen_isl" if "regen_isl" in results else modes[0]
s = results[focus][0]
st.subheader(cfg.MODE_LABELS[focus])
c = st.columns(6)
c[0].metric("Delivered", f"{s['delivery_ratio']:.1%}", f"{s['dropped']} dropped, {s['pending']} pending", delta_color="off")
def fmt_latency(v):
    if not np.isfinite(v):
        return "n/a"
    return f"{v * 1e3:.0f} ms" if v < 1 else f"{v:.0f} s" if v < 120 else f"{v / 60:.1f} min"


c[1].metric("Critical p50 latency", fmt_latency(s["critical_p50_s"]))
c[2].metric("Critical < 250 ms", f"{s['critical_within_250ms']:.0%}")
c[3].metric("All traffic <= 90 min", f"{s['all_within_90min']:.1%}")
c[4].metric("Longest coverage gap", f"{s['max_gap_min']:.0f} min", f"basin covered {s['basin_coverage']:.0%} of time",
            delta_color="off")
c[5].metric("Routing compliant", f"{s['routing_compliance']:.0%}",
            f"policy re-routed {s['policy_redirects']:.0%}", delta_color="off")

if compare:
    rows = []
    for m in modes:
        x = results[m][0]
        rows.append({"Mode": cfg.MODE_LABELS[m], "Delivered": x["delivery_ratio"],
                     "Critical p50 (s)": x["critical_p50_s"], "Critical p95 (s)": x["critical_p95_s"],
                     "Critical < 250 ms": x["critical_within_250ms"], "All <= 90 min": x["all_within_90min"],
                     "Max onboard queue (kB)": x["max_onboard_queue_kb"], "Compliant": x["routing_compliance"]})
    st.dataframe(pd.DataFrame(rows).style.format({
        "Delivered": "{:.1%}", "Critical < 250 ms": "{:.0%}", "All <= 90 min": "{:.1%}", "Compliant": "{:.0%}",
        "Critical p50 (s)": "{:.3g}", "Critical p95 (s)": "{:.3g}", "Max onboard queue (kB)": "{:,.0f}"}),
        hide_index=True, width="stretch")

tab_lat, tab_net, tab_q, tab_pol, tab_data = st.tabs(["Latency", "Network map", "Queues & coverage", "Policy", "Data"])

# --- latency ----------------------------------------------------------------------------
with tab_lat:
    def cdf(series: pd.Series):
        v = np.sort(series.values)
        return v, np.arange(1, len(v) + 1) / len(v)

    left, right = st.columns(2)
    fig = go.Figure()
    for m in modes:
        rec = results[m][2]
        crit = rec[rec.cls == "critical"].latency_s if len(rec) else pd.Series(dtype=float)
        if len(crit):
            x, y = cdf(crit)
            fig.add_scatter(x=x, y=y, name=cfg.MODE_LABELS[m], mode="lines", line=dict(color=MODE_COLOR[m], width=2),
                            hovertemplate="%{y:.0%} delivered within %{x:.3g} s")
    for xv, label in ((0.15, "150 ms"), (0.25, "250 ms"), (5400, "90 min")):
        fig.add_vline(x=xv, line=dict(color=MUTED, width=1, dash="dot"), annotation_text=label,
                      annotation_font_color=MUTED)
    style(fig, title="Critical alarms: share delivered within latency", xaxis_type="log",
          xaxis_title="End-to-end latency (s, log scale)", yaxis_title="Share delivered", yaxis_tickformat=".0%")
    left.plotly_chart(fig, width="stretch")

    rec = results[focus][2]
    fig = go.Figure()
    for cl in ("critical", "metadata", "regular"):
        sub = rec[rec.cls == cl].latency_s if len(rec) else pd.Series(dtype=float)
        if len(sub):
            x, y = cdf(sub)
            fig.add_scatter(x=x, y=y, name=cl, mode="lines", line=dict(color=CLASS_COLOR[cl], width=2),
                            hovertemplate="%{y:.0%} within %{x:.3g} s")
    fig.add_vline(x=5400, line=dict(color=MUTED, width=1, dash="dot"), annotation_text="90 min",
                  annotation_font_color=MUTED)
    style(fig, title=f"All classes: {cfg.MODE_LABELS[focus]}", xaxis_type="log",
          xaxis_title="End-to-end latency (s, log scale)", yaxis_title="Share delivered", yaxis_tickformat=".0%")
    right.plotly_chart(fig, width="stretch")

    if len(rec):
        live = rec[rec.wait_terminal_s + rec.wait_onboard_s == 0]
        if len(live):
            st.markdown("**Where the milliseconds go**: messages delivered in the same pass, by path")
            g = live.groupby("path").network_s.describe(percentiles=[.5, .95])[["count", "50%", "95%"]]
            st.dataframe((g.assign(**{"50%": g["50%"] * 1e3, "95%": g["95%"] * 1e3})
                          .rename(columns={"50%": "p50 (ms)", "95%": "p95 (ms)"})).style.format("{:.0f}"),
                         width="stretch")
        st.markdown("**By offshore sector**")
        st.dataframe(rec.groupby("sector").latency_s.agg(
            delivered="count", p50_s="median", p95_s=lambda v: v.quantile(.95),
            within_250ms=lambda v: (v < .25).mean()).style.format(
            {"p50_s": "{:.3g}", "p95_s": "{:.3g}", "within_250ms": "{:.0%}"}), width="stretch")

# --- map ----------------------------------------------------------------------------------
with tab_net:
    sc = scenarios[focus]
    t_map = st.slider("Time (minutes into simulation)", 0, hours * 60, 0, 1)
    sim = Simulation(sc)
    snap = sim.snapshot(t_map * 60.0)
    fig = go.Figure()
    cross_label = f"{'RF' if sc.constellation.cross_isl == 'rf' else 'Optical'} ISL (cross-plane)"
    for in_plane, color, dash, label in ((True, SLOT[0], "solid", "RF ISL (intra-plane)"),
                                         (False, SLOT[1], "dash", cross_label)):
        lats, lons = [], []
        for i, j, km, k in snap["isl"]:
            if (snap["plane"][i] == snap["plane"][j]) == in_plane:
                lats += [snap["sat_lat"][i], snap["sat_lat"][j], None]
                lons += [snap["sat_lon"][i], snap["sat_lon"][j], None]
        if lats:
            fig.add_scattergeo(lat=lats, lon=lons, mode="lines", name=label, line=dict(color=color, width=2, dash=dash),
                               hoverinfo="skip")
    lats, lons = [], []
    for g, sat in snap["feeders"]:
        lats += [cfg.GATEWAYS[g].lat, snap["sat_lat"][sat], None]
        lons += [cfg.GATEWAYS[g].lon, snap["sat_lon"][sat], None]
    if lats:
        fig.add_scattergeo(lat=lats, lon=lons, mode="lines", name="Feeder link", line=dict(color=MUTED, width=1),
                           hoverinfo="skip")
    fig.add_scattergeo(lat=sim.term_lat, lon=sim.term_lon, mode="markers", name="Terminals",
                       marker=dict(size=4, color="#6B6B73"), text=sim.term_sector, hovertemplate="%{text} terminal")
    fig.add_scattergeo(lat=snap["sat_lat"], lon=snap["sat_lon"], mode="markers", name="Satellites (gNB onboard)",
                       marker=dict(size=10, color=TEXT, symbol=np.where(snap["optical"], "star", "circle"),
                                   line=dict(color=SURFACE, width=2)),
                       text=[f"Sat {k} - plane {p}{' - cross-plane ISL' if o else ''}"
                             for k, (p, o) in enumerate(zip(snap["plane"], snap["optical"]))],
                       hovertemplate="%{text}<extra></extra>")
    open_gw = [g for g in cfg.GATEWAYS if g.name not in sc.blocked_gateways]
    shut_gw = [g for g in cfg.GATEWAYS if g.name in sc.blocked_gateways]
    fig.add_scattergeo(lat=[g.lat for g in open_gw], lon=[g.lon for g in open_gw], mode="markers+text",
                       name="Gateway", text=[f"{g.name} ({g.country})" for g in open_gw], textposition="top center",
                       textfont=dict(color=TEXT, size=11), marker=dict(size=11, color=OK, symbol="square"))
    if shut_gw:
        fig.add_scattergeo(lat=[g.lat for g in shut_gw], lon=[g.lon for g in shut_gw], mode="markers+text",
                           name="Gateway offline", text=[f"{g.name}: offline" for g in shut_gw],
                           textposition="bottom center", textfont=dict(color=ALERT, size=11),
                           marker=dict(size=12, color=ALERT, symbol="x"))
    fig.update_geos(projection_type="orthographic", projection_rotation=dict(lat=50, lon=0),
                    showland=True, landcolor="#2F2F37", showocean=True, oceancolor=BG, showcountries=True,
                    countrycolor="#353535", coastlinecolor="#6B6B73", bgcolor=SURFACE, lataxis_showgrid=True,
                    lonaxis_showgrid=True, lataxis_gridcolor=GRID, lonaxis_gridcolor=GRID)
    style(fig, height=640, title=f"t = {t_map} min: {len(snap['isl'])} ISLs, {len(snap['feeders'])} feeder links",
          hovermode="closest")
    st.plotly_chart(fig, width="stretch")
    st.caption("Stars carry a cross-plane ISL terminal. Drag the globe to rotate.")

# --- queues & coverage ------------------------------------------------------------------
with tab_q:
    def series_chart(col, title, ytitle, shape="linear"):
        fig = go.Figure()
        for m in modes:
            ts = results[m][3]
            fig.add_scatter(x=ts.t / 3600, y=ts[col], name=cfg.MODE_LABELS[m], mode="lines",
                            line=dict(color=MODE_COLOR[m], width=2, shape=shape))
        return style(fig, height=280, title=title, xaxis_title="Hours", yaxis_title=ytitle)

    st.plotly_chart(series_chart("onboard_queue_kb", "Onboard store-and-forward queue", "kB"),
                    width="stretch")
    st.plotly_chart(series_chart("terminal_queue_msgs", "Messages waiting on terminals", "messages"),
                    width="stretch")
    ts = results[focus][3]
    fig = go.Figure(go.Scatter(x=ts.t / 3600, y=ts.sats_over_basin, mode="lines", line=dict(color=SLOT[0], width=2, shape="hv"),
                               name="Satellites in view"))
    st.plotly_chart(style(fig, height=240, title="Satellites in view of the North Sea basin (57N 3E, 10 deg mask)",
                          xaxis_title="Hours", yaxis_title="satellites", showlegend=False), width="stretch")
    st.caption(f"Handovers: {s['handovers_per_terminal_day']:.1f} per terminal per day. "
               f"Mean coverage gap {s['mean_gap_min']:.1f} min.")

# --- policy -------------------------------------------------------------------------------
with tab_pol:
    rec = results[focus][2]
    st.markdown("Every flow is routed only to a gateway its jurisdiction allows "
                "(`UK` to UK, `NO` to Norway, `EEA` to EEA, international waters to any). "
                "*Policy re-routed* = the latency-optimal gateway was not allowed, so the engine chose another.")
    if len(rec):
        mix = pd.crosstab(rec.jurisdiction, rec.gateway, normalize="index")
        fig = go.Figure(go.Heatmap(z=mix.values, x=mix.columns, y=mix.index, colorscale=[[0, SURFACE], [1, SLOT[0]]],
                                   zmin=0, zmax=1, text=np.vectorize(lambda v: f"{v:.0%}" if v else "")(mix.values),
                                   texttemplate="%{text}", hovertemplate="%{y} -> %{x}: %{z:.0%}<extra></extra>",
                                   xgap=2, ygap=2, colorbar=dict(title="share", tickformat=".0%")))
        st.plotly_chart(style(fig, height=320, title="Where each jurisdiction's traffic lands", hovermode="closest"),
                        width="stretch")
        st.dataframe(rec.groupby("jurisdiction").agg(
            delivered=("id", "count"), compliant=("compliant", "mean"), policy_rerouted=("policy_redirect", "mean"),
            via_isl=("isl_hops", lambda v: (v > 0).mean())).style.format(
            {"compliant": "{:.0%}", "policy_rerouted": "{:.0%}", "via_isl": "{:.0%}"}), width="stretch")

# --- data -----------------------------------------------------------------------------------
with tab_data:
    for m in modes:
        st.markdown(f"**{cfg.MODE_LABELS[m]}**: by traffic class")
        st.dataframe(results[m][1], hide_index=True, width="stretch")
    rec = results[focus][2]
    st.download_button("Download message log (CSV)", rec.to_csv(index=False), f"ntnpulse_{focus}_messages.csv")
