# YUDAANT — 2-minute demo script + judge Q&A (padh ke jaana, bhool mat jaana 😄)

## ⏱ The 120-second run-through (rehearse twice)
1. **(0:00) Hook — 15s** — Empty hero pe:
   "What happens when hundreds of simple agents must choose — share or steal — every day?
   YUDAANT is an artificial society you can actually run: 8 actions, transparent scoring,
   zero LLM magic. Every number on this page is computed live from the simulation."
2. **(0:15) Start — 20s** — sidebar: preset **🌀 Culture War** → Start → LIVE map with HUD
   (red dot, tickers): "This is live playback — watch trust collapse in real time."
   Press **⏭ Skip to end** for the rest.
3. **(0:35) Proof — 20s** — scroll to **🏆 Judges' Brief**:
   "One page the judges get: headline stats, a Society-DNA radar built from this exact run,
   a highlight reel where every claim cites its round number — and a reproducibility fingerprint.
   Same seed plus same settings ⇒ same md5. Rerun it yourself; I double-dare you."
4. **(0:55) Depth — 40s** — **🧠 Learning lab**: [L5] policy heatmaps ("each agent learns its own
   table via online REINFORCE — seed-deterministic"), [L9] culture condensation (sub-cultures),
   **⚔ stress arena** (rules-brain vs learned-brain under famine). Then **🗂 Study shelf**
   Δ-split: "I can diff two worlds — this Δ column is why parameter sweeps are one click."
5. **(1:35) Honesty moment — 15s** — **📖 Method & limits**:
   "Everything is synthetic. Observations and interpretations are visually separate.
   12 engine self-checks run on every cold start and are shown in the brief — failures
   would be surfaced, never hidden. Data lives only in your browser session."
6. **(1:50) Close — 10s** — society card export:
   "One JSON card = the whole world, loadable anywhere. Thank you."

## 🎤 One-liners that land
- "No API, no database, no LLM — a 4,335-line transparent engine in ONE file."
- "Judges can rerun any world: we print the seed AND an md5 fingerprint of the result table."
- "The UI is decoration; the engine is the product — and it checks its own maths, 12 ways."

## ❓ Judge Q&A — honest answers only
**Q: Why no LLM?** A: We study *mechanisms*, not language. Scoring is an auditable factor sum;
every decision's breakdown is inspectable (Agent inspector → WHY). An LLM would add cost,
nondeterminism and unverifiable choices.
**Q: Is this real social science?** A: No — it's a synthetic society. Findings are observations
about OUR model; the app says so on every panel and separates reading from observation.
**Q: How do we trust your results?** A: Same seed + settings ⇒ bit-identical frames (self-check
[1] proves it on every cold start). Conservation, ledger and learning checks guard the maths.
**Q: What about scaling?** A: Pure Python, so 110 agents × 200 rounds ≈ a few seconds; 250 × 500
stresses free hosting but works. Architecture is vectorised where it matters (numpy grids).
**Q: Where's the data?** A: Session-only by design — nothing stored server-side. Export CSV/JSON/zip
in 💾; a run's entire setting travels as a shareable society card.
**Q: Learning — explain simply.** A: Each agent keeps a value table over 8 actions, updates via
online REINFORCE with a personal learning rate; optional policy carry = generational culture.
Culture diffusion spreads neighbours' anchors — that's what the 🌀 slider is.

## 🚨 If the cloud link is slow/blank
Free tier sleeps after inactivity — reload once, wait ~10s for cold start (self-checks run).
If Manage app shows Error: ⋮ menu → "Clear cache and reinstall dependencies".
Demo day: keep the trycloudflare link or local `streamlit run app.py` as backup — zero network risk.
