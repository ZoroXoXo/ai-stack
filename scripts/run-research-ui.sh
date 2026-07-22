#startup logic

#!/usr/bin/env bash
# Start Ollama (if not running) and Open WebUI (Docker) for the research workspace.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
# shellcheck disable=SC1091
if [ -f .env ]; then
  while IFS='=' read -r key value; do
    case "$key" in
      ''|'#*') continue ;;
    esac
    value="${value%\"}"
    value="${value#\"}"
    export "$key"="$value"
  done < <(grep -v '^[[:space:]]*#' .env | sed '/^[[:space:]]*$/d')
fi

RESEARCH_MODEL="${RESEARCH_MODEL:-phi3.5:3.8b-mini-instruct-q4_K_M}"
OPEN_WEBUI_PORT="${OPEN_WEBUI_PORT:-3000}"
AUTO_PULL_RESEARCH_MODEL="${AUTO_PULL_RESEARCH_MODEL:-1}"

if ! pgrep -x "ollama" >/dev/null 2>&1; then
  echo "Starting Ollama..."
  ollama serve &
  sleep 2
fi

if [ "$AUTO_PULL_RESEARCH_MODEL" != "0" ] && [ "$AUTO_PULL_RESEARCH_MODEL" != "false" ]; then
  if ! ollama list | grep -q "$(echo "$RESEARCH_MODEL" | cut -d: -f1)"; then
    echo "Pulling research model: $RESEARCH_MODEL"
    ollama pull "$RESEARCH_MODEL"
  fi
else
  echo "Model auto-pull disabled. Make sure $RESEARCH_MODEL is installed before opening Research."
fi

if command -v docker >/dev/null 2>&1; then
  if [ "$(docker ps -aq -f name=open-webui)" ]; then
    echo "Starting existing open-webui container..."
    docker start open-webui
  else
    echo "Creating open-webui container..."
    docker run -d \
      --name open-webui \
      -p "${OPEN_WEBUI_PORT}:3000" \
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