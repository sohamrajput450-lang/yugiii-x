import re
import py_compile

P = "/home/user/yudaant/app.py"
s = open(P, encoding="utf-8").read()
n0 = len(s)

# ── 1) JUDGE SUITE functions, before the hero section ──────────────────────
ANCHOR1 = "# ── hero + KPI strip ─"
assert s.count(ANCHOR1) == 1

BLOCK = '''# ═══════════════════════════════════════════════════════════════════════════
#  JUDGE SUITE — one-page brief, society-DNA radar, highlight reel, ticker
#  Everything computed live from the finished run's own dataframes.
# ═══════════════════════════════════════════════════════════════════════════

def society_radar(res: SimResult) -> Optional[go.Figure]:
    """‘Society DNA’ radar — every axis is a final-round value from this run's
    rounds_df; axes whose underlying column is absent are dropped, never faked.
    Min–max scaling (prosperity) spans this run only; hovers carry raw values."""
    rd = res.rounds_df
    if rd.empty:
        return None
    last = rd.iloc[-1]
    axes: list[tuple[str, float, str]] = []

    def push(name: str, value: float, rawtxt: str) -> None:
        axes.append((name, float(np.clip(value, 0.0, 1.0)), rawtxt))

    if "cooperation_rate" in rd:
        push("co-operation", float(last["cooperation_rate"]),
             f"{last['cooperation_rate'] * 100:.1f}% at the final round")
    if "survival" in rd:
        push("survival", float(last["survival"]),
             f"{res.meta.get('alive_end', '?')}/{res.n0} alive at end")
    if "gini_wealth" in rd:
        push("equality", 1.0 - float(last["gini_wealth"]),
             f"gini {last['gini_wealth']:.3f} (lower = fairer split)")
    if "avg_wealth" in rd and float(rd["avg_wealth"].max()) > float(rd["avg_wealth"].min()):
        wmin, wmax = float(rd["avg_wealth"].min()), float(rd["avg_wealth"].max())
        push("prosperity", (float(last["avg_wealth"]) - wmin) / (wmax - wmin),
             f"{last['avg_wealth']:.1f} pts · scaled to this run's own {wmin:.0f}–{wmax:.0f} range")
    if "cooperation_rate" in rd and len(rd) > 5:
        c = rd["cooperation_rate"]
        push("stability", 1.0 - min(1.0, float(c.std()) / max(float(c.mean()), 1e-9)),
             f"σ {c.std():.3f} on μ {c.mean():.3f} over {len(rd)} rounds")
    if "var_within" in rd.columns and float(rd["var_within"].max()) > 1e-9:
        push("cohesion", 1.0 - min(1.0, float(last["var_within"]) / 0.01),
             f"within-group behavioural variance {last['var_within']:.4f} (≥0.01 ≈ full sub-culture split)")
    if "policy_entropy" in rd.columns and float(rd["policy_entropy"].max()) > 1e-6:
        bits = math.log2(8.0)
        push("exploration", float(last["policy_entropy"]) / bits,
             f"policy entropy {last['policy_entropy']:.2f}/{bits:.1f} bits")
    if len(axes) < 3:
        return None
    names = [a[0] for a in axes] + [axes[0][0]]
    vals = [a[1] for a in axes] + [axes[0][1]]
    txts = [a[2] for a in axes] + [axes[0][2]]
    fig = go.Figure(go.Scatterpolar(
        r=vals, theta=names, fill="toself", fillcolor="rgba(45,212,191,.16)",
        line=dict(color="#2dd4bf", width=3),
        marker=dict(size=7, color="#5eead4", line=dict(color="#06251f", width=1)),
        text=txts, hoverinfo="text", name="this run"))
    fig.update_layout(
        height=390, margin=dict(l=56, r=56, t=44, b=30), showlegend=False,
        polar=dict(bgcolor="rgba(0,0,0,0)",
                   radialaxis=dict(range=[0, 1], gridcolor="rgba(148,163,184,.16)",
                                   angleangle=90, tickfont=dict(size=9, color="#5c6f92")),
                   angularaxis=dict(gridcolor="rgba(148,163,184,.16)", angle=90,
                                    tickfont=dict(size=11.5, color="#a9c0e2"))))
    return fig


def story_moments(res: SimResult) -> list[tuple[str, str]]:
    """Highlight reel — the drama a judge can quote, located in the data."""
    rd, out = res.rounds_df, []
    if len(rd):
        r = rd.reset_index(drop=True)
        if "cooperation_rate" in r:
            i = int(r["cooperation_rate"].idxmax())
            out.append((f"r{i + 1}", f"🤝 Co-operation peaked at {r.loc[i, 'cooperation_rate'] * 100:.0f}% "
                                     f"(round {i + 1} of {len(r)})"))
            i = int(r["cooperation_rate"].idxmin())
            out.append((f"r{i + 1}", f"🥶 Trust bottomed — only {r.loc[i, 'cooperation_rate'] * 100:.0f}% "
                                     f"chose to co-operate in round {i + 1}"))
        if "deaths" in r and r["deaths"].max() > 0:
            dd = r["deaths"].diff().fillna(r["deaths"])
            i = int(dd.idxmax())
            out.append((f"r{i + 1}", f"💀 Deadliest round: {int(dd.iloc[i])} died in round {i + 1}; "
                                     f"{int(r['deaths'].iloc[-1])} total"))
        if "gini_wealth" in r:
            i = int(r["gini_wealth"].idxmax())
            out.append((f"r{i + 1}", f"⚖️ Most unequal moment: Gini {r.loc[i, 'gini_wealth']:.3f} in round {i + 1}"))
        if "var_within" in r.columns:
            above = r.index[r["var_within"] > 0.01]
            if len(above):
                i0 = int(above[0])
                out.append((f"r{i0 + 1}", f"🌀 Sub-cultures condensed: within-group variance crossed 0.01 in "
                                         f"round {i0 + 1} and stayed above it for {int(len(above))} rounds"))
        if "groups" in r and r["groups"].max() > 0:
            i = int(r["groups"].idxmax())
            out.append((f"r{i + 1}", f"⭕ Crowds: group formation peaked at {int(r.loc[i, 'groups'])} camps "
                                     f"in round {i + 1}"))
    ev = res.events or []
    firsts: dict = {}
    for e in ev:
        firsts.setdefault(e["kind"], e)
    for kind, icon in (("betray", "🗡"), ("trade", "🔁"), ("death", "🕯")):
        e = firsts.get(kind)
        if e:
            out.append((f"r{e['round']}", f"{icon} First recorded {kind} — {e['text']}"))
    seen, uniq = set(), []
    for tag, txt in out:
        if txt not in seen:
            seen.add(txt)
            uniq.append((tag, txt))
    return uniq[:8]


def render_judges_brief(res: SimResult, checks: list[dict]) -> None:
    rd = res.rounds_df
    if rd.empty:
        st.info("The run produced no rounds — nothing to summarise.")
        return
    last = rd.iloc[-1]
    st.caption("One page, auto-generated from this run's own dataframes — no hand-tuned numbers anywhere. "
               "All data is synthetic; ‘reading’-style lines are interpretations and stay visually marked.")

    tick = (f"SEED {res.cfg.seed} · {res.cfg.population} agents × {res.cfg.rounds} rounds · policy "
            f"{res.cfg.policy} · 🌀 influence {res.cfg.influence:.2f} · final co-operation "
            f"{last['cooperation_rate'] * 100:.0f}% · survival {last['survival'] * 100:.0f}% · "
            f"{int(last['deaths'])} deaths · Gini {last['gini_wealth']:.3f} · field food "
            f"{last['world_food']:,.0f} · {len(res.events):,} events · {res.meta.get('decisions', 0):,} "
            f"decision records · computed in {res.meta['run_ms']:,} ms · pure Python · "
            f"self-checks {sum(1 for c in checks if c['ok'])}/{len(checks)} green")
    st.markdown("<div class='yu-ticker'><div class='yu-tick-in'><b>✦ " + tick + "</b><span class='sep'></span>"
                "<b>✦ " + tick + "</b><span class='sep'></span></div></div>", unsafe_allow_html=True)

    mega = [
        (f"{last['cooperation_rate'] * 100:.0f}%", "co-operation rate",
         f"started at {rd['cooperation_rate'].iloc[0] * 100:.0f}% · trend "
         f"{'▲ up' if len(rd) > 4 and rd['cooperation_rate'].iloc[-1] > rd['cooperation_rate'].iloc[:4].mean() else '▼ down'}",
         PALETTE["teal"]),
        (f"{last['survival'] * 100:.0f}%", "survival",
         f"{res.meta.get('alive_end', '?')} of {res.n0} agents still alive", PALETTE["blue"]),
        (f"{last['gini_wealth']:.3f}", "wealth gini",
         "0 = equal shares · 1 = one owner", PALETTE["violet"]),
        (f"{res.meta['run_ms']:,} ms", "compute time",
         "pure Python engine · zero APIs · fully offline", PALETTE["amber"]),
    ]
    st.markdown("<div class='yu-mega-row'>" + "".join(
        f"<div class='yu-mega'><div class='v' style='color:{c}'>{v}</div>"
        f"<div class='l'>{lab}</div><div class='s'>{sub}</div></div>"
        for v, lab, sub, c in mega) + "</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.12])
    with c1:
        st.markdown("**🧬 Society DNA** — axes are this run's final-round metrics; hover any vertex for raw value")
        fig = society_radar(res)
        if fig is not None:
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Not enough signal axes for a radar yet — run more rounds.")
    with c2:
        st.markdown("**🎬 Highlight reel** — every line locates itself in the recorded data")
        rows = "".join(f"<div class='yu-story'><span class='r'>{tag}</span><span class='x'>{txt}</span></div>"
                       for tag, txt in story_moments(res)) or \
               "<div class='yu-story'><span class='x'>quiet world — nothing crossed a milestone bar</span></div>"
        st.markdown(f"<div class='yu-feed' style='max-height:390px'>{rows}</div>", unsafe_allow_html=True)

    st.markdown("**🔥 What the data shouts** — top findings of this run (full list in 🧭 Discoveries)")
    try:
        finds = discover(res)
    except Exception:
        finds = []
    for fnd in finds[:4]:
        st.markdown(
            f"<div class='yu-find {fnd['severity']}'><h4>{fnd['title']}</h4>"
            f"<div class='obs'>{fnd['observed']}</div>"
            + (f"<div class='read'>{fnd['reading']}</div>" if fnd.get("reading") else "")
            + "</div>", unsafe_allow_html=True)
    if not finds:
        st.caption("No finding crossed the reporting bar — usually a short or very stable run.")

    fp = hashlib.md5(rd.to_csv(index=False).encode()).hexdigest()[:12]
    okn = sum(1 for c in checks if c["ok"])
    st.markdown(
        f"<div class='yu-ok'><b>🔁 Reproducibility fingerprint</b> — same engine + same settings + same seed ⇒ "
        f"same numbers, same fingerprint. Seed <code>{res.cfg.seed}</code> · config hash "
        f"<code>{res.meta['config_hash']}</code> · rounds-table md5 <code>{fp}</code>. A judge can rerun this "
        f"exact world and diff the CSV export (fingerprint assumes the same library versions, noted openly).</div>"
        f"<div class='yu-note'><b>🧪 Engine self-checks: {okn}/{len(checks)} passed at cold start</b> — "
        f"deterministic replay, conservation, score-sum, death ledger, learning update and more. They verify "
        f"the maths — not the morals 😎 · exports & raw tables in 💾 Data & export.</div>",
        unsafe_allow_html=True)

    with st.expander(f"🧪 Self-check ledger — {okn}/{len(checks)} green", expanded=okn != len(checks)):
        for c in checks:
            st.markdown(
                f"<div class='yu-story'><span class='r'>{'✅' if c['ok'] else '❌'}</span>"
                f"<span class='x'><b>{c['check']}</b> — {str(c['detail']).splitlines()[0][:140]}</span></div>",
                unsafe_allow_html=True)


'''
s = s.replace(ANCHOR1, BLOCK + ANCHOR1, 1)

# ── 2) tabs list: append Judges' brief ──────────────────────────────────────
A2 = '"📖 Method & limits"])'
assert s.count(A2) == 1
s = s.replace(A2, '"📖 Method & limits", "🏆 Judges\u2019 brief"])', 1)

# ── 3) main: wire the new tab body ─────────────────────────────────────────
A3 = "    with tabs[8]:\n        render_method(res, checks)\n"
assert s.count(A3) == 1
s = s.replace(A3, A3 + """    with tabs[9]:
        if live:
            render_live_wait()
        elif res:
            render_judges_brief(res, checks)
        else:
            render_no_run("🏆 the judges' brief writes itself after a run — headline numbers, society DNA, "
                          "highlight reel and a reproducibility fingerprint")
""", 1)

# ── 4) main: pointer chip under KPI strip ──────────────────────────────────
A4 = "    if res is not None and not live:\n        render_kpi_strip(res)\n"
assert s.count(A4) == 1
A4B = '''"        st.markdown("<div class='yu-chiprow'>" + chip("✨ 🏆 Judges’ brief tab — one-page summary of everything below, ready to screenshot", "#2a2044", "#fcd34d") + "</div>", unsafe_allow_html=True)\n'''
s = s.replace(A4, A4 + A4B, 1)

# ── 5) live HUD strip ──────────────────────────────────────────────────────
A5 = "    cL, cR = st.columns([2.05, 1])\n    with cL:\n        fig = go.Figure()\n        g = np.array(fr["
assert s.count(A5) == 1
s = s.replace(A5, """    st.markdown(
        f"<div class='yu-live'><span class='yu-live-dot'></span> LIVE&nbsp;FEED&nbsp;·&nbsp;"
        f"<span style='color:#c3d0e6;letter-spacing:.02em;text-transform:none;font-weight:700'>"
        f"seed {cfg.seed} · round {soc.rnd}/{cfg.rounds} · {fr['n_alive']} agents · deaths {int(row.get('deaths', 0))} "
        f"· groups {int(row.get('groups', 0))}</span></div>", unsafe_allow_html=True)
""" + A5, 1)

# ── 6) CSS for judge suite ──────────────────────────────────────────────────
A6 = "@keyframes yuFadeUp {"
assert s.count(A6) == 1
CSS_ADD = """/* ── judge suite skins ── */
.yu-mega-row {display:flex; gap:12px; flex-wrap:wrap; margin:4px 0 14px 0;}
.yu-mega {flex:1 1 170px; text-align:center; padding:16px 10px 13px; position:relative; overflow:hidden;
  background:linear-gradient(170deg, rgba(20,32,56,.92), rgba(11,18,32,.86));
  border:1px solid rgba(148,163,184,.18); border-radius:16px; backdrop-filter:blur(8px);
  transition:transform .2s ease, border-color .2s ease; animation:yuFadeUp .6s ease both;}
.yu-mega:hover {transform:translateY(-2px); border-color:rgba(45,212,191,.4);}
.yu-mega::before {content:""; position:absolute; inset:0; pointer-events:none;
  background:radial-gradient(130px 62px at 50% -12px, rgba(45,212,191,.16), transparent 72%);}
.yu-mega .v {font-size:30px; font-weight:900; letter-spacing:.02em; line-height:1.15;
  font-variant-numeric:tabular-nums; text-shadow:0 0 26px rgba(45,212,191,.22);}
.yu-mega .l {font-size:10px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; color:#7c8db0; margin-top:3px;}
.yu-mega .s {font-size:11px; color:#8ea0bd; margin-top:2px;}
.yu-ticker {border:1px solid rgba(148,163,184,.16); border-radius:12px; overflow:hidden;
  background:rgba(8,14,26,.72); margin:2px 0 12px 0; backdrop-filter:blur(6px);}
.yu-tick-in {display:inline-block; white-space:nowrap; padding:7px 0; font-size:12.5px; color:#b9c7de;
  animation:yuTick 40s linear infinite;}
.yu-ticker:hover .yu-tick-in {animation-play-state:paused;}
.yu-tick-in b {color:#5eead4; font-weight:800;}
.yu-tick-in .sep {padding:0 26px; color:#334366;}
@keyframes yuTick {from {transform:translateX(0);} to {transform:translateX(-50%);}}
.yu-live {display:flex; align-items:center; gap:9px; margin:0 0 8px 0; font-size:11.5px;
  letter-spacing:.14em; text-transform:uppercase; color:#fda4af; font-weight:800;}
.yu-live-dot {width:9px; height:9px; border-radius:50%; background:#f87171;
  animation:yuBlink 1.4s ease-out infinite;}
@keyframes yuBlink {0% {box-shadow:0 0 0 0 rgba(248,113,113,.6);}
  70% {box-shadow:0 0 0 10px rgba(248,113,113,0);} 100% {box-shadow:0 0 0 0 rgba(248,113,113,0);}}
.yu-story {display:flex; gap:10px; align-items:baseline; padding:7px 10px;
  border-bottom:1px dashed rgba(148,163,184,.12); transition:background .15s ease;}
.yu-story:hover {background:rgba(45,212,191,.05); border-radius:9px;}
.yu-story .r {font-variant-numeric:tabular-nums; color:#5eead4; font-weight:800; font-size:11.5px;
  white-space:nowrap; background:rgba(45,212,191,.09); border:1px solid rgba(45,212,191,.25);
  padding:1px 8px; border-radius:999px;}
.yu-story .x {color:#c3d0e6; font-size:12.8px; line-height:1.45;}

"""
s = s.replace(A6, CSS_ADD + A6, 1)

open(P, "w", encoding="utf-8").write(s)
py_compile.compile(P, doraise=True)
print(f"applied: {n0} -> {len(s)} bytes · compile clean")
