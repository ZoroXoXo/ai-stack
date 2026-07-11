<!-- What a product should do -->
<!-- Influences what modules exist in /src -->

# Product Requirements Document: Local AI Research Workspace and Laptop Copilot

## Overview

This project is a local-first AI assistant system built for a Linux laptop
environment. It consists of two connected but separate products: a research
workspace for learning, note-taking, and web-assisted exploration, and a
lightweight laptop copilot for safe device actions such as opening apps,
creating notes, checking recent files, and handling simple desktop workflows.

The system is designed around local model execution with Ollama, a richer UI
layer for research tasks, and a smaller controller layer for desktop
automation. This split keeps the research experience capable while keeping
the system-control layer fast, resource-light, and safer to operate.

## Problem Statement

Terminal-only local model usage is powerful but inconvenient for day-to-day
student and productivity workflows. A usable AI system for laptop life needs
a proper interface with chat history, organization, workspace separation, and
search-friendly conversation management rather than a raw command-line-only
experience.

At the same time, laptop control tasks have different needs from research
chat. Desktop actions need predictable latency, low idle resource usage, and
strict tool boundaries, while learning and research tasks benefit from richer
context, larger prompts, and workspace-oriented UX.

## Product Vision

Create a private, local-first AI stack that feels like a proper app instead
of a terminal tool. The final experience should let a user switch between a
research assistant with organized workspaces and a quick-action laptop
copilot that handles everyday tasks through a minimal native interface.

The system should be practical for a student or builder using Linux,
affordable to run on existing hardware, and extendable into a
portfolio-grade desktop project. Open WebUI already provides a strong base
for the research side, while Tauri offers a path to packaging a custom
desktop experience later.

## Goals

- Provide a polished local AI interface for study, research, notes, and
  web-assisted exploration.
- Support chat history, search, workspace separation, prompt presets, and
  model switching in the research interface.
- Provide a lightweight local copilot for laptop actions such as launching
  apps, opening recent files, creating notes, and checking simple system
  context.
- Keep the system local-first, with Ollama as the model runtime and optional
  web access only where explicitly useful.
- Preserve privacy by preferring on-device execution and minimizing
  dependency on paid cloud inference.
- Create a project that can be documented on GitHub and presented as a
  resume-quality systems and AI integration build.

## Non-Goals

- Building a fully autonomous, unrestricted agent that can run arbitrary
  shell commands without guardrails.
- Replacing the operating system's native security model.
- Delivering a mobile app in the first version.
- Achieving frontier-model reasoning on-device; the system is optimized for
  practical local usefulness rather than maximum benchmark performance.

## Target User

The primary user is a technically advanced student or maker who uses Linux
heavily, prefers local tools, and wants one AI system for learning workflows
and another for low-friction device assistance. The user values
customization, privacy, and resource efficiency more than glossy
cloud-only features.

## Product Scope

### Product A: Research Workspace

Handles learning, reading, question answering, summarization, web-assisted
research, and organized ongoing conversations. Presents as a proper
interface with persistent history, search, and workspace-like organization.

Open WebUI is an appropriate first implementation because it is designed as
a self-hosted AI interface that supports Ollama and other OpenAI-compatible
APIs, and its feature set already includes conversation history, search, and
broader chat-management functionality.

### Product B: Laptop Copilot

Handles small desktop actions through a lightweight native UI or daemon. It
should wake quickly, consume minimal resources, and route user intent into a
fixed set of approved tools such as opening applications, capturing notes,
retrieving recent files, and showing simple device information.

Should not depend on a browser-first workflow. A native helper implemented
first as a Python daemon and later optionally packaged or reimplemented in
Tauri or Rust better matches the low-latency system-integration goal.

## Functional Requirements

### Research Workspace Requirements

1. The system shall run local models through Ollama.
2. The system shall provide a graphical interface for chatting with local
   models.
3. The interface shall support conversation history and history search.
4. The interface shall support organization features such as workspaces,
   prompts, or equivalent grouping methods for distinct user contexts.
5. The interface shall support switching between multiple local models.
6. The interface shall support optional web-assisted research features
   where configured.
7. The interface should support file or note attachment workflows for study
   materials where available in the selected UI.

### Laptop Copilot Requirements

1. The system shall expose a quick-access UI through hotkey, tray, launcher,
   or a similar native entry point.
2. The copilot shall support a fixed set of safe actions in version 1.
3. The copilot shall interpret natural-language requests into action intents
   using either a very small model or rule-based routing.
4. The copilot shall execute only whitelisted tools and scripts.
5. The copilot shall log action history for transparency and debugging.
6. The copilot shall support at least the following actions in the first
   release:
   - Open application.
   - Create quick note.
   - Show recent files.
   - Open last downloaded or last used file.
   - Open calendar view or calendar application.
   - Show clipboard contents or search clipboard text.
   - Show basic device state such as battery or network status.
7. The copilot should be usable without the research workspace being open.

## User Stories

### Research Workspace

- As a student, I want to ask questions in a proper app with history so
  earlier explanations are easy to revisit.
- As a learner, I want separate workspaces for subjects such as college,
  Linux, and project ideas so conversations do not mix.
- As a privacy-conscious user, I want local models instead of depending
  entirely on paid cloud tools.
- As a builder, I want to switch models depending on speed, quality, or task
  type.

### Laptop Copilot

- As a power user, I want to wake a small assistant quickly and ask it to
  open an app or file without typing long commands.
- As a multitasker, I want to create and retrieve quick notes without
  switching context.
- As a Linux user, I want recent-file and launcher actions to integrate
  with desktop workflows.
- As a cautious user, I want the assistant to act only through approved
  tools rather than unrestricted shell execution.

## Recommended Technical Stack

| Layer | Recommendation | Reason |
|---|---|---|
| Model runtime | Ollama / ollama-cuda | Local model execution with Linux support and GPU path. |
| Research UI | Open WebUI | Fastest path to a usable interface with rich chat features. |
| Research API compatibility | Ollama OpenAI-compatible endpoints | Makes custom frontend integration easier. |
| Controller runtime | Python first, Rust later | Fast iteration first; optimize later. |
| Desktop packaging | Tauri | Small desktop-app path for later custom packaging. |
| Optional containerization | Docker for Open WebUI only | Useful for easy setup and isolation without forcing containerization everywhere. |

## Model Strategy

The project should use a two-model strategy instead of forcing one model to
do every job. The research workspace should use a small-to-medium model with
better context handling and instruction following, while the controller
should use an ultra-light model only if natural-language intent parsing is
necessary.

A suitable first research model is Phi-3.5 Mini, which NVIDIA describes as a
3.8B-parameter model in its RTX-oriented quantized form — a reasonable
starting point for efficient long-context local use without moving directly
to heavier models.

The controller should start with no model or a very small model, because
predictable actions matter more than generative fluency for desktop control.
In version 1, rule-based routing plus a small intent parser is preferable to
a fully agentic design.

## UX Requirements

### Research Workspace UX

- Clean app-like interface with dark mode support if available.
- Sidebar or equivalent structure for chat history and topic grouping.
- Fast model switcher.
- Clear prompt area for long study questions.
- Searchable history and easy revisit of previous sessions.

### Laptop Copilot UX

- Invoked in one action through hotkey, launcher, or tray icon.
- Minimal window or floating panel.
- Action confirmation for sensitive operations.
- Fast display of recent actions.
- Human-readable feedback after a command runs.

## Safety and Guardrails

The laptop copilot must not be allowed to execute arbitrary free-form
commands from model output. Instead, all executable actions should be
mediated through whitelisted scripts, structured tool definitions, and
optional confirmation prompts for sensitive tasks.

Recommended guardrails:

- Tool whitelist in JSON or config file.
- Argument validation.
- Confirmation prompt for delete, move, or overwrite operations.
- Persistent action logs.
- Separate permissions for read-only versus write actions.

## Architecture — High-Level Flow

1. Ollama runs locally as the model backend.
2. Open WebUI connects to Ollama for the research assistant experience.
3. A separate native copilot process receives local commands through
   hotkey, popup, or launcher.
4. The copilot maps requests to approved tools and scripts.
5. Optional later version: a Tauri shell unifies the experience into a
   branded desktop app.

## Deployment Modes

| Component | Preferred mode | Alternate mode |
|---|---|---|
| Ollama | Native Arch install | Docker if specifically desired |
| Open WebUI | Docker or local install | Desktop app where supported |
| Copilot | Native daemon | Tauri-packaged desktop helper |

## Milestones

**Milestone 1: Foundation**
- Install Ollama. Pull first local model.
- Install and connect Open WebUI.
- Confirm local chat works end to end.

**Milestone 2: Research Workflow**
- Create separate subject workspaces.
- Save prompt presets.
- Test history and retrieval of prior chats.

**Milestone 3: Copilot MVP**
- Build daemon or background helper.
- Add first five safe actions.
- Add logs and confirmations.
- Add launcher or hotkey entry point.

**Milestone 4: Daily-Use Build**
- Add recent-file logic.
- Add note capture and retrieval.
- Add calendar opener or read-only calendar integration.
- Improve performance and startup behavior.

**Milestone 5: Productization**
- Add custom branding.
- Package with Tauri.
- Publish GitHub documentation and demo assets.

## Success Metrics

### Research Workspace Metrics

- User can install and launch the workspace in under one hour on the target
  laptop.
- User can maintain separate chat contexts for at least three ongoing
  topics.
- User can retrieve previous chat content through history search
  successfully.
- Local response quality is sufficient for study, summarization, and
  exploratory research tasks.

### Laptop Copilot Metrics

- Hotkey-to-usable-interface time is under two seconds on the target
  machine.
- At least 90 percent of fixed commands succeed when called with supported
  phrasing.
- Idle resource usage remains low enough that the copilot can stay
  available in the background.
- No unrestricted command execution path exists in version 1.

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Small models may be weak for deeper reasoning | Medium | Keep research mode separate; allow later model upgrades. |
| Copilot may become unsafe if given too much freedom | High | Whitelist actions only; add confirmations and logs. |
| Too many features may delay delivery | High | Ship two narrow MVPs before attempting a unified "Jarvis" experience. |
| Desktop integration bugs on Linux | Medium | Start with simple scripts and i3-friendly launch methods before deeper integration. |
| Resource contention between workspace and controller | Medium | Keep controller small; use larger model only on demand. |

## Estimated Timeline

A working local research setup can be operational very quickly — Open
WebUI's getting-started flow says the first AI conversation can be reached
in under five minutes — while the larger time investment comes from
controller design, integration, and polish.

A realistic delivery plan is:

- 1 day for foundation setup.
- 2 to 4 days for research workflow tuning.
- 3 to 7 days for the first controller MVP.
- 1 to 3 additional weeks for polish, packaging, and better desktop
  integration.

## Open Questions

- Which exact desktop environment hooks should be targeted first for recent
  files and window management?
- Should calendar integration be read-only in version 1 or support event
  creation?
- Should voice wake be postponed until the text-first copilot is stable?
- Should the final branded product merge both surfaces into one shell, or
  keep research and control as separate apps?
- Which model should be the default controller parser after initial testing
  on the target laptop?

## Recommended Next Step

Implement Milestone 1 and Milestone 3 in parallel: set up Ollama plus Open
WebUI for immediate usability, and build a tiny native copilot that supports
only a handful of whitelisted actions. This approach creates a usable
product early while preserving a clear path to a more polished custom
desktop app later.