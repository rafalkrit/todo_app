from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from src.cli.commands.interactive import interactive


CommandFunction = Callable[..., object]


class CommandRegistrar(Protocol):
    """Minimal command registration interface used by the CLI registry."""

    def command(self) -> Callable[[CommandFunction], CommandFunction]:
        """Return a decorator that registers a CLI command."""


def register_commands(app: CommandRegistrar) -> None:
    """Register all CLI commands on the provided Typer application."""
    app.command()(interactive)
