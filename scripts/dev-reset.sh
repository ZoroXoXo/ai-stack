#cleanup/reset logic for local development state

#!/usr/bin/env bash
# Wipe local dev state (logs, cached data, memory) without touching config or code.
# Does NOT touch Ollama models or the Open WebUI container/volume.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

read -r -p "This will delete logs/, data/cache/*, data/memory/* and data/notes/*. Continue? [y/N] " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "Aborted."
  exit 0
fi

rm -rf logs/*.log
find data/cache data/memory data/notes -type f ! -name '.gitkeep' -delete

echo "Dev state reset."