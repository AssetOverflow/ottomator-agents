"""Command line interface for interacting with the agent runtime."""

from __future__ import annotations

import asyncio
from typing import Optional

import typer

from ..agent.runtime import AgentRuntime
from ..logging.setup import configure_logging, get_logger

app = typer.Typer(add_completion=False)
configure_logging()
logger = get_logger(__name__)


@app.command()
def chat(message: Optional[str] = typer.Option(None, "-m", "--message", help="Message to send")) -> None:
    """Send a single message to the agent."""

    async def _run(text: str) -> None:
        runtime = AgentRuntime()
        response = await runtime.handle(text)
        typer.echo(response.message)
        typer.echo(f"Sources: {', '.join(response.sources)}")

    text = message or typer.prompt("Message")
    asyncio.run(_run(text))


if __name__ == "__main__":
    app()
