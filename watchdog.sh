#!/usr/bin/env bash
# YUDAANT public-link watchdog — keeps Streamlit (port 8501) AND the cloudflared
# quick tunnel alive; writes the current public URL to /home/user/yudaant/PUBLIC_URL.txt
set -u
APPDIR=/home/user/yudaant
WDIR=/tmp/yu_watchdog; mkdir -p "$WDIR"
URLF="$APPDIR/PUBLIC_URL.txt"
TUNPAT='cloudflared tunnel --url http://127.0.0.1:8501'
log(){ echo "[$(date '+%H:%M:%S')] $*"; }

start_app(){
  log "starting streamlit…"
  ( cd "$APPDIR" && nohup python -m streamlit run app.py --server.port 8501 \
      --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false \
      >>"$WDIR/app.log" 2>&1 & echo $! > "$WDIR/app.pid" )
  for _ in $(seq 1 30); do
    curl -sf --max-time 2 http://127.0.0.1:8501/_stcore/health >/dev/null && { log "app healthy"; return 0; }
    sleep 2
  done
  log "app FAILED to start (see $WDIR/app.log)"; return 1
}

start_tunnel(){
  pkill -f "$TUNPAT" 2>/dev/null; sleep 1
  log "starting cloudflared tunnel…"
  chmod +x "$APPDIR/tools/cloudflared" 2>/dev/null
  : > "$WDIR/tun.log"
  ( nohup "$APPDIR/tools/cloudflared" tunnel --url http://127.0.0.1:8501 --no-autoupdate \
      >>"$WDIR/tun.log" 2>&1 & echo $! > "$WDIR/tun.pid" )
  for _ in $(seq 1 30); do
    u=$(grep -Eo 'https://[a-z0-9-]+\.trycloudflare\.com' "$WDIR/tun.log" | tail -1)
    [ -n "${u:-}" ] && { echo "$u" > "$URLF"; log "tunnel up → $u"; return 0; }
    sleep 2
  done
  log "tunnel FAILED to come up (see $WDIR/tun.log)"; return 1
}

app_ok(){ curl -sf --max-time 3 http://127.0.0.1:8501/_stcore/health >/dev/null; }
tun_ok(){
  u=$(cat "$URLF" 2>/dev/null || true)
  [ -n "${u:-}" ] && curl -sf --max-time 15 "$u/_stcore/health" >/dev/null
}

log "watchdog started"
TFAILS=0
while true; do
  app_ok || start_app
  if tun_ok; then
    TFAILS=0
  else
    if pgrep -f "$TUNPAT" >/dev/null; then
      if [ ! -s "$URLF" ]; then
        u=$(grep -Eo 'https://[a-z0-9-]+\.trycloudflare\.com' "$WDIR/tun.log" 2>/dev/null | tail -1)
        [ -n "${u:-}" ] && { echo "$u" > "$URLF"; log "re-scanned URL → $u"; }
      fi
      TFAILS=$((TFAILS+1))
      if [ "$TFAILS" -ge 6 ]; then
        log "tunnel process alive but URL dead for ${TFAILS} checks — forcing restart"
        start_tunnel; TFAILS=0
      else
        log "tunnel URL not answering ($TFAILS/6) — waiting"
      fi
    else
      start_tunnel; TFAILS=0
    fi
  fi
  sleep 15
done
