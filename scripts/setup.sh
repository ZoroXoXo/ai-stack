#installation /bootstrap logic

#!/usr/bin/env bash
# One-time setup for the ai-stack project.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "== ai-stack setup =="

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example — edit it before continuing."
fi

if ! command -v ollama >/dev/null 2>&1; then
  echo "Ollama not found. Install it first:"
  echo "  curl -fsSL https://ollama.com/install.sh | sh"
  echo "See docs/setup.md for distro-specific package options."
else
  echo "Ollama found: $(ollama --version 2>/dev/null || echo 'version unknown')"
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found (optional, needed for the Open WebUI container path)."
fi

if [ ! -d .venv ]; then
  echo "Creating Python virtualenv..."
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip >/dev/null
pip install -e ".[dev]"

echo ""
echo "Setup complete."
echo "Next steps:"
echo "  1. Edit .env"
echo "  2. ./scripts/run-research-ui.sh   # start Ollama + Open WebUI"
echo "  3. ./scripts/run-copilot.sh       # start the laptop copilot"