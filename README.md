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

todo_app is a portfolio project focused on clean Python application architecture rather than UI complexity.

The application runs entirely in the terminal. It stores tasks in a local JSON file and exposes an interactive menu built with Typer, Questionary, and Rich. There is no web server, no database, and no background process — just a well-structured Python codebase with strict quality gates.

The codebase demonstrates:

- **Domain-driven modeling** — `Task` and `TaskList` own all business rules and validation
- **Layered architecture** — domain, CLI, UI, schemas, and persistence are fully separated
- **Typed contracts** — `TypedDict` schemas with runtime guards for all serialized data
- **Testable design** — interactive workflows are tested by monkeypatching prompts and state functions
- **Strict tooling** — Ruff, ty, pytest, 100% branch coverage, pre-commit hooks

---

## Features

- Add, list, update, and remove tasks through an interactive terminal menu
- Rich table rendering with colour-coded status, priority, deadline, and tags
- Full JSON persistence — every change is saved immediately
- Automatic `completed_at` timestamp management on status transitions
- Tag normalization: lowercase, trimmed, deduplicated, order-preserved
- Deadline validation against task creation date
- UUIDv4 identity for every task
- Filter and sort task collections at the domain level

---

## Quick Start

**1. Clone and install**

```powershell
git clone https://github.com/rafalkrit/todo_app.git
cd todo_app
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
| `STORAGE_PATH_ENV` | yes | Absolute path to the JSON storage file. The file must exist and contain valid task-list JSON before running. |

If the variable is missing, empty, or points to an invalid file, the application fails at startup with a validation error.

---

## Usage

The application starts with an interactive menu:

```
❯ Show tasks
  Add task
  Update task
  Remove task
  Exit
```

### Show tasks

Renders all tasks in a Rich table:

```
 #   Description                  Status        Priority   Deadline
─────────────────────────────────────────────────────────────────────
 1   Prepare release checklist    in progress   HIGH       2026-05-20
 2   Review PR from @kacper       todo          MEDIUM     —
 3   Write unit tests for ui/     completed     LOW        —
 4   Fix deadline validation bug  blocked       HIGH       2026-05-15
```

### Add task

Prompts for each field in sequence:

| Field | Constraints |
|---|---|
| Description | 3–120 characters, required |
| Status | `todo` · `in progress` · `completed` · `blocked` |
| Priority | `LOW` · `MEDIUM` · `HIGH` |
| Deadline | none / today / tomorrow / +7 days / +14 days / exact `YYYY-MM-DD` |
| Tags | comma-separated, normalized automatically |

### Update task

Select a task by its visible number, then choose which field to edit. Changes are saved immediately after exiting the update submenu.

### Remove task

Select a task by its visible number. The task is removed by UUID and the file is saved.

---

## Data Model

### Storage format

```json
{
  "tasks": [
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
  ]
}
```

### Task fields

| Field | Type | Notes |
|---|---|---|
| `idx` | UUIDv4 | auto-generated if omitted |
| `description` | string | 3–120 characters, required |
| `status` | enum | `todo` · `in progress` · `completed` · `blocked` |
| `priority` | enum | `LOW=1` · `MEDIUM=2` · `HIGH=3` |
| `created_at` | datetime | UTC, set at creation |
| `deadline` | date · null | optional, must not predate `created_at` |
| `completed_at` | datetime · null | auto-set when status → `completed`, cleared otherwise |
| `tags` | list[str] | lowercase, trimmed, deduplicated, order-preserved |

---

## Architecture

```
src/
├── cli/
│   ├── commands/     # one module per user workflow: add, list, update, remove, exit
│   ├── registry.py   # registers command functions on the Typer app
│   └── state.py      # singleton TaskList — loads from and saves to JSON
├── enums/            # StatusEnum, PriorityEnum
├── schemas/          # TypedDict contracts (TaskDict, TaskListDict) + runtime guards
├── task/             # Task domain model
├── task_list/        # TaskList collection
└── ui/               # Rich table, Questionary prompts, console instance
```

### Layer responsibilities

| Layer | Owns |
|---|---|
| `task/` | Field validation, tag normalization, UUID parsing, deadline rules, `completed_at` logic, serialization |
| `task_list/` | Uniqueness, add/remove/get, filtering, sorting, iteration, serialization |
| `cli/commands/` | User-facing workflows — orchestrates domain and UI, no business logic |
| `cli/state.py` | Singleton `TaskList` instance, JSON load/save |
| `ui/` | All terminal output — Rich table, Questionary prompt wrappers, console |
| `schemas/` | `TypedDict` shapes for JSON structures, runtime type guards |

### Key design decisions

- **`Task` owns validation.** Description length, deadline rules, UUID handling, tag normalization, and `completed_at` transitions live in the domain model, not in CLI handlers.
- **`TaskList` owns collection behavior.** Filtering, sorting, uniqueness enforcement, and serialization are methods on `TaskList`, not utility functions scattered across the codebase.
- **CLI commands are thin.** They call domain methods and UI functions. They do not contain conditionals about business rules.
- **Storage is isolated.** `cli/state.py` is the only module that reads from or writes to the filesystem at runtime. Tests replace it entirely with `monkeypatch`.
- **Tests never touch real storage.** Every test that needs a file uses `tmp_path`. Every test that triggers a prompt uses `monkeypatch.setattr`.

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

### Running the quality checks

```powershell
uv run ruff format       # format all code
uv run ruff check        # lint and auto-fix
uv run ty check          # static type analysis
uv run pytest            # run full test suite with branch coverage
```

### Running tests

```powershell
# full suite
uv run pytest

# single module
uv run pytest tests/task/test_status.py -v

# with coverage report
uv run pytest --cov=src --cov-report=term-missing
```

### Pre-commit hooks

```powershell
uv run pre-commit install          # install hooks
uv run pre-commit run --all-files  # run manually on all files
```

Hooks run on every `git commit`: `ruff format`, `ruff check --fix`, `ty check`.
`pytest` runs on every `git push`.

### Quality requirements

- Branch coverage: **100%**
- `DeprecationWarning` and `FutureWarning` are treated as errors
- All imports must be sorted (enforced by Ruff `I001`)

---

## Testing Approach

Tests are organized to mirror the source tree:

```
tests/
├── cli/
│   ├── commands/   # one test module per command handler
│   └── test_state.py
├── schemas/        # TypedDict guard validation
├── task/           # Task domain: validation, serialization, status, deadline, tags
├── task_list/      # TaskList: add, remove, filter, sort, serialization
└── ui/             # prompt wrappers
```

Patterns used across the test suite:

- `monkeypatch.setattr` for all external dependencies (prompts, storage, datetime)
- Named inner spy functions that append to a `msgs` list for side-effect verification
- `iter` / `next` pattern for simulating sequential menu selections
- `tmp_path` fixture for all filesystem interactions
- Shared `task_1` – `task_4` fixtures reused across modules

---

## Project Structure

```
todo_app/
├── main.py
├── pyproject.toml
├── pytest.toml
├── ruff.toml
├── src/
│   ├── cli/
│   │   ├── commands/
│   │   │   ├── add_task.py
│   │   │   ├── flow_update.py
│   │   │   ├── interactive.py
│   │   │   ├── list_tasks.py
│   │   │   ├── print_task_summary.py
│   │   │   └── remove_task.py
│   │   ├── registry.py
│   │   └── state.py
│   ├── enums/
│   ├── schemas/
│   │   └── guards/
│   ├── task/
│   ├── task_list/
│   └── ui/
└── tests/
    ├── cli/
    │   └── commands/
    ├── schemas/
    ├── task/
    ├── task_list/
    └── ui/
```

---

## Known Limitations

- No protection against concurrent writes to the same JSON file
- No automatic creation of a missing storage file
- No migration mechanism for future JSON schema changes
- No non-interactive CLI subcommands yet
- No packaged console entry point

---

## Roadmap

- [ ] Non-interactive subcommands (`add`, `list`, `done`, `remove`, `update`)
- [ ] Packaged console entry point (`todo-app`)
- [ ] Storage initialization command (`init`)
- [ ] Structured logging
- [ ] JSON schema versioning and migrations
- [ ] CI pipeline (Ruff, ty, pytest, coverage)
- [ ] SQLite backend for concurrent access
- [ ] Release automation and changelog

---

## Contributing

This is a personal portfolio project, but feedback and suggestions are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and ensure all quality checks pass:
   ```powershell
   uv run pre-commit run --all-files
   uv run pytest
   ```
4. Open a pull request with a clear description of what changed and why

---

<sub>Built by <a href="https://github.com/stuntsxlc4">Rafal</a> · Python 3.13 · local-first</sub>