import py_compile

P = "/home/user/yudaant/app.py"
s = open(P, encoding="utf-8").read()
n0 = len(s)

# ══ 1) STARK CSS appended inside the <style> block ════════════════════════
HUD = '''
/* ═══ STARK PROTOCOL · Mark-L HUD skin — cyan arc-core, chamfered glass, scanlines ═══ */
:root {
  --stk-cyan:#61e7ff; --stk-gold:#ffcf6b; --stk-line:rgba(97,231,255,.26);
  --stk-bg:#03080f; --mono:ui-monospace,'Cascadia Mono','Consolas','SF Mono',Menlo,monospace;}
html, body, [data-testid="stAppViewContainer"] {background-color:var(--stk-bg);}
.stApp {background:
  radial-gradient(1600px 900px at 50% -30%, rgba(97,231,255,.09), transparent 60%),
  radial-gradient(1200px 800px at 88% 110%, rgba(255,207,107,.05), transparent 55%),
  linear-gradient(180deg, #040a14 0%, #03080f 52%, #01050b 100%);}
.stApp::before {background:radial-gradient(circle, rgba(97,231,255,.14), transparent 65%);}
.stApp::after {background:radial-gradient(circle, rgba(255,207,107,.09), transparent 65%);}
[data-testid="stAppViewContainer"]::before {background-image:
  linear-gradient(rgba(97,231,255,.05) 1px, transparent 1px),
  linear-gradient(90deg, rgba(97,231,255,.05) 1px, transparent 1px);background-size:40px 40px;}
[data-testid="stAppViewContainer"]::after {content:"";position:fixed;inset:0;pointer-events:none;
  background:linear-gradient(180deg,transparent 44%,rgba(97,231,255,.05) 48%,rgba(97,231,255,.14) 50%,rgba(97,231,255,.05) 52%,transparent 56%);
  animation:stkScan 8s linear infinite;}
@keyframes stkScan {from {transform:translateY(-110%);} to {transform:translateY(110%);}}
.stk-frame {position:fixed;inset:8px;height:calc(100vh - 16px);z-index:4;pointer-events:none;opacity:.55;}
.stk-frame span {position:absolute;width:26px;height:26px;border:0 solid var(--stk-cyan);}
.stk-frame .c1 {top:0;left:0;border-top-width:2px;border-left-width:2px;}
.stk-frame .c2 {top:0;right:0;border-top-width:2px;border-right-width:2px;}
.stk-frame .c3 {bottom:0;left:0;border-bottom-width:2px;border-left-width:2px;}
.stk-frame .c4 {bottom:0;right:0;border-bottom-width:2px;border-right-width:2px;}
.stk-frame .t1,.stk-frame .t2 {top:0;border-top-width:1px;left:60px;right:60px;width:auto;height:0;opacity:.5;}
.stk-frame .t2 {top:auto;bottom:0;border-top:0;border-bottom-width:1px;}

/* hero → arc core console */
.stk-hero {display:flex;gap:28px;align-items:center;border-radius:2px;
  border:1px solid rgba(97,231,255,.4) !important;
  background:linear-gradient(150deg,rgba(6,17,30,.94),rgba(2,8,15,.9)) !important;
  box-shadow:0 0 60px rgba(97,231,255,.12), inset 0 0 40px rgba(97,231,255,.05) !important;}
.stk-hero > div:last-child {flex:1 1 auto;}
.stk-reactor {position:relative;width:126px;height:126px;flex:0 0 auto;border-radius:50%;
  background:radial-gradient(circle,rgba(97,231,255,.26),rgba(97,231,255,.04) 55%,transparent 72%);}
.stk-reactor i {position:absolute;border-radius:50%;}
.stk-reactor i:nth-of-type(1) {inset:6px;border:1.5px solid rgba(97,231,255,.5);
  border-top-color:transparent;border-bottom-color:transparent;animation:stkSpin 3.4s linear infinite;}
.stk-reactor i:nth-of-type(2) {inset:17px;border:1px solid rgba(97,231,255,.4);
  border-left-color:transparent;border-right-color:transparent;animation:stkSpin 2.1s linear infinite reverse;}
.stk-reactor i:nth-of-type(3) {inset:27px;border:1px dashed rgba(97,231,255,.3);animation:stkSpin 6.5s linear infinite;}
.stk-reactor b {position:absolute;inset:40px;border-radius:50%;
  background:radial-gradient(circle,#e6fcff,rgba(97,231,255,.85) 38%,rgba(97,231,255,.14) 68%,transparent);
  animation:stkGlow 2.6s ease-in-out infinite;}
.stk-reactor u {position:absolute;inset:0 56px;border-top:1px solid rgba(97,231,255,.45);transform-origin:50% 50%;opacity:.5;}
.stk-reactor u:nth-of-type(1){transform:rotate(0deg);} .stk-reactor u:nth-of-type(2){transform:rotate(90deg);}
@keyframes stkSpin {to {transform:rotate(360deg);}}
@keyframes stkGlow {50% {filter:brightness(1.55);transform:scale(1.07);}}
.stk-hero .yu-title {font-family:var(--mono);font-size:31px;letter-spacing:.26em;color:#e4faff;
  text-shadow:0 0 20px rgba(97,231,255,.5);animation:stkBoot 5s steps(1) 1 both;}
.stk-hero .yu-title .accent {background:linear-gradient(92deg,#e4faff,#61e7ff 55%,#ffcf6b);
  background-size:200% 100%;-webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;animation:yuTitle 5.5s linear infinite;}
@keyframes stkBoot {0%{opacity:0}7%{opacity:1}9%{opacity:.15}11%{opacity:1}13%{opacity:.5}15%{opacity:1}}
.stk-hero .yu-sub {font-family:var(--mono);font-size:12.5px;letter-spacing:.06em;color:#7fb6cc;}
.stk-sys {font-family:var(--mono);font-size:10px;letter-spacing:.3em;color:var(--stk-cyan);opacity:.85;
  margin-top:6px;display:block;}
.stk-sys::after {content:"▮";animation:yuBlink 1.1s step-end infinite;margin-left:4px;}

/* panels → chamfered HUD glass */
.yu-card,div[data-testid="stMetric"],.yu-mega {border-radius:2px;
  clip-path:polygon(11px 0,100% 0,100% calc(100% - 11px),calc(100% - 11px) 100%,0 100%,0 11px);
  background:linear-gradient(165deg,rgba(7,18,32,.94),rgba(3,10,18,.9)) !important;
  border:1px solid var(--stk-line) !important;}
.yu-card:hover,div[data-testid="stMetric"]:hover,.yu-mega:hover {
  border-color:rgba(97,231,255,.6) !important;
  box-shadow:0 0 26px rgba(97,231,255,.2), inset 0 0 30px rgba(97,231,255,.06) !important;}
.yu-kpi-value,div[data-testid="stMetricValue"],.yu-mega .v {font-family:var(--mono);letter-spacing:.02em;
  color:#dff7ff;text-shadow:0 0 16px rgba(97,231,255,.4);}
.yu-kpi-label,div[data-testid="stMetric"] label,.yu-mega .l {font-family:var(--mono);color:#5f94ad !important;}
.yu-mega::before {background:radial-gradient(130px 62px at 50% -12px,rgba(97,231,255,.2),transparent 72%);}

/* tabs → segmented console bar */
.stTabs [data-baseweb="tab-list"] {background:rgba(3,10,18,.88);border:1px solid rgba(97,231,255,.22);
  border-radius:2px;padding:4px;}
.stTabs [data-baseweb="tab"] {font-family:var(--mono);font-size:11px;letter-spacing:.08em;
  text-transform:uppercase;border-radius:0;color:#6f93a8;padding:7px 12px;}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
  background:linear-gradient(180deg,rgba(97,231,255,.2),rgba(97,231,255,.05)) !important;
  color:var(--stk-cyan) !important;
  box-shadow:inset 0 -2px 0 var(--stk-cyan),0 0 18px rgba(97,231,255,.18) !important;}
.stTabs [data-baseweb="tab"]:hover {color:#b9ecfa;background:rgba(97,231,255,.05);}

/* buttons → HUD triggers */
.stButton > button,.stDownloadButton > button,[data-testid="stFormSubmitButton"] > button {
  font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;
  border-radius:2px;color:#a8dff0 !important;
  background:linear-gradient(180deg,rgba(97,231,255,.07),rgba(4,10,20,.85)) !important;
  border:1px solid rgba(97,231,255,.3) !important;}
.stButton > button:hover,.stDownloadButton > button:hover,[data-testid="stFormSubmitButton"] > button:hover {
  color:#e4faff !important;border-color:var(--stk-cyan) !important;
  box-shadow:0 0 20px rgba(97,231,255,.28), inset 0 0 14px rgba(97,231,255,.08) !important;}
button[kind="primary"] {background:linear-gradient(160deg,rgba(97,231,255,.2),rgba(4,22,32,.92)) !important;
  border:1px solid var(--stk-cyan) !important;color:#d9f7ff !important;
  text-shadow:0 0 12px rgba(97,231,255,.7);animation:stkPulse 2.8s ease-in-out infinite !important;}
@keyframes stkPulse {0%,100%{box-shadow:0 0 14px rgba(97,231,255,.25);}
  50%{box-shadow:0 0 34px rgba(97,231,255,.55), inset 0 0 22px rgba(97,231,255,.22);}}

/* inputs → console fields */
.stTextInput input,.stNumberInput input,.stTextArea textarea {font-family:var(--mono);border-radius:2px;
  background:rgba(2,7,14,.9) !important;border-color:rgba(97,231,255,.25) !important;color:#c9effc !important;}
.stTextInput:focus-within input,.stNumberInput:focus-within input {border-color:var(--stk-cyan) !important;
  box-shadow:0 0 0 2px rgba(97,231,255,.14) !important;}
[data-baseweb="select"] > div {border-radius:2px;background:rgba(2,7,14,.9);border-color:rgba(97,231,255,.25);}
.stRadio p,.stCheckbox span,[data-testid="stWidgetLabel"] p {font-family:var(--mono);font-size:11px;
  letter-spacing:.13em;text-transform:uppercase;color:#77a9c4;}

/* chips + ticker telemetry */
.yu-chiprow span {border-radius:2px !important;border:1px solid rgba(97,231,255,.3) !important;
  font-family:var(--mono) !important;letter-spacing:.06em !important;}
.yu-ticker {border:1px solid rgba(97,231,255,.3);background:rgba(2,8,15,.92);border-radius:2px;}
.yu-tick-in {font-family:var(--mono);color:#8fd8ee;}
.yu-tick-in b {color:var(--stk-cyan);text-shadow:0 0 10px rgba(97,231,255,.6);}
.yu-live {color:#7de8ff;font-family:var(--mono);}
.yu-story .r {font-family:var(--mono);color:#9ff0ff;border-radius:2px;background:rgba(97,231,255,.08);
  border-color:rgba(97,231,255,.35);}
.yu-story .x {color:#a8d5e8;}
.yu-feed .row {color:#a8d5e8;}

/* frames around charts & tables */
div[data-testid="stPlotlyChart"] {border:1px solid rgba(97,231,255,.16);border-radius:2px;
  background:rgba(4,11,20,.55);padding:8px 8px 3px;}
div[data-testid="stDataFrame"] {border:1px solid rgba(97,231,255,.18);border-radius:2px;}
div[data-testid="stExpander"] details {border-radius:2px;background:rgba(3,10,18,.7);
  border:1px solid rgba(97,231,255,.16);}
div[data-testid="stAlert"] {border-radius:2px;}
.yu-note,.yu-danger,.yu-ok,.yu-find {border-radius:2px;border-color:rgba(97,231,255,.28);}
.empty-state {border:1.5px dashed rgba(97,231,255,.4);border-radius:2px;background:
  radial-gradient(700px 220px at 50% 0%,rgba(97,231,255,.07),transparent 70%);}
code,.stMarkdown code {color:#9ff0ff;background:rgba(2,10,18,.9);border-color:rgba(97,231,255,.3);border-radius:2px;}
progress::-webkit-progress-value {background:linear-gradient(90deg,#1892b8,#61e7ff);
  box-shadow:0 0 18px rgba(97,231,255,.7);}
div[data-testid="stSidebar"] {background:linear-gradient(200deg,rgba(4,12,22,.98),rgba(2,6,12,.99)) !important;
  border-right:1px solid rgba(97,231,255,.18) !important;}
div[data-testid="stSidebar"] .yu-side-title {font-family:var(--mono);color:#9fe4fb;letter-spacing:.26em;}
.stCaption,.stCaption * {color:#5f94ad;}
'''
A1 = "\n</style>"
assert s.count(A1) == 1, "style close anchor"
s = s.replace(A1, HUD + A1, 1)

# ══ 2) hero → arc-core console ═══════════════════════════════════════════
A2 = '''    st.markdown(
        "<div class='yu-hero'>"
        "<div class='yu-title'>⚔ YUDA<span class='accent'>ANT</span>"
        "<span style=\\"font-size:13px;font-weight:600;color:#7c8db0;letter-spacing:.18em;margin-left:10px;\\">"
        "ARTIFICIAL-SOCIETY OBSERVATORY</span></div>"
        "<div class='yu-sub'>A small synthetic society of agents — they gather, trade, share, co-operate "
        "and steal in a seeded world. Every score and chart on this page is computed <b>live from that "
        "simulation</b>.</div>"
        "</div>", unsafe_allow_html=True)'''
assert s.count(A2) == 1, "hero anchor"
HERO2 = '''    st.markdown(
        "<div class='yu-hero stk-hero'>"
        "<div class='stk-reactor'><i></i><i></i><i></i><b></b><u></u><u></u></div>"
        "<div><div class='yu-title'>⚡ YUDA<span class='accent'>ANT</span>"
        "<span style=\\"font-size:12px;font-weight:600;color:#5f94ad;letter-spacing:.3em;margin-left:10px;\\">"
        "ARTIFICIAL-SOCIETY OBSERVATORY</span></div>"
        "<div class='yu-sub'>Synthetic society of " + str(int(st.session_state.get(\\"sb_population\\", 110))) +
        " agents · 8 transparently-scored actions · zero LLM, zero network. "
        "Every readout below is computed <b>live from the engine</b> — press Start on the control deck.</div>"
        "<span class='stk-sys'>SYSTEM NOMINAL · ENGINE " + ENGINE_VERSION + " · ARC CORE ONLINE</span>"
        "</div></div>", unsafe_allow_html=True)'''
s = s.replace(A2, HERO2, 1)

# ══ 3) HUD frame overlay in main() ════════════════════════════════════════
A3 = "    st.markdown(CSS, unsafe_allow_html=True)\n"
assert s.count(A3) == 1, "css-mark anchor"
FR = '''    st.markdown("<div class='stk-frame'><span class='c1'></span><span class='c2'></span><span class='c3'></span><span class='c4'></span><span class='t1'></span><span class='t2'></span></div>", unsafe_allow_html=True)
'''
s = s.replace(A3, A3 + FR, 1)

# ══ 4) plotly template → arc colors ═══════════════════════════════════════
pairs = [
    ('"colorway": ["#2dd4bf", "#818cf8", "#f5b23c", "#f87171",\n                 "#60a5fa", "#c084fc", "#34d399", "#fb923c"],',
     '"colorway": ["#61e7ff", "#ffcf6b", "#ff7ab6", "#9d7bff",\n                 "#5ef2c0", "#ff9d5c", "#7aa2ff", "#d9f7ff"],'),
    ('"gridcolor": "rgba(148,163,184,.12)", "zeroline": False', '"gridcolor": "rgba(97,231,255,.10)", "zeroline": False'),
    ('"bgcolor": "#0e1930", "bordercolor": "#2dd4bf"', '"bgcolor": "#051019", "bordercolor": "#61e7ff"'),
    ('"title": {"font": {"family": _PLOTLY_FONT, "size": 16, "color": "#dbe6fb"}}',
     '"title": {"font": {"family": _PLOTLY_FONT, "size": 15, "color": "#d9f7ff"}}'),
]
for old, new in pairs:
    assert old in s, f"template miss: {old[:40]}"
    s = s.replace(old, new)

open(P, "w", encoding="utf-8").write(s)
py_compile.compile(P, doraise=True)
print(f"STARK applied: {n0} -> {len(s)} bytes · compile clean")
