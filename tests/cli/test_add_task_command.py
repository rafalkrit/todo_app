from _pytest.monkeypatch import MonkeyPatch
from typer.testing import CliRunner

import src.cli.cli as cli_module
from src.task_list.task_list import TaskList


runner = CliRunner()


def test_add_task_command_adds_task(monkeypatch: MonkeyPatch) -> None:
    tasks = TaskList()
    monkeypatch.setattr(cli_module, "tasks", tasks)

    result = runner.invoke(cli_module.app, ["add-task", "Implement CLI add command"])

    assert result.exit_code == 0
    assert len(tasks) == 1
    assert tasks[0].description == "Implement CLI add command"
    assert "Task added:" in result.stdout


def test_add_task_command_returns_error_for_invalid_description(monkeypatch: MonkeyPatch) -> None:
    tasks = TaskList()
    monkeypatch.setattr(cli_module, "tasks", tasks)

    result = runner.invoke(cli_module.app, ["add-task", "ab"])

    assert result.exit_code == 1
    assert len(tasks) == 0
    assert "must be between 3 and 120 characters" in result.stdout
