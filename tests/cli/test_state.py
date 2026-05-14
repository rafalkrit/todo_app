from pathlib import Path
import re

import pytest

from src.cli.state import get_storage_path, get_task_list, load_todo_list, save_task_list
from src.task_list.task_list import TaskList


def test_get_storage_path(monkeypatch: pytest.MonkeyPatch, tmp_file: Path) -> None:
    monkeypatch.setenv("STORAGE_PATH_ENV", str(tmp_file))

    path = get_storage_path()
    assert path == tmp_file


def test_get_storage_path_raises_when_missing_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("STORAGE_PATH_ENV", raising=False)

    with pytest.raises(ValueError, match=re.escape("Data stogare is not configured.")):
        get_storage_path()


def test_load_todo_list_read_error(monkeypatch: pytest.MonkeyPatch, tmp_file: Path) -> None:
    monkeypatch.setenv("STORAGE_PATH_ENV", str(tmp_file))

    with pytest.raises(ValueError, match=re.escape("Data storage can not be read.")):
        load_todo_list()


def test_load_todo_list_empty_file(monkeypatch: pytest.MonkeyPatch, tmp_file: Path) -> None:

    tmp_file.write_text("  ", encoding="utf-8")

    monkeypatch.setenv("STORAGE_PATH_ENV", str(tmp_file))

    with pytest.raises(ValueError, match=re.escape("Data storage is invalid.")):
        load_todo_list()


def test_load_todo_list_invalid_json(monkeypatch: pytest.MonkeyPatch, tmp_file: Path) -> None:
    tmp_file.write_text("error", encoding="utf-8")

    monkeypatch.setenv("STORAGE_PATH_ENV", str(tmp_file))

    with pytest.raises(ValueError, match=re.escape("Invalid data storage.")):
        load_todo_list()


def test_load_todo_list_success(monkeypatch: pytest.MonkeyPatch, tmp_file: Path) -> None:

    tmp_file.write_text('{"tasks": []}', encoding="utf-8")

    monkeypatch.setenv("STORAGE_PATH_ENV", str(tmp_file))

    task_list = load_todo_list()

    assert isinstance(task_list, TaskList)


def test_save_task_list_writes_file(monkeypatch: pytest.MonkeyPatch, tmp_file: Path) -> None:
    tmp_file.write_text('{"tasks": []}', encoding="utf-8")
    monkeypatch.setenv("STORAGE_PATH_ENV", str(tmp_file))

    task_list = get_task_list()

    json_before = task_list.to_json(indent=4)

    save_task_list()

    content = tmp_file.read_text(encoding="utf-8")
    assert content == json_before
