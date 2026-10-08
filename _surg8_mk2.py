import random
import py_compile

P = "/home/user/yudaant/app.py"
s = open(P, encoding="utf-8").read()
n0 = len(s)

# ── deterministic starfield layers (decoration only — seed fixed, noted in code) ──
rnd = random.Random(777)
def stars(n, ymax=1050, alpha=(0.25, 0.85)):
    out = []
    for _ in range(n):
        x, y = rnd.randint(0, 1900), rnd.randint(0, ymax)
        a = rnd.uniform(*alpha)
        sz = rnd.choice([0, 0, 0.4])
        out.append(f"{x}px {y}px 0 {sz}px rgba(188,240,255,{a:.2f})")
    return ",".join(out)
S1, S2 = stars(130), stars(80)

# ── 1) MK-II CSS, appended inside the <style> block ──
MK2 = '''
/* ── MK-II CINEMATIC: starfield, tron horizon, film grain, vignette, glitch, holo, boot ── */
.stk-sky i {position:fixed;top:5%;left:3%;width:1px;height:1px;border-radius:50%;background:transparent;
  z-index:-1;pointer-events:none;will-change:opacity;animation:stkTwk 7s ease-in-out infinite alternate;}
.stk-sky i:nth-child(2) {animation-delay:3.4s;opacity:.75;}
@keyframes stkTwk {from {opacity:.35;} to {opacity:.9;}}
.stk-floor {position:fixed;left:-60vw;right:-60vw;bottom:-48vh;height:88vh;z-index:-1;pointer-events:none;
  opacity:.15;transform:perspective(560px) rotateX(64deg);
  background-image:linear-gradient(rgba(97,231,255,.55) 1px,transparent 1px),
    linear-gradient(90deg,rgba(97,231,255,.42) 1px,transparent 1px);
  background-size:72px 72px;
  -webkit-mask-image:linear-gradient(to top,#000 6%,transparent 60%);
  mask-image:linear-gradient(to top,#000 6%,transparent 60%);
  animation:stkFloor 9s linear infinite;}
@keyframes stkFloor {from {background-position:0 0;} to {background-position:0 72px;}}
.stk-grain {position:fixed;inset:-60px;z-index:3;pointer-events:none;opacity:.05;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='140' height='140'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='140' height='140' filter='url(%23n)'/></svg>");
  animation:stkGrain 1.15s steps(3) infinite;}
@keyframes stkGrain {0% {transform:translate(0,0);} 33% {transform:translate(-14px,9px);}
  66% {transform:translate(10px,-15px);} 100% {transform:translate(0,0);}}
.stk-frame {box-shadow:inset 0 0 190px 34px rgba(1,4,9,.5);}
.yu-mk2 .yu-title {animation:stkBoot 5s steps(1) 1 both, stkGlx 9s 4.5s infinite;}
@keyframes stkGlx {0%,91% {text-shadow:0 0 18px rgba(97,231,255,.45);}
  92% {text-shadow:-3px 0 rgba(255,122,182,.85),3px 0 rgba(97,231,255,.85);}
  93.5% {text-shadow:2px 1px rgba(255,207,107,.7),-2px -1px rgba(97,231,255,.8);}
  95%,100% {text-shadow:0 0 18px rgba(97,231,255,.45);}}
.stk-reactor {animation:stkHolo 5.5s ease-in-out infinite;}
@keyframes stkHolo {0%,100% {filter:none;} 46% {filter:brightness(1.07);}
  47% {filter:brightness(.9) saturate(1.45);} 48% {filter:brightness(1.12);}}
.stTabs [data-baseweb="tab-list"] {position:relative;overflow:hidden;}
.stTabs [data-baseweb="tab-list"]::after {content:"";position:absolute;left:-30%;bottom:0;width:30%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(97,231,255,.9),transparent);
  animation:stkSweep 7s linear infinite;}
@keyframes stkSweep {to {left:130%;}}
div[data-testid="stPlotlyChart"] svg {filter:drop-shadow(0 0 9px rgba(97,231,255,.08));}
.stk-boot {position:fixed;inset:0;z-index:9999;display:grid;place-items:center;background:#02060c;
  pointer-events:none;animation:stkBootOut 3.9s ease-in .3s forwards;}
@keyframes stkBootOut {0%,72% {opacity:1;} 100% {opacity:0;visibility:hidden;}}
.stk-boot-in {font-family:var(--mono);color:#9feaf9;text-align:left;min-width:360px;}
.stk-boot-in b {display:block;letter-spacing:.34em;color:#61e7ff;margin-bottom:14px;font-size:14px;}
.stk-boot-in p {margin:4px 0;font-size:12px;letter-spacing:.12em;opacity:0;animation:stkRow .5s forwards;}
.stk-boot-in p:nth-of-type(1) {animation-delay:.5s;}
.stk-boot-in p:nth-of-type(2) {animation-delay:1.1s;}
.stk-boot-in p:nth-of-type(3) {animation-delay:1.7s;}
@keyframes stkRow {from {opacity:0;transform:translateX(-8px);} to {opacity:1;transform:none;}}
.stk-boot-bar {display:block;height:2px;background:linear-gradient(90deg,#0e7490,#61e7ff);margin-top:16px;
  width:0;animation:stkBar 2.2s ease-out .6s forwards;box-shadow:0 0 14px rgba(97,231,255,.7);}
@keyframes stkBar {to {width:100%;}}
'''
A_CSS = "\n</style>"
assert s.count(A_CSS) == 1, "css close anchor"
s = s.replace(A_CSS, MK2 + A_CSS, 1)

# ── 2) hero gets yu-mk2 class ──
A_HERO = "\"<div class='yu-hero stk-hero'>\""
assert s.count(A_HERO) == 1, "hero anchor"
s = s.replace(A_HERO, "\"<div class='yu-hero stk-hero yu-mk2'>\"", 1)

# ── 3) overlays + boot sequence after the HUD-frame line in main() ──
A_FRAME = "    st.markdown(\"<div class='stk-frame'><span class='c1'></span><span class='c2'></span><span class='c3'></span><span class='c4'></span><span class='t1'></span><span class='t2'></span></div>\", unsafe_allow_html=True)\n"
assert s.count(A_FRAME) == 1, "frame anchor"
OVERLAYS = """    st.markdown("<div class='stk-sky'><i style='box-shadow:" + _STARS1 + "'></i>"
                "<i style='box-shadow:" + _STARS2 + "'></i></div>"
                "<div class='stk-floor'></div><div class='stk-grain'></div>", unsafe_allow_html=True)
    if not st.session_state.get("_mk2_boot"):
        st.session_state["_mk2_boot"] = True
        _ck = cached_checks()
        _ckmsg = "ALL GREEN" if all(c["ok"] for c in _ck) else "SEE METHOD & LIMITS"
        st.markdown("<div class='stk-boot'><div class='stk-boot-in'><b>◈ YUDAANT MK-II</b>"
                    f"<p>ARC CORE ............. ONLINE · ENGINE {ENGINE_VERSION}</p>"
                    f"<p>SELF-CHECKS ......... {len(_ck)} GATES · {_ckmsg}</p>"
                    "<p>UI OVERLAY .......... CINEMATIC · GRAIN · HOLO-FLICKER</p>"
                    "<span class='stk-boot-bar'></span></div></div>", unsafe_allow_html=True)
"""
s = s.replace(A_FRAME, A_FRAME + OVERLAYS, 1)

# star strings as module constants, injected right before main()
A_MAIN = "def main() -> None:"
assert s.count(A_MAIN) == 1
CONSTS = (f"_STARS1 = \"{S1}\"\n_STARS2 = \"{S2}\"\n\n\n" + A_MAIN)
s = s.replace(A_MAIN, CONSTS, 1)

# ── 4) bloom halos on agents — society view map ──
B1 = '''            fig.add_trace(go.Scatter(x=d0["x"], y=d0["y"], mode="markers", name=f"{cat} ({len(d0['x'])})",
                                     marker=dict(size=d0["sz"], color=CAT_COLOR.get(cat, "#94a3b8"), opacity=0.85,
                                                 line=dict(width=0.6, color="rgba(2,8,16,.85)")),
                                     text=d0["hov"], hoverinfo="text"))'''
assert s.count(B1) == 1, "society map trace anchor"
B1N = '''            _halo = [s0 * 2.7 for s0 in d0["sz"]]
            fig.add_trace(go.Scatter(x=d0["x"], y=d0["y"], mode="markers", showlegend=False, hoverinfo="skip",
                                     marker=dict(size=_halo, color=CAT_COLOR.get(cat, "#94a3b8"), opacity=0.12)))
''' + B1
s = s.replace(B1, B1N, 1)

# ── 5) bloom halos — live map ──
B2 = '''            fig.add_trace(go.Scatter(
                x=d0["x"], y=d0["y"], mode="markers",
                name=f"{cat} ({len(d0['x'])})",
                marker=dict(size=d0["sz"], color=CAT_COLOR.get(cat, "#94a3b8"), opacity=0.85,
                            line=dict(width=0.6, color="rgba(2,8,16,.85)")),
                text=d0["hov"], hoverinfo="text"))'''
assert s.count(B2) == 1, "live map trace anchor"
B2N = '''            _halo = [s0 * 2.7 for s0 in d0["sz"]]
            fig.add_trace(go.Scatter(x=d0["x"], y=d0["y"], mode="markers", showlegend=False, hoverinfo="skip",
                                     marker=dict(size=_halo, color=CAT_COLOR.get(cat, "#94a3b8"), opacity=0.12)))
''' + B2
s = s.replace(B2, B2N, 1)

open(P, "w", encoding="utf-8").write(s)
py_compile.compile(P, doraise=True)
print(f"MK-II applied: {n0} -> {len(s)} bytes · compile clean")
