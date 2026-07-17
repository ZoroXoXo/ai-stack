# ai-stack

A local-first AI assistant system for Linux laptops, made of two connected but
separate products:

- **Research Workspace** — a full chat interface (Open WebUI + Ollama) for
  learning, note-taking, and web-assisted research. Persistent history,
  workspace separation, prompt presets, model switching.
- **Laptop Copilot** — a small, fast native daemon for safe desktop actions:
  opening apps, creating notes, checking recent files, clipboard search,
  battery/network status. Whitelisted tools only — no free-form shell
  execution.

See [`docs/prd.md`](docs/prd.md) for the full product requirements,
[`docs/architecture.md`](docs/architecture.md) for the system design, and
[`docs/setup.md`](docs/setup.md) to get running.

## Quick start

```bash
cp .env.example .env
./scripts/setup.sh
./scripts/run-research-ui.sh   # Ollama + Open WebUI
./scripts/run-copilot.sh       # laptop copilot (CLI / rofi entry point)
./scripts/run-desktop.sh       # PySide6 desktop shell (Copilot/Research/Settings)
```

The desktop shell (`src/laptop_copilot/ui/desktop.py`) is a `QMainWindow`
with a sidebar and three stacked pages:

- **Copilot** — the same router → whitelisted tools → action-log pipeline
  used by the CLI, in a text-in/results-out panel with a live history list.
- **Research** — starts `scripts/run-research-ui.sh` (Ollama + Open WebUI)
  and opens the workspace in your browser; the research experience itself
  stays in Open WebUI rather than being reimplemented in Qt.
- **Settings** — live Ollama reachability/model check, plus a read-only view
  of the active tool whitelist (`config/tools.json`).

## Layout

```
ai-stack/
├── docs/            PRD, architecture, setup, roadmap
├── research-ui/     prompts, workspace notes, env templates for Open WebUI
├── models/          model choice notes for research + controller
├── scripts/         setup and run scripts
├── src/laptop_copilot/  the copilot daemon + PySide6 desktop shell (Python)
├── config/          tool whitelist, preferences, logging config
├── data/            notes, memory, cache (gitignored contents)
├── logs/            runtime logs (gitignored contents)
└── tests/           unit tests for the copilot
```

## Status

Early scaffold — Milestone 1 (foundation) and Milestone 3 (copilot MVP) in
progress. See [`docs/roadmap.md`](docs/roadmap.md).

## License

Personal / portfolio project — add a license before publishing publicly.