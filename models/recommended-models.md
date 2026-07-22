<!-- explains model trade-offs and choices -->
# Recommended Models

## Research model (Product A)

Default: **Phi-3.5 Mini** (`phi3.5:3.8b-mini-instruct-q4_K_M`)

- ~3.8B parameters, quantized for RTX-class GPUs; good instruction-following
  and context handling for its size.
- Good starting point for study/summarization/exploratory research without
  jumping straight to a heavier (7B+) model.
- Note: this tag may not support Ollama tools in some Ollama/Open WebUI
  configurations. If you need tool support, choose a compatible model and
  set `RESEARCH_MODEL` in `.env`.

Upgrade paths if hardware allows:

- `qwen2.5:7b-instruct` — stronger reasoning, higher VRAM/RAM need.
- `llama3.1:8b-instruct` — solid general-purpose alternative.
- `mistral:7b-instruct` — fast, decent quality, widely used baseline.

Pick based on available VRAM and desired context length; keep the smaller
model as a fast fallback for quick questions.

## Controller model (Product B)

Default: **none** — rule-based routing in v1 (see PRD: "predictable actions
matter more than generative fluency for desktop control").

If natural-language intent parsing becomes necessary:

- `qwen2.5:1.5b-instruct` or `llama3.2:1b` — small enough to keep the
  copilot's wake-to-response time under ~2 seconds on modest hardware.
- Constrain output to a fixed intent schema (JSON) rather than free text —
  see `router.py` for the intent contract.

## Notes

- Always confirm actual quantized tag names against what's currently
  published for your Ollama version before pulling — tags change over time.
- Track real-world speed/quality observations in
  `research-ui/workspace-notes/model-notes.md`.