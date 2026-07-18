# ai-stack

Local-first AI assistant for Linux laptops. It combines two complementary
products:

- **Research Workspace** — Open WebUI + Ollama for chat, model-driven research,
  and persistent workspace notes.
- **Laptop Copilot** — a native Python agent (CLI + PySide6 desktop shell) for
  safe desktop actions using a whitelist of tools.

See `docs/` for the PRD, architecture, and a longer setup guide.

## Requirements

- Linux (development targeted at desktop Linux)
- Python 3.10+ (use the provided `./scripts/setup.sh` to create a `.venv`)
- Docker (for Open WebUI runtime) and Ollama installed locally for research

## Quick start

1. Copy and adjust environment files:

```bash
cp .env.example .env
# edit .env if you want to change ports or model names
```

2. Bootstrap the environment (installs Python deps into `.venv`):

```bash
./scripts/setup.sh
source .venv/bin/activate
export PYTHONPATH="${PWD}/src"
```

3. Start components (order is flexible):

```bash
./scripts/run-research-ui.sh   # starts Ollama + Open WebUI (Docker)
./scripts/run-copilot.sh       # CLI copilot / rofi entrypoint
./scripts/run-desktop.sh       # PySide6 desktop shell (Copilot/Research/Settings)
```

Notes:
- The desktop shell is at `src/laptop_copilot/ui/desktop.py` and exposes three
  pages: Copilot, Research, Settings.
- If your local Open WebUI frontend runs on a non-default port (e.g. 3000), set
  `FRONTEND_URL` in `.env` or `OPEN_WEBUI_PORT` to match; the UI prefers
  `FRONTEND_URL` when present.

## Environment variables (important)

- `RESEARCH_MODEL` — model name pulled by the research script (default in
  `.env.example`).
- `OPEN_WEBUI_PORT` — host port to map to the Open WebUI container (script
  defaults to `3000` in this branch).
- `FRONTEND_URL` — optional full URL (e.g. `http://localhost:3000`) that the
  desktop will open when the research stack is ready.

## Development

- Use `export PYTHONPATH=${PWD}/src` when running modules during development.
- Run unit tests with `pytest` from the repo root.

## Troubleshooting

- If the Research page shows an error when starting the stack, open a terminal
  and run `docker logs open-webui --tail 200` to inspect the container logs.
- If `.env` parsing fails (shell errors about `command not found`), ensure
  values with spaces are quoted, e.g. `APP_NAME="AI Stack"`.
- If the UI opens the wrong port, confirm `FRONTEND_URL` or `OPEN_WEBUI_PORT`
  in `.env` and restart the desktop.

## Contributing

PRs welcome. Keep changes small and focused; update tests where relevant.

## License

This repository currently has no attached license. Add a `LICENSE` file
before publishing or sharing publicly.
