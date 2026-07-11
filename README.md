# AI Stack

> A local-first AI workspace for running Ollama models through a cleaner app experience instead of a terminal-only workflow.

![Status](https://img.shields.io/badge/status-early--development-blue)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey)
![Local%20LLM](https://img.shields.io/badge/runtime-Ollama-111111)
![License](https://img.shields.io/badge/license-MIT-green)

## What is this?

AI Stack is a personal project focused on turning local LLM usage into a practical desktop workflow. Instead of chatting with models only through the terminal, the goal is to build a cleaner interface for research, prompt workflows, file-aware tasks, and local AI experimentation. [web:473][web:497]

This repo is being built as a foundation for:
- a local chat and research app,
- a developer-friendly AI workspace,
- and a reusable base for future AI tools and portfolio projects. [cite:488]

## Why this exists

Using Ollama directly is powerful, but the default workflow can feel too raw for daily use. This project aims to make local AI feel closer to a real app: easier to launch, easier to extend, and better suited for actual laptop workflows. [web:473][web:495]

## Planned features

- Local chat UI for Ollama models
- Model selector and session management
- Prompt templates and reusable workflows
- Conversation history
- File-aware workflows
- Local configuration via `.env`
- Modular structure for backend and frontend growth

## Tech direction

- **Runtime:** Ollama
- **Backend:** Python
- **Frontend:** Open WebUI first, then a custom app UI
- **Version control:** Git + GitHub
- **Target environment:** Linux-first local development

## Quick start

### Clone the repo

```bash
git clone git@github.com:YOUR_USERNAME/ai-stack.git
cd ai-stack
```

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Create local environment config

```bash
cp .env.example .env
```

### Run Ollama

Make sure Ollama is installed and running locally before connecting any UI or backend services.

## Project structure

```text
ai-stack/
├── backend/
├── frontend/
├── data/
├── logs/
├── models/
├── .env.example
├── .gitignore
└── README.md
```

> The structure is intentionally minimal right now and will evolve as implementation begins.

## Status

This project is currently in the setup phase. The repository structure, documentation, and local development workflow are being prepared before the first working backend/UI integration. [web:497][web:484]

## Roadmap

- [x] Create repository structure
- [x] Add `.gitignore`
- [ ] Add `LICENSE`
- [ ] Add `.env.example`
- [ ] Set up backend scaffold
- [ ] Connect Ollama locally
- [ ] Build initial UI workflow
- [ ] Add conversation and prompt features
- [ ] Explore desktop packaging

## Development notes

Current focus:
- keeping the repo clean,
- documenting setup properly,
- and building a base that is easy to maintain and expand.

## Contributing

This is currently a personal project, but the repository is being organized with future collaboration in mind.

## License

This project is intended to use the MIT License. Add the full license text in the `LICENSE` file.