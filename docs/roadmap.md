<!-- what comes next -->
<!--  drives future work in tests/, src/, and research-ui/ -->

# Roadmap

Derived from PRD milestones. Check items off as they land.

## Milestone 1 — Foundation
- [ ] Install Ollama, pull first local model
- [ ] Install and connect Open WebUI
- [ ] Confirm local chat works end to end

## Milestone 2 — Research Workflow
- [ ] Create separate subject workspaces (college / Linux / project ideas)
- [ ] Save prompt presets (`research-ui/prompts/`)
- [ ] Test history search and retrieval of prior chats

## Milestone 3 — Copilot MVP
- [ ] Build daemon / background helper (`src/laptop_copilot`)
- [ ] Implement first five safe actions:
  - [ ] Open application
  - [ ] Create quick note
  - [ ] Show recent files
  - [ ] Open last downloaded/used file
  - [ ] Show battery/network status
- [ ] Add action logs (`memory.py` + `logs/`)
- [ ] Add confirmation prompts for sensitive actions
- [ ] Add launcher/hotkey entry point (rofi + WM binding)

## Milestone 4 — Daily-Use Build
- [ ] Recent-file logic refinement
- [ ] Note capture and retrieval polish
- [ ] Calendar opener (read-only) or calendar app launch
- [ ] Clipboard show/search
- [ ] Performance and startup-time improvements

## Milestone 5 — Productization
- [ ] Custom branding
- [ ] Tauri packaging for both surfaces (or a unified shell — TBD, see open
      questions in the PRD)
- [ ] GitHub documentation and demo assets (README, screenshots/GIFs, demo
      script)

## Estimated timeline

| Phase | Estimate |
|---|---|
| Foundation setup | 1 day |
| Research workflow tuning | 2–4 days |
| First controller MVP | 3–7 days |
| Polish, packaging, desktop integration | 1–3 weeks |