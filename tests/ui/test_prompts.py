from datetime import UTC, date, datetime, timedelta

import pytest
from questionary import Style

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.ui.prompts import prompt_deadline, prompt_description, prompt_menu, prompt_priority, prompt_status, prompt_tags
from tests.conftest import FixedDatetime


class DummySelect:
    def __init__(self, message: str | None) -> None:
        self.message = message

    def ask(self) -> str | None:
        return self.message


def test_prompt_description(monkeypatch: pytest.MonkeyPatch) -> None:

    values = iter(["ab", "a", "valid"])

    def stub_prompt(text: str) -> str:
        return next(values)

    monkeypatch.setattr("src.ui.prompts.typer.prompt", stub_prompt)
    result = prompt_description()

    assert result == "valid"


def test_prompt_status(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr("src.ui.prompts.select", lambda *_, **__: DummySelect("In Progress"))

    result = prompt_status()

    assert result == StatusEnum("in progress")


def test_prompt_priority(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr("src.ui.prompts.select", lambda *_, **__: DummySelect("Low"))

    result = prompt_priority()

    assert result == PriorityEnum.LOW


def test_prompt_deadline_no_deadline(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr("src.ui.prompts.select", lambda *_, **__: DummySelect("No deadline"))

    assert prompt_deadline() is None


def test_prompt_deadline_today(fixed_datetime: type[FixedDatetime], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.ui.prompts.select", lambda *_, **__: DummySelect("Today"))
    monkeypatch.setattr("src.ui.prompts.datetime", fixed_datetime)

    assert prompt_deadline() == datetime(2025, 12, 4, tzinfo=UTC).date()


def test_prompt_deadline_tomorrow(fixed_datetime: type[FixedDatetime], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.ui.prompts.select", lambda *_, **__: DummySelect("Tomorrow"))
    monkeypatch.setattr("src.ui.prompts.datetime", fixed_datetime)

    assert prompt_deadline() == datetime(2025, 12, 4, tzinfo=UTC).date() + timedelta(days=1)


def test_prompt_deadline_7_days(fixed_datetime: type[FixedDatetime], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.ui.prompts.select", lambda *_, **__: DummySelect("In 7 days"))
    monkeypatch.setattr("src.ui.prompts.datetime", fixed_datetime)

    assert prompt_deadline() == datetime(2025, 12, 4, tzinfo=UTC).date() + timedelta(days=7)


def test_prompt_deadline_14_days(fixed_datetime: type[FixedDatetime], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.ui.prompts.select", lambda *_, **__: DummySelect("In 14 days"))
    monkeypatch.setattr("src.ui.prompts.datetime", fixed_datetime)

    assert prompt_deadline() == datetime(2025, 12, 4, tzinfo=UTC).date() + timedelta(days=14)


def test_prompt_deadline_exact_day(fixed_datetime: type[FixedDatetime], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.ui.prompts.select", lambda *_, **__: DummySelect("Pick exact day (YYYY-MM-DD)"))
    monkeypatch.setattr("src.ui.prompts.datetime", fixed_datetime)
    monkeypatch.setattr("src.ui.prompts.typer.prompt", lambda *_, **__: "2025-12-31")

    assert prompt_deadline() == date(2025, 12, 31)


def test_prompt_deadline_manual_retry(fixed_datetime: type[FixedDatetime], monkeypatch: pytest.MonkeyPatch) -> None:

    values = iter(["bad", "2025-11-30", "2026-06-12"])

    def stub_prompt(text: str) -> str:
        return next(values)

    monkeypatch.setattr("src.ui.prompts.datetime", fixed_datetime)
    monkeypatch.setattr("src.ui.prompts.select", lambda *_, **__: DummySelect("Pick exact day (YYYY-MM-DD)"))
    monkeypatch.setattr("src.ui.prompts.typer.prompt", stub_prompt)
    monkeypatch.setattr("src.ui.prompts.typer.echo", lambda _: None)

    assert prompt_deadline() == date(2026, 6, 12)


def test_prompt_tags(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr("src.ui.prompts.typer.prompt", lambda *_, **__: "tag1, tag2, tag3")
    result = prompt_tags()

    assert result == ["tag1", "tag2", "tag3"]


def test_prompt_tags_empty(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr("src.ui.prompts.typer.prompt", lambda *_, **__: "")
    result = prompt_tags()

    assert result == []


def test_prompt_menu(monkeypatch: pytest.MonkeyPatch) -> None:

    captured = {}

    def spy_select(message: str, *, choices: list[str], style: Style) -> DummySelect:
        captured["message"] = message
        captured["choices"] = choices
        captured["style"] = style

        return DummySelect("Task description")

    monkeypatch.setattr("src.ui.prompts.select", spy_select)

    result = prompt_menu(["Task description", "Status"])

    assert result == "Task description"
    assert captured["message"] == "Menu"
    assert captured["choices"] == ["Task description", "Status"]
