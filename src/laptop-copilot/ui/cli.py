#What it does: Command-line interface for interacting with the app.
#Logic used: Input parsing and output formatting.
#Interconnection: Likely calls main.py or router.py

"""Command-line entry point for the laptop copilot.

Two modes:
  copilot "open firefox"        # one-shot request
  copilot                       # opens a rofi prompt (or falls back to stdin)
"""
from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console

from laptop_copilot import memory, router, tools
from laptop_copilot.config import settings
from laptop_copilot.integrations import rofi
from laptop_copilot.ui.status import format_result

app = typer.Typer(add_completion=False, help="Laptop Copilot — whitelisted local desktop actions.")
console = Console()


def _confirm(prompt_text: str) -> bool:
    return typer.confirm(prompt_text, default=False)


def handle_request(request_text: str, skip_confirmation: bool = False) -> None:
    settings.ensure_dirs()
    try:
        intent = router.route(request_text)
    except router.UnroutableRequest as e:
        console.print(f"[yellow]✗ Didn't understand that:[/yellow] {e}")
        console.print(f"Known actions: {', '.join(tools.list_tools())}")
        return

    tool = tools.get_tool(intent.tool_name)
    if tool is None:
        console.print(f"[red]✗ Internal error: unknown tool '{intent.tool_name}'[/red]")
        return

    confirmed: Optional[bool] = None
    if tool.write and settings.require_confirmation and not skip_confirmation:
        confirmed = _confirm(f"Run '{tool.name}' with {intent.args}?")
        if not confirmed:
            console.print("[yellow]Cancelled.[/yellow]")
            memory.log_action(tool.name, intent.args, ok=False, message="Cancelled by user", confirmed=False)
            return

    result = tool.handler(**intent.args)
    console.print(format_result(tool.name, result))
    memory.log_action(tool.name, intent.args, ok=result.ok, message=result.message, confirmed=confirmed)


@app.command()
def run(
    request: Optional[str] = typer.Argument(None, help="Natural-language request, e.g. 'open firefox'"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompts."),
):
    """Run a single copilot request. With no argument, opens a rofi prompt."""
    text = request
    if text is None:
        text = rofi.prompt("copilot")
        if text is None:
            text = typer.prompt("copilot")

    if not text or not text.strip():
        console.print("[yellow]Nothing entered.[/yellow]")
        raise typer.Exit(code=0)

    handle_request(text.strip(), skip_confirmation=yes)


@app.command()
def history(limit: int = 20):
    """Show recent copilot action history."""
    entries = memory.recent_actions(limit=limit)
    if not entries:
        console.print("No actions logged yet.")
        return
    for e in entries:
        icon = "✓" if e["ok"] else "✗"
        console.print(f"{icon} [{e['timestamp']}] {e['tool']} {e['args']} — {e['message']}")


@app.command()
def tools_list():
    """List all whitelisted tools."""
    for name in tools.list_tools():
        t = tools.get_tool(name)
        console.print(f"[bold]{name}[/bold]: {t.description}")


if __name__ == "__main__":
    app()