#What it does: Main entry point of the copilot app.
#Logic used: Startup logic; usually bootstraps config, services, router, and UI.
#Interconnection: Calls config.py, may create service instances, and hands control to
#CLI/UI modules.

"""Module entry point: `python -m laptop_copilot.main`.

Thin wrapper around the CLI app so scripts/run-copilot.sh has a stable
target regardless of how the Typer app is structured.
"""
from laptop_copilot.ui.cli import app

if __name__ == "__main__":
    app()