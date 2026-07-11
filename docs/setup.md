<!-- how to install and run it -->
<!-- connects to scripts/, .env.example, and pyproject.toml -->
# Setup

Target environment: Arch-based (or similar) Linux laptop.

## 1. Prerequisites

- Linux, ideally with a GPU for faster inference (CPU-only works, just slower).
- Python 3.10+
- Docker (optional, for Open WebUI) or a native Open WebUI install.
- `rofi` (or your launcher of choice) for the copilot's quick-access UI.

## 2. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
# or, on Arch:
# sudo pacman -S ollama          # CPU
# sudo pacman -S ollama-cuda     # NVIDIA GPU

systemctl --user enable --now ollama   # or: ollama serve
```

Pull the default research model:

```bash
ollama pull phi3.5:3.8b-mini-instruct-q4_K_M
```

See `models/recommended-models.md` for alternatives.

## 3. Install Open WebUI

Docker route (recommended for isolation):

```bash
docker run -d \
  --name open-webui \
  -p 8080:8080 \
  --add-host=host.docker.internal:host-gateway \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v open-webui-data:/app/backend/data \
  --restart unless-stopped \
  ghcr.io/open-webui/open-webui:main
```

Then open `http://localhost:8080` and connect it to your local Ollama
instance if it isn't auto-detected.

## 4. Set up the laptop copilot

```bash
cd ai-stack
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Edit `.env` as needed (model names, hotkey, log paths).

Run it:

```bash
./scripts/run-copilot.sh
```

Or directly:

```bash
python -m laptop_copilot.main
```

## 5. Run the tests

```bash
pytest tests/
```

## 6. Wire up the hotkey

Bind `scripts/run-copilot.sh` (or `copilot` once installed) to a keybinding
in your window manager (e.g. i3, sway) so it launches instantly via `rofi`.
Example i3 config line:

```
bindsym $mod+space exec --no-startup-id /path/to/ai-stack/scripts/run-copilot.sh
```

See `docs/roadmap.md` for what's implemented vs. planned at each milestone.