# AI-Stack

> A local-first AI assistant for Linux laptops — chat, research, and safe desktop automation, all running on your own machine.

[![License](https://img.shields.io/badge/license-see%20LICENSE-lightgrey.svg)](./LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-blue.svg)](#requirements)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](#requirements)

`ai-stack` combines two complementary products in one repo:

| Product | What it does |
|---|---|
| **Research Workspace** | Open WebUI + Ollama for chat, model-driven research, and persistent workspace notes. |
| **Laptop Copilot** | A native Python agent (CLI + PySide6 desktop shell) for safe desktop actions, using a whitelist of tools. |

📚 See [`docs/`](./docs) for the PRD, architecture notes, and a longer setup guide.

---

## Table of contents

- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Environment variables](#environment-variables)
- [Project structure](#project-structure)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Requirements

- **OS:** Linux (development targeted at desktop Linux)
- **Python:** 3.10+ — use the provided `./scripts/setup.sh` to create a `.venv`
- **Docker:** required for the Open WebUI runtime
- **Ollama:** installed locally for research features

## Quick start

### 1. Configure your environment

```bash
cp .env.example .env
# edit .env if you want to change ports or model names
```

### 2. Bootstrap the project

```bash
./scripts/setup.sh
source .venv/bin/activate
export PYTHONPATH="${PWD}/src"
```

### 3. Start the components

Order is flexible — start whichever pieces you need:

```bash
./scripts/run-research-ui.sh   # starts Ollama + Open WebUI (Docker)
./scripts/run-copilot.sh       # CLI copilot / rofi entrypoint
./scripts/run-desktop.sh       # PySide6 desktop shell (Copilot / Research / Settings)
```

> **Note:** The desktop shell lives at `src/laptop_copilot/ui/desktop.py` and exposes three pages: **Copilot**, **Research**, and **Settings**.
>
> If your local Open WebUI frontend runs on a non-default port (e.g. `3000`), set `FRONTEND_URL` in `.env`, or `OPEN_WEBUI_PORT` to match — the UI prefers `FRONTEND_URL` when present.

## Environment variables

| Variable | Description |
|---|---|
| `RESEARCH_MODEL` | Model name pulled by the research script (default set in `.env.example`). |
| `OPEN_WEBUI_PORT` | Host port mapped to the Open WebUI container (defaults to `3000` on this branch). |
| `FRONTEND_URL` | Optional full URL (e.g. `http://localhost:3000`) the desktop shell opens once the research stack is ready. |

## Project structure

```
ai-stack/
├── config/                       # runtime config (logging, preferences, tool whitelist)
│   ├── logging.json
│   ├── preferences.json
│   └── tools.json
├── data/                         # local cache, memory, and notes storage
│   ├── cache/
│   ├── memory/
│   └── notes/
├── docs/                         # PRD, architecture, roadmap, setup guide
│   ├── architecture.md
│   ├── prd.md
│   ├── roadmap.md
│   └── setup.md
├── logs/
│   └── actions.jsonl             # copilot action log
├── models/                       # model config + recommendations
│   ├── controller-model.txt
│   ├── recommended-models.md
│   └── research-model.txt
├── research-ui/                  # Open WebUI / Ollama configuration
│   ├── env/                      # env templates for ollama + open-webui
│   ├── prompts/                  # system prompts (research, coding, summarizer)
│   └── workspace-notes/          # persistent research notes
├── resources/                    # desktop entry template + icon
│   ├── ai-stack.desktop.template
│   └── ai-stack.svg
├── scripts/                      # setup + run scripts
│   ├── setup.sh
│   ├── dev-reset.sh
│   ├── install-desktop.sh
│   ├── run-research-ui.sh
│   ├── run-copilot.sh
│   └── run-desktop.sh
├── src/
│   └── laptop_copilot/
│       ├── main.py
│       ├── config.py
│       ├── memory.py
│       ├── router.py
│       ├── tools.py
│       ├── integrations/         # clipboard, notifications, rofi, window control
│       ├── services/             # command runner, file service, notes, ollama client
│       └── ui/
│           ├── cli.py
│           ├── desktop.py        # PySide6 desktop shell
│           ├── status.py
│           └── pages/            # copilot / research / settings pages
├── tests/                        # pytest unit tests
├── .env.example
├── LICENSE
├── pyproject.toml
└── README.md
```

## Development

```bash
export PYTHONPATH="${PWD}/src"
pytest
```

Run unit tests with `pytest` from the repo root.

## Troubleshooting

<details>
<summary><strong>Research page shows an error when starting the stack</strong></summary>

Open a terminal and inspect the container logs:

```bash
docker logs open-webui --tail 200
```
</details>

<details>
<summary><strong>.env parsing fails ("command not found" errors)</strong></summary>

Make sure values containing spaces are quoted:

```bash
APP_NAME="AI Stack"
```
</details>

<details>
<summary><strong>UI opens the wrong port</strong></summary>

Confirm `FRONTEND_URL` or `OPEN_WEBUI_PORT` in `.env`, then restart the desktop shell.
</details>

## Contributing

PRs welcome! Please:

- Keep changes small and focused
- Update or add tests where relevant
- Describe the "why" in your PR description, not just the "what"

## License

See [`LICENSE`](./LICENSE) for details.
