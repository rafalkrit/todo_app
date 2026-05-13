import pytest
import typer

from src.cli.commands.interactive import exit_app, interactive


def test_exit_app(monkeypatch: pytest.MonkeyPatch) -> None:
    msgs = []

    def spy_print(msg: str) -> None:
        return msgs.append(msg)

    monkeypatch.setattr("src.cli.commands.interactive.console.print", spy_print)

    with pytest.raises(typer.Exit):
        exit_app()

    assert msgs[0] == "[dim]Bye 👋[/dim]"


def test_interactive_action(monkeypatch: pytest.MonkeyPatch) -> None:

    actions = iter(["Add task", "Exit"])
    add_task_called = {"called": False}

    def spy_add_task() -> None:
        add_task_called["called"] = True

    monkeypatch.setattr("src.cli.commands.interactive.add_task", spy_add_task)
    monkeypatch.setattr("src.cli.commands.interactive.prompt_menu", lambda _: next(actions))

    with pytest.raises(typer.Exit):
        interactive()

    assert add_task_called["called"] is True
