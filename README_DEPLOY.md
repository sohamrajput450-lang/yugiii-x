# YUDAANT — permanent free link (v2, ab theme file bhi)

Repo root me exactly 3 entries chahiye:
  app.py
  requirements.txt
  .streamlit/config.toml   ← isse dark theme + styling sahi aayegi

requirements.txt:
  streamlit>=1.34
  plotly>=5.18
  pandas>=2.0
  numpy>=1.26

## Streamlit Cloud update steps
1. github.com/<user>/<repo> → Upload files → naya app.py drag karke OVERWRITE-commit
2. Add file → Create new file → filename me literally type karo: `.streamlit/config.toml`
   (slash type karte hi .streamlit folder ban jaayega) → paste:
   [theme]
   base = "dark"
   primaryColor = "#61e7ff"
   backgroundColor = "#03080f"
   secondaryBackgroundColor = "#071220"
   textColor = "#d5eefb"
   [browser]
   gatherUsageStats = false
3. Commit → auto-rebuild (~1 min) → link ready, ab AURUM FX skin ke saath ✨
4. (_surg3.py jaisa koi scratch file pade ho repo me to delete kar dena.)

## Demo flow
See **DEMO_SCRIPT.md** — 2-min pitch, click order, judge Q&A answers.

## Demo flow
🌀 Culture War preset → Start → Skip to end → 🧠 Learning lab ([L5] heatmap, [L9]
condensation, ⚔ stress arena) → 🗂 shelf Δ-split → 📇 society card.
Sab data simulated; same seed = same run; 12 self-checks har process cold-start pe.
