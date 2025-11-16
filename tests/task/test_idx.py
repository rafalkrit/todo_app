from uuid import UUID, uuid4

import pytest

from src.task.task import Task


def test_idx_with_default() -> None:
    task = Task("python", idx=None)
    assert isinstance(task.idx, UUID)


def test_idx_accepts_str() -> None:
    idx = "ebfb1c34-5a3e-475f-a809-31bfd02d8908"
    task = Task("python", idx=idx)
    assert task.idx == UUID(idx, version=4)


def test_idx_accepts_uuid() -> None:
    idx = uuid4()
    task = Task("python", idx=idx)
    assert task.idx == idx


def test_idx_invalid_str_raises() -> None:
    with pytest.raises(ValueError, match="badly formed hexadecimal UUID string"):
        _ = Task("python", idx="ninvo236")
