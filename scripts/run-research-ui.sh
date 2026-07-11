#startup logic

#!/usr/bin/env bash
# Start Ollama (if not running) and Open WebUI (Docker) for the research workspace.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
# shellcheck disable=SC1091
[ -f .env ] && source .env

RESEARCH_MODEL="${RESEARCH_MODEL:-phi3.5:3.8b-mini-instruct-q4_K_M}"
OPEN_WEBUI_PORT="${OPEN_WEBUI_PORT:-8080}"

if ! pgrep -x "ollama" >/dev/null 2>&1; then
  echo "Starting Ollama..."
  ollama serve &
  sleep 2
fi

if ! ollama list | grep -q "$(echo "$RESEARCH_MODEL" | cut -d: -f1)"; then
  echo "Pulling research model: $RESEARCH_MODEL"
  ollama pull "$RESEARCH_MODEL"
fi

if command -v docker >/dev/null 2>&1; then
  if [ "$(docker ps -aq -f name=open-webui)" ]; then
    echo "Starting existing open-webui container..."
    docker start open-webui
  else
    echo "Creating open-webui container..."
    docker run -d \
      --name open-webui \
      -p "${OPEN_WEBUI_PORT}:8080" \
      --add-host=host.docker.internal:host-gateway \
      -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
      -v open-webui-data:/app/backend/data \
      --restart unless-stopped \
      ghcr.io/open-webui/open-webui:main
  fi
  echo "Open WebUI available at http://localhost:${OPEN_WEBUI_PORT}"
else
  echo "Docker not found. Install Open WebUI natively — see docs/setup.md."
fi