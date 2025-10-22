#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/srv/musshop"
BRANCH="main"
GIT_REMOTE="origin"
VENV="$APP_DIR/.venv"
PY="$VENV/bin/python"
MANAGE="$PY $APP_DIR/manage.py"
DJANGO_SETTINGS_MODULE="config.settings"
GUNICORN_SERVICE="gunicorn-musshop"
NGINX_SERVICE="nginx"

log(){ printf "\n\033[1;36m[DEPLOY]\033[0m %s\n" "$*"; }

cd "$APP_DIR"

log "Точка отката: $(git rev-parse --short HEAD)"
echo "PRE_DEPLOY $(date +'%F %T') $(git rev-parse --short HEAD)" >> "$APP_DIR/deploy.log" || true

log "Git pull (rebase + autostash)"
git fetch --all --prune
git checkout "$BRANCH"
git pull --rebase --autostash "$GIT_REMOTE" "$BRANCH"

log "Venv"
[ -x "$PY" ] || python3 -m venv "$VENV"
# shellcheck disable=SC1090
source "$VENV/bin/activate"
python -m pip install -U pip wheel >/dev/null
[ -f requirements.txt ] && pip install -r requirements.txt || true

log "Env & checks"
export DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE"
export PYTHONUNBUFFERED=1

log "Migrations"
$MANAGE migrate

log "Collectstatic"
$MANAGE collectstatic --noinput

log "Restart services"
systemctl restart "$GUNICORN_SERVICE"
systemctl restart "$NGINX_SERVICE"

log "Gunicorn logs:"
journalctl -u "$GUNICORN_SERVICE" -n 50 --no-pager || true

log "Done. Commit: $(git rev-parse --short HEAD)"
