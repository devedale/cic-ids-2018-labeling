#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
WITH_SYSTEM_DEPS="${1:-}"

log() {
  printf "[setup] %s\n" "$1"
}

ensure_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    printf "[setup] ERROR: comando mancante: %s\n" "$cmd" >&2
    exit 1
  fi
}

if [[ "$WITH_SYSTEM_DEPS" == "--system-deps" ]]; then
  ensure_cmd sudo
  ensure_cmd apt-get
  log "Installo dipendenze di sistema (openjdk-8-jdk, unrar, p7zip-full)..."
  sudo apt-get update
  sudo apt-get install -y openjdk-8-jdk unrar p7zip-full
fi

ensure_cmd python3

if [[ ! -d "$VENV_DIR" ]]; then
  log "Creo virtual environment in ${VENV_DIR}"
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

log "Aggiorno pip/setuptools/wheel"
pip install -U pip setuptools wheel

log "Installo requirements"
pip install -r "${ROOT_DIR}/requirements.txt"

log "Verifica moduli Python principali"
python3 - <<'PY'
import importlib
for name in ["boto3", "pandas", "sklearn", "yaml"]:
    importlib.import_module(name)
print("[setup] Python dependencies OK")
PY

log "Setup completato"
log "Per eseguire: source .venv/bin/activate && python main.py"
