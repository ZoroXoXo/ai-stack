<!-- how the system is organised -->
<!-- influences package boundaries like services/,integrations/,ui/>

<!-- should ideally describe why the model roles are separated (models/)-->
# Architecture

## System diagram (conceptual)

```
                        ┌───────────────────────────┐
                        │        Ollama              │
                        │  (local model runtime)     │
                        │  - research-model           │
                        │  - controller-model (opt.)  │
                        └─────────────┬─────────────┘
                                      │ OpenAI-compatible API
              ┌───────────────────────┼───────────────────────┐
              │                                                │
   ┌──────────▼───────────┐                       ┌────────────▼────────────┐
   │      Open WebUI        │                       │   laptop_copilot daemon  │
   │  (Research Workspace)  │                       │   (Laptop Copilot)       │
   │  - chat history/search │                       │   - router.py            │
   │  - workspaces/prompts  │                       │   - tools.py (whitelist) │
   │  - model switcher      │                       │   - memory.py            │
   │  - web-assisted search │                       │   - services/*           │
   └─────────────────────────┘                       │   - integrations/*       │
                                                      └────────────┬────────────┘
                                                                   │
                                                     ┌─────────────▼─────────────┐
                                                     │  Whitelisted OS actions     │
                                                     │  - launch app (rofi/dmenu)  │
                                                     │  - create/read note          │
                                                     │  - list recent files         │
                                                     │  - clipboard read/search     │
                                                     │  - battery/network status    │
                                                     │  - calendar open (read-only) │
                                                     └───────────────────────────┘
```

## Two-process split

The Research Workspace and the Laptop Copilot are **separate processes** that
happen to share one thing: the local Ollama runtime. They are not merged into
one app in v1, on purpose — see PRD non-goals and risks.

- **Research Workspace** (Open WebUI + Ollama) optimizes for capability:
  richer context, larger prompts, workspace/prompt organization, optional
  web search.
- **Laptop Copilot** (`laptop_copilot` daemon) optimizes for latency and
  safety: sub-2-second wake time, a fixed whitelist of tools, no free-form
  shell execution, confirmation prompts for destructive actions.

## Copilot internal flow

1. **Entry point** — hotkey / tray / launcher (`rofi`, a tray icon, or a
   keybinding in the window manager) invokes `laptop_copilot.ui.cli`.
2. **Router** (`router.py`) — takes the raw text request and maps it to an
   `Intent` (e.g. `open_app`, `create_note`, `show_recent_files`). In v1 this
   is rule/pattern based; a small model can be swapped in later via
   `CONTROLLER_MODEL` in `.env`.
3. **Tools** (`tools.py`) — holds the whitelist of executable actions, each
   with a name, argument schema, and a `requires_confirmation` flag. The
   router can only call tools that exist in this whitelist — there is no
   path from model/user text to an arbitrary shell command.
4. **Services** (`services/`) — the actual implementations: talking to
   Ollama (only used if a controller model is enabled), running whitelisted
   commands (`command_runner.py`), managing notes (`notes_service.py`), and
   reading file/recency info (`file_service.py`).
5. **Integrations** (`integrations/`) — thin wrappers around Linux-specific
   tools: `rofi` for the launcher UI, `notify-send` for notifications,
   clipboard access, and basic window control.
6. **Memory** (`memory.py`) — a small persistent store (JSON/SQLite) for
   action history/logs, used for the "action history for transparency and
   debugging" requirement.

## Guardrails (see PRD "Safety and Guardrails")

- `config/tools.json` is the single source of truth for what the copilot is
  *allowed* to do. Nothing outside this list is reachable.
- Every tool call is logged to `logs/` with timestamp, tool name, arguments,
  and result.
- Tools tagged `"write": true` in `tools.json` require confirmation unless
  `COPILOT_REQUIRE_CONFIRMATION=false` is explicitly set.
- No tool accepts raw shell strings from user/model text — arguments are
  validated against a schema per tool.

## Deployment

- **Ollama**: native install (preferred) for GPU access; Docker as an
  alternative.
- **Open WebUI**: Docker (simplest) or native/local install; a packaged
  desktop app where supported.
- **Copilot**: native Python daemon in v1; optional future Tauri-packaged
  desktop helper (see Milestone 5).