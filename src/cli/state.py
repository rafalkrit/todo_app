import os
from pathlib import Path

from src.task_list.task_list import TaskList


def get_storage_path() -> Path:
    """Return the configured task storage path.

    Raises:
        ValueError: If the STORAGE_PATH_ENV environment variable is missing.
    """
    configured_path: str | None = os.getenv("STORAGE_PATH_ENV")
    if not configured_path:
        raise ValueError("Data stogare is not configured.")
    return Path(configured_path).expanduser()


def load_todo_list() -> TaskList:
    """Load and validate the task list from configured JSON storage.

    Returns:
        TaskList: Deserialized task collection.

    Raises:
        ValueError: If storage is unreadable, empty, or structurally invalid.
    """
    storage_path = get_storage_path()
    try:
        raw = storage_path.read_text(encoding="utf-8")
    except OSError as e:
        raise ValueError("Data storage can not be read.") from e

    if not raw.strip():
        raise ValueError("Data storage is invalid.")

    try:
        return TaskList.from_json(raw)
    except (TypeError, ValueError) as e:
        raise ValueError("Invalid data storage.") from e


_task_list: TaskList | None = None


def save_task_list() -> None:
    """Persist the current in-memory task list to configured JSON storage."""
    storage_path = get_storage_path()
    storage_path.write_text(get_task_list().to_json(indent=4), encoding="utf-8")


def get_task_list() -> TaskList:
    """Return the cached task list, loading it from storage on first access."""
    global _task_list  # noqa: PLW0603

    if _task_list is None:
        _task_list = load_todo_list()
    return _task_list
