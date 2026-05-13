from collections.abc import Callable

from src.cli.commands.interactive import interactive
from src.cli.registry import register_commands


class FakeApp:
    def __init__(self) -> None:
        self.commands = []

    def command(self) -> Callable[[Callable[..., object]], Callable[..., object]]:
        def decorator(fn: Callable[..., object]) -> Callable[..., object]:
            self.commands.append(fn)
            return fn

        return decorator


def test_register_commands() -> None:
    app = FakeApp()

    register_commands(app)

    assert len(app.commands) == 1
    assert app.commands[0] is interactive
