import re, sys

P = "/home/user/yudaant/app.py"
src = open(P, encoding="utf-8").read()
orig_len = len(src)

# ── 1) global plotly template right after imports ──────────────────────────
anchor = "import plotly.graph_objects as go\n"
assert src.count(anchor) == 1, "plotly import anchor not unique"
ins = anchor + """import plotly.io as pio
"""
src = src.replace(anchor, ins, 1)

anchor2 = "import streamlit as st\n"
assert src.count(anchor2) == 1, "streamlit import anchor not unique"
tpl = anchor2 + '''

# ── global plotly theme ("yudaant") ── every fig inherits it unless it
# explicitly overrides an attribute. Presentation only; engine untouched.
_PLOTLY_FONT = "'Inter','Segoe UI',system-ui,sans-serif"
_yu_tmpl = go.layout.Template()
_yu_tmpl.layout = {
    "font": {"family": _PLOTLY_FONT, "size": 12, "color": "#b9c7de"},
    "title": {"font": {"family": _PLOTLY_FONT, "size": 16, "color": "#dbe6fb"}},
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "colorway": ["#2dd4bf", "#818cf8", "#f5b23c", "#f87171",
                 "#60a5fa", "#c084fc", "#34d399", "#fb923c"],
    "xaxis": {"gridcolor": "rgba(148,163,184,.12)", "zeroline": False,
              "linecolor": "rgba(148,163,184,.25)", "ticks": "",
              "title": {"font": {"color": "#8ea0bd", "size": 12}}},
    "yaxis": {"gridcolor": "rgba(148,163,184,.12)", "zeroline": False,
              "linecolor": "rgba(148,163,184,.25)", "ticks": "",
              "title": {"font": {"color": "#8ea0bd", "size": 12}}},
    "legend": {"orientation": "h", "yanchor": "bottom", "y": 1.02,
               "xanchor": "left", "x": 0,
               "font": {"size": 11, "color": "#9fb3d1"}},
    "margin": {"l": 42, "r": 18, "t": 48, "b": 36},
    "hoverlabel": {"bgcolor": "#0e1930", "bordercolor": "#2dd4bf",
                   "font": {"color": "#eaf1fb", "size": 12, "family": _PLOTLY_FONT}},
}
pio.templates["yudaant"] = _yu_tmpl
pio.templates.default = "yudaant"
'''
src = src.replace(anchor2, tpl, 1)

# ── 2) full CSS skin replacement ──────────────────────────────────────────
NEW_CSS = '''CSS = """
<style>
/* ──────────────────────────────────────────────────────────────────────
   YUDAANT · "AURUM FX" skin — aurora background, glass cards, motion.
   Pure presentational CSS; embedded, zero external resources. No rule
   here changes what the engine computes or what the numbers mean.
   ────────────────────────────────────────────────────────────────────── */
#MainMenu, footer {visibility:hidden;}
[data-testid="stToolbar"] {visibility:hidden;}
[data-testid="stHeader"] {background:transparent;}
.block-container {padding-top:2.4rem; padding-bottom:3.4rem; max-width:1560px; position:relative; z-index:1;}
html, body, [class*="css"] {font-family:'Inter','Segoe UI Variable Display','Segoe UI',system-ui,sans-serif;}
html, body, [data-testid="stAppViewContainer"] {background-color:#070c16;}
::selection {background:rgba(45,212,191,.32); color:#f4fbff;}
::-webkit-scrollbar {width:10px; height:10px;}
::-webkit-scrollbar-track {background:transparent;}
::-webkit-scrollbar-thumb {background:#1c2b47; border-radius:10px; border:2px solid transparent; background-clip:content-box;}
::-webkit-scrollbar-thumb:hover {background:rgba(45,212,191,.45); background-clip:content-box;}

/* ── aurora orbs drifting behind everything ── */
.stApp {background:
  radial-gradient(1400px 800px at 18% -12%, rgba(45,212,191,.09), transparent 55%),
  radial-gradient(1200px 700px at 86% -4%, rgba(129,140,248,.11), transparent 55%),
  linear-gradient(180deg, #0a1122 0%, #070c16 48%, #05080f 100%);}
.stApp::before, .stApp::after {content:""; position:fixed; border-radius:50%; pointer-events:none; z-index:0;
  filter:blur(90px); opacity:.5;}
.stApp::before {width:46vw; height:46vw; left:-12vw; top:32vh;
  background:radial-gradient(circle, rgba(20,184,166,.17), transparent 65%);
  animation:yuDriftA 36s ease-in-out infinite alternate;}
.stApp::after {width:52vw; height:52vw; right:-16vw; top:-10vh;
  background:radial-gradient(circle, rgba(99,102,241,.18), transparent 65%);
  animation:yuDriftB 46s ease-in-out infinite alternate;}
[data-testid="stAppViewContainer"]::before {content:""; position:fixed; inset:0; z-index:0; pointer-events:none;
  background-image:linear-gradient(rgba(148,163,184,.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148,163,184,.05) 1px, transparent 1px);
  background-size:44px 44px;
  -webkit-mask-image:radial-gradient(90% 62% at 50% 0%, #000 26%, transparent 88%);
  mask-image:radial-gradient(90% 62% at 50% 0%, #000 26%, transparent 88%);}
@keyframes yuDriftA {from {transform:translate3d(0,0,0) scale(1);} to {transform:translate3d(9vw,-13vh,0) scale(1.16);}}
@keyframes yuDriftB {from {transform:translate3d(0,0,0) scale(1.06);} to {transform:translate3d(-8vw,10vh,0) scale(.92);}}

/* ── hero ── */
.yu-hero {position:relative; overflow:hidden;
  background:
    radial-gradient(1100px 320px at 12% -80px, rgba(45,212,191,.16), transparent 60%),
    radial-gradient(760px 280px at 92% -70px, rgba(129,140,248,.15), transparent 60%),
    linear-gradient(160deg, rgba(19,30,54,.86), rgba(11,18,32,.78));
  backdrop-filter:blur(10px);
  border:1px solid rgba(45,212,191,.26); border-radius:20px; padding:28px 32px 22px 32px; margin-bottom:16px;
  box-shadow:0 24px 70px rgba(2,6,16,.55), inset 0 1px 0 rgba(255,255,255,.05);
  animation:yuFadeUp .7s cubic-bezier(.2,.7,.2,1) both;}
.yu-hero::after {content:""; position:absolute; top:-120%; left:-45%; width:36%; height:340%; transform:rotate(14deg);
  background:linear-gradient(100deg, transparent, rgba(255,255,255,.06), transparent);
  animation:yuSheen 8s ease-in-out infinite;}
@keyframes yuSheen {0%,56% {left:-45%;} 80% {left:125%;} 100% {left:125%;}}
.yu-title {font-size:37px; font-weight:800; color:#f2f6fd; margin:0; letter-spacing:.06em; line-height:1.12;
  text-shadow:0 2px 26px rgba(45,212,191,.22);}
.yu-title .accent {font-weight:900; background:linear-gradient(92deg,#5eead4,#2dd4bf 38%,#a5b4fc 72%,#5eead4);
  background-size:220% 100%; -webkit-background-clip:text; background-clip:text;
  -webkit-text-fill-color:transparent; color:transparent; text-shadow:none; animation:yuTitle 6.5s linear infinite;}
@keyframes yuTitle {from {background-position:0% 50%;} to {background-position:220% 50%;}}
.yu-sub {color:#93a6c8; font-size:14.5px; margin:8px 0 12px 0; max-width:940px; line-height:1.6;}

/* ── glass cards + KPIs ── */
.yu-card {position:relative; overflow:hidden; transition:transform .22s ease, box-shadow .22s ease, border-color .22s ease;
  background:linear-gradient(175deg, rgba(18,28,50,.88), rgba(12,20,37,.82));
  border:1px solid rgba(148,163,184,.16); border-radius:14px; padding:11px 14px; height:100%;
  backdrop-filter:blur(7px);}
.yu-card:hover {transform:translateY(-2px); border-color:rgba(45,212,191,.4);
  box-shadow:0 14px 36px rgba(2,6,16,.5), 0 0 24px rgba(45,212,191,.10);}
.yu-card::after {content:""; position:absolute; inset:0; opacity:0; transition:opacity .3s; pointer-events:none;
  background:radial-gradient(190px 90px at 18% 0%, rgba(255,255,255,.07), transparent 70%);}
.yu-card:hover::after {opacity:1;}
.yu-kpi-label {font-size:10.5px; letter-spacing:.13em; text-transform:uppercase; color:#7c8db0; font-weight:700;}
.yu-kpi-value {font-size:25px; font-weight:800; color:#eaf1fb; line-height:1.3;
  font-variant-numeric:tabular-nums; text-shadow:0 0 24px rgba(45,212,191,.14);}
.yu-kpi-sub {font-size:11px; color:#7c8db0; line-height:1.4;}
div[data-testid="stMetric"] {background:linear-gradient(175deg, rgba(17,27,49,.82), rgba(11,18,32,.76));
  border:1px solid rgba(148,163,184,.15); border-radius:14px; padding:12px 15px; backdrop-filter:blur(6px);
  transition:transform .2s ease, border-color .2s ease;}
div[data-testid="stMetric"]:hover {transform:translateY(-2px); border-color:rgba(45,212,191,.35);}
div[data-testid="stMetric"] label {color:#7c8db0; font-weight:700; letter-spacing:.12em; text-transform:uppercase; font-size:10.5px;}
div[data-testid="stMetricValue"] {color:#eaf1fb; font-weight:800;}

/* ── feed, notes, findings ── */
.yu-feed {max-height:430px; overflow-y:auto; padding-right:6px; font-size:12.8px;}
.yu-feed .row {padding:5.5px 9px; border-bottom:1px dashed rgba(148,163,184,.14); color:#c3d0e6; line-height:1.4;
  transition:background .14s ease;}
.yu-feed .row:hover {background:rgba(45,212,191,.05); border-radius:8px;}
.yu-feed .row .t {color:#5c6f92; font-variant-numeric:tabular-nums; margin-right:8px;}
.yu-feed::-webkit-scrollbar {width:8px;}
.yu-feed::-webkit-scrollbar-thumb {background:#243250; border-radius:8px;}
.yu-note {background:rgba(245,178,60,.07); border:1px solid rgba(245,178,60,.35); border-radius:12px;
  padding:12px 16px; color:#e7c98a; font-size:13.5px; line-height:1.55; backdrop-filter:blur(4px);}
.yu-danger {background:rgba(248,113,113,.07); border:1px solid rgba(248,113,113,.4); border-radius:12px;
  padding:12px 16px; color:#f3b1b1; font-size:13.5px; line-height:1.55; backdrop-filter:blur(4px);}
.yu-ok {background:rgba(52,211,153,.07); border:1px solid rgba(52,211,153,.35); border-radius:12px;
  padding:12px 16px; color:#a9e8cf; font-size:13.5px; line-height:1.55; backdrop-filter:blur(4px);}
.yu-find {background:linear-gradient(180deg, rgba(13,21,38,.8), rgba(10,16,30,.72)); border:1px solid rgba(148,163,184,.15);
  border-left:4px solid #94a3b8; border-radius:12px; padding:13px 16px; margin-bottom:10px;
  box-shadow:0 6px 22px rgba(2,6,16,.3); transition:transform .2s ease, box-shadow .2s ease;}
.yu-find:hover {transform:translateY(-1px); box-shadow:0 10px 28px rgba(2,6,16,.42);}
.yu-find.high {border-left-color:#f87171;} .yu-find.medium {border-left-color:#f5b23c;}
.yu-find.low {border-left-color:#60a5fa;} .yu-find.info {border-left-color:#94a3b8;}
.yu-find h4 {margin:0 0 4px 0; color:#e7eefb; font-size:15px;}
.yu-find .obs {color:#b9c7de; font-size:12.8px; line-height:1.5;}
.yu-find .read {color:#e7c98a; font-size:12px; font-style:italic; margin-top:6px; line-height:1.45;}
.yu-chiprow {margin:2px 0 12px 0; display:flex; gap:8px; flex-wrap:wrap; align-items:center;}

/* ── tabs: floating glass pill bar ── */
.stTabs [data-baseweb="tab-list"] {gap:3px; width:fit-content; max-width:100%;
  background:rgba(10,17,31,.66); border:1px solid rgba(148,163,184,.14); border-radius:14px; padding:5px;
  backdrop-filter:blur(10px); box-shadow:0 10px 30px rgba(2,6,16,.35);}
.stTabs [data-baseweb="tab"] {border:none; border-radius:10px; padding:6px 13px; color:#8ea0bd;
  font-weight:650; font-size:13.5px; letter-spacing:.02em; transition:color .16s ease, background .16s ease;}
.stTabs [data-baseweb="tab"]:hover {color:#cfe0fb; background:rgba(148,163,184,.08);}
.stTabs [data-baseweb="tab"][aria-selected="true"] {color:#a7f3eb !important;
  background:linear-gradient(160deg,#155e55,#173a63) !important;
  box-shadow:0 4px 18px rgba(45,212,191,.28), inset 0 1px 0 rgba(255,255,255,.14);}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display:none;}

/* ── sidebar ── */
div[data-testid="stSidebar"] {background:linear-gradient(195deg, rgba(12,20,38,.97), rgba(7,12,22,.99));
  border-right:1px solid rgba(45,212,191,.14); box-shadow:14px 0 60px rgba(2,6,16,.5);}
div[data-testid="stSidebar"] .yu-side-title {font-size:13px; font-weight:800; letter-spacing:.12em;
  color:#dbe6fb; text-transform:uppercase;}

/* ── widgets ── */
.stTextInput input, .stNumberInput input, .stTextArea textarea {
  background:rgba(8,14,26,.82) !important; border-color:#223252 !important; color:#d7e3f8 !important;
  border-radius:10px; transition:border-color .16s ease, box-shadow .16s ease;}
.stTextInput:focus-within input, .stNumberInput:focus-within input {border-color:#2dd4bf !important;
  box-shadow:0 0 0 2px rgba(45,212,191,.16);}
[data-baseweb="select"] > div {background:rgba(8,14,26,.82); border:1px solid #223252; border-radius:10px;
  color:#c9d7ee; transition:border-color .16s ease;}
[data-baseweb="select"] > div:hover {border-color:rgba(45,212,191,.5);}
.stRadio p, .stCheckbox span, .stSlider [data-baseweb="label"], [data-testid="stWidgetLabel"] p {color:#b9c7de;}
.stCaption, .stCaption * {color:#8ea0bd;}
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
  border-radius:12px; border:1px solid rgba(148,163,184,.2); color:#c9d7ee; font-weight:650; letter-spacing:.03em;
  background:linear-gradient(170deg, rgba(17,27,49,.92), rgba(11,18,32,.92));
  transition:transform .16s ease, box-shadow .16s ease, border-color .16s ease, color .16s ease;}
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
  transform:translateY(-1px); color:#eaf4ff; border-color:rgba(45,212,191,.55);
  box-shadow:0 8px 26px rgba(2,6,16,.5), 0 0 18px rgba(45,212,191,.14);}
.stButton > button:active, .stDownloadButton > button:active {transform:translateY(0);}
button[kind="primary"] {background:linear-gradient(160deg,#0d9488,#115e59 55%,#0e7490) !important;
  border:1px solid #2dd4bf !important; color:#eafffb !important; font-weight:800; letter-spacing:.04em;
  animation:yuPulse 3.4s ease-in-out infinite;}
button[kind="primary"]:hover {filter:brightness(1.13); box-shadow:0 8px 32px rgba(45,212,191,.4);}
@keyframes yuPulse {0%,100% {box-shadow:0 5px 22px rgba(45,212,191,.24);}
  50% {box-shadow:0 5px 30px rgba(45,212,191,.5), 0 0 44px rgba(45,212,191,.18);}}

/* ── progress ── */
progress {width:100%; height:8px; accent-color:#2dd4bf; border-radius:999px; overflow:hidden;}
progress::-webkit-progress-bar {background:rgba(148,163,184,.12); border-radius:999px;}
progress::-webkit-progress-value {background:linear-gradient(90deg,#0d9488,#2dd4bf 55%,#818cf8);
  border-radius:999px; box-shadow:0 0 18px rgba(45,212,191,.5); transition:width .25s ease;}
[data-testid="stProgress"] > div > div {border-radius:999px;}

/* ── tables / charts / expanders / alerts ── */
div[data-testid="stDataFrame"] {border:1px solid rgba(148,163,184,.15); border-radius:14px; overflow:hidden;}
div[data-testid="stPlotlyChart"] {animation:yuFadeUp .55s ease both; border-radius:14px;}
div[data-testid="stExpander"] details {background:rgba(11,18,32,.62); border:1px solid rgba(148,163,184,.14);
  border-radius:14px; backdrop-filter:blur(5px); transition:border-color .2s ease;}
div[data-testid="stExpander"] details:hover {border-color:rgba(45,212,191,.32);}
div[data-testid="stAlert"] {border-radius:14px; backdrop-filter:blur(5px);}

code, .stMarkdown code {background:#0e1930; border:1px solid #1e2c49; padding:1px 6px; border-radius:6px;
  color:#9fe8dc; font-size:.86em;}

.empty-state {border:1.5px dashed #2f4468; border-radius:18px; padding:42px 30px; text-align:center; color:#8ea0bd;
  background:radial-gradient(700px 220px at 50% 0%, rgba(45,212,191,.08), transparent 70%); margin-top:8px;
  animation:yuFadeUp .7s ease both;}
.empty-state h3 {color:#cfe0fb; margin-top:8px;}

@keyframes yuFadeUp {from {opacity:0; transform:translateY(10px);} to {opacity:1; transform:none;}}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {animation-duration:.01ms !important; animation-iteration-count:1 !important;
    transition-duration:.01ms !important;}}
</style>
"""'''

pat = re.compile(r'CSS = """.*?"""', re.DOTALL)
m = pat.search(src)
assert m, "CSS block not found"
assert len(pat.findall(src)) == 1, "multiple CSS blocks"
src = src[:m.start()] + NEW_CSS + src[m.end():]

open(P, "w", encoding="utf-8").write(src)
print(f"OK: {orig_len} -> {len(src)} bytes")

import py_compile
py_compile.compile(P, doraise=True)
print("py_compile: clean")
