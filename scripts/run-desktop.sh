#!/usr/bin/env bash
# Launch the PySide6 desktop shell.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ -d .venv ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

export PYTHONPATH="${ROOT_DIR}/src:${PYTHONPATH:-}"
python3 -m laptop_copilot.ui.desktop "$@"
