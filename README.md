# todo_app

A typed Python CLI application for managing tasks from an interactive terminal interface.

[![Python](https://img.shields.io/badge/python-3.13-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-package%20manager-blueviolet?style=flat-square)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/badge/ruff-linting-orange?style=flat-square)](https://docs.astral.sh/ruff/)
[![ty](https://img.shields.io/badge/ty-type%20checked-informational?style=flat-square)](https://github.com/astral-sh/ty)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=flat-square)](https://pre-commit.com/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?style=flat-square)](https://github.com/rafalkrit/todo_app)

---

## Overview

todo_app is a portfolio project focused on clean Python application architecture.

The codebase is intentionally small but structured like a maintainable production system:

- domain logic is fully separated from CLI and UI layers
- data contracts are typed with `TypedDict` and runtime guards
- interactive workflows are testable via monkeypatched prompts and state
- all code paths are covered by automated quality checks

---

## Features

- Add, list, update, and remove tasks from an interactive terminal menu
- Rich table rendering with status, priority, deadline, and tags
- Full JSON persistence via a configurable storage file
- Automatic `completed_at` management on status transitions
- Tag normalization: lowercase, trimmed, deduplicated, order-preserved
- Deadline validation against task creation date
- UUIDv4 identity for every task

---

## Quick Start

**1. Install dependencies**

```powershell
uv sync
```

**2. Create a storage file**

```powershell
New-Item -ItemType Directory -Force .\temp
'{"tasks": []}' | Set-Content -Encoding utf8 .\temp\todo_list.json
```

**3. Set the storage path**

```powershell
$env:STORAGE_PATH_ENV = "$PWD\temp\todo_list.json"
```

**4. Run**

```powershell
uv run python main.py
```

---

## Configuration

| Variable | Required | Description |
|---|---|---|
| `STORAGE_PATH_ENV` | yes | Absolute path to the JSON storage file. Must exist before running. |

---

## Usage

The application starts with an interactive menu:

**Add task** prompts for:

| Field | Constraints |
|---|---|
| Description | 3–120 characters |
| Status | `todo` · `in progress` · `completed` · `blocked` |
| Priority | `LOW` · `MEDIUM` · `HIGH` |
| Deadline | none / today / tomorrow / +7d / +14d / custom date |
| Tags | comma-separated, normalized automatically |

---

## Data Model

```json
{
  "description": "Prepare release checklist",
  "status": "in progress",
  "priority": 3,
  "created_at": "2026-05-13T08:00:00+00:00",
  "deadline": "2026-05-20",
  "completed_at": null,
  "tags": ["release", "ops"],
  "idx": "63614577-08fa-4049-8e23-267d6867517c"
}
```

| Field | Type | Notes |
|---|---|---|
| `idx` | UUIDv4 | auto-generated |
| `description` | string | 3–120 characters, required |
| `status` | enum | `todo` · `in progress` · `completed` · `blocked` |
| `priority` | enum | `LOW=1` · `MEDIUM=2` · `HIGH=3` |
| `created_at` | datetime | UTC, set at creation |
| `deadline` | date · null | must not predate `created_at` |
| `completed_at` | datetime · null | auto-set when status becomes `completed` |
| `tags` | list[str] | lowercase, trimmed, deduplicated |

---

## Architecture

**Key design decisions:**

- `Task` owns all field-level validation: description length, deadline rules, UUID parsing, tag normalization, completion timestamps.
- `TaskList` owns collection behavior: uniqueness, filtering, sorting, lookup, serialization.
- CLI commands orchestrate user workflows but contain no business logic.
- Storage is file-based, isolated behind a state module, and configured via environment variable.
- Tests patch prompts and storage functions via `monkeypatch` — no test touches the real filesystem except through `tmp_path`.

---

## Tech Stack

| Area | Tool |
|---|---|
| Language | Python 3.13 |
| CLI | [Typer](https://typer.tiangolo.com/) |
| Prompts | [Questionary](https://questionary.readthedocs.io/) |
| Terminal output | [Rich](https://rich.readthedocs.io/) |
| Package manager | [uv](https://docs.astral.sh/uv/) |
| Tests | [pytest](https://pytest.org/) + [pytest-cov](https://pytest-cov.readthedocs.io/) |
| Linting / formatting | [Ruff](https://docs.astral.sh/ruff/) |
| Type checking | [ty](https://github.com/astral-sh/ty) |
| Git hooks | [pre-commit](https://pre-commit.com/) |

---

## Development

```powershell
uv run ruff format       # format code
uv run ruff check        # lint
uv run ty check          # type check
uv run pytest            # run tests with coverage
```

Pre-commit hooks run `ruff format`, `ruff check`, and `ty check` on every commit.
`pytest` runs on push.

Branch coverage threshold: **100%**.
`DeprecationWarning` and `FutureWarning` are treated as errors.

---

## Project Structure

---

## Roadmap

- [ ] Non-interactive subcommands (`add`, `list`, `done`, `remove`, `update`)
- [ ] Packaged console entry point (`todo-app`)
- [ ] Storage initialization command (`init`)
- [ ] Structured logging
- [ ] JSON schema versioning and migrations
- [ ] CI pipeline (Ruff, ty, pytest, coverage)
- [ ] SQLite backend for concurrent access

---

## Notes

- This is a local CLI application. No web server, no database, no background process.
- The storage file must exist before running — the app does not create it automatically.
- The project favors explicit, testable code over framework-heavy architecture.

---

<sub>Built by <a href="https://github.com/stuntsxlc4">Rafal</a> · Python 3.13 · local-first</sub>