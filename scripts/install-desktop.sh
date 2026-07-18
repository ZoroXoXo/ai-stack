#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DESKTOP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}"/applications
mkdir -p "$DESKTOP_DIR"

TPL="$ROOT_DIR/resources/ai-stack.desktop.template"
OUT="$DESKTOP_DIR/ai-stack.desktop"

if [ ! -f "$TPL" ]; then
  echo "Template not found: $TPL" >&2
  exit 1
fi

sed "s|%ROOT%|$ROOT_DIR|g" "$TPL" > "$OUT"
chmod 644 "$OUT"

# Refresh desktop database if available (non-fatal)
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
fi

echo "Installed desktop entry: $OUT"

echo "You can now launch 'AI Stack' from your desktop environment's application menu." 
