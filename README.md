# Todo App

A typed Python CLI application for managing tasks from an interactive terminal interface.

This project is intentionally small, but it is structured like a maintainable production codebase: domain logic is separated from CLI workflows, persistence is isolated behind a state layer, data contracts are typed, and the code is covered by automated quality checks.

## Why This Project Exists

Todo App is a portfolio project focused on clean Python application architecture, not on UI complexity.

It demonstrates:

- domain-driven modeling with `Task` and `TaskList`
- clear separation between domain, CLI, UI, schemas, and persistence
- JSON serialization and runtime data validation
- interactive terminal workflows with Typer, Questionary, and Rich
- testable command handlers with mocked prompts and state
- strict tooling with Ruff, pytest, coverage, and ty

## Features

- Add new tasks interactively
- List tasks in a formatted terminal table
- Update task fields
- Remove tasks by list number
- Store tasks in a local JSON file
- Validate task descriptions, deadlines, IDs, tags, and serialized data
- Filter and sort task collections at the domain level
- Serialize and restore tasks from dictionaries and JSON

## Tech Stack

| Area | Tool |
| --- | --- |
| Language | Python 3.13 |
| CLI | Typer |
| Prompts | Questionary |
| Terminal output | Rich |
| Package manager | uv |
| Tests | pytest |
| Linting / formatting | Ruff |
| Type checking | ty |
| Git hooks | pre-commit |

## Architecture

The project is split into small layers with clear responsibilities:

```text
src/
|-- cli/          # command handlers, app state, command registration
|-- enums/        # status and priority enums
|-- schemas/      # typed JSON contracts and runtime guards
|-- task/         # Task domain model
|-- task_list/    # TaskList collection model
`-- ui/           # prompts, console output, table rendering
```

### Core Design Decisions

- `Task` owns validation rules such as description length, deadline validity, UUID handling, tag normalization, and completion timestamps.
- `TaskList` owns collection behavior such as uniqueness, filtering, sorting, lookup, and serialization.
- CLI commands orchestrate workflows but do not own business rules.
- Storage is file-based and configured through an environment variable.
- Tests isolate interactive flows by monkeypatching prompts and persistence functions.

## Quick Start

Install dependencies:

```powershell
uv sync
```

Create a local storage file:

```powershell
New-Item -ItemType Directory -Force .\temp
'{"tasks": []}' | Set-Content -Encoding utf8 .\temp\todo_list.json
```

Configure the storage path:

```powershell
$env:STORAGE_PATH_ENV = "$PWD\temp\todo_list.json"
```

Run the application:

```powershell
uv run python main.py
```

## Usage

After starting the app, choose an action from the interactive menu:

```text
Show tasks
Add task
Update task
Remove task
Exit
```

When adding or updating a task, the app prompts for fields such as:

- description
- status
- priority
- deadline
- tags

## Storage Format

The app stores data in a JSON file with this top-level structure:

```json
{
  "tasks": []
}
```

Example task:

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

## Development

Run tests:

```powershell
uv run pytest
```

Run linting:

```powershell
uv run ruff check src tests
```

Format code:

```powershell
uv run ruff format
```

Run type checking:

```powershell
uv run ty check
```

## Quality

The repository is configured with:

- strict linting and formatting through Ruff
- type checking through ty
- automated tests with pytest
- coverage configuration
- pre-commit hooks for local quality gates
- docstrings in production code

## Project Structure

```text
todo_app/
|-- main.py
|-- pyproject.toml
|-- pytest.toml
|-- ruff.toml
|-- src/
|   |-- cli/
|   |-- enums/
|   |-- schemas/
|   |-- task/
|   |-- task_list/
|   `-- ui/
`-- tests/
    |-- cli/
    |-- schemas/
    |-- task/
    |-- task_list/
    `-- ui/
```

## Notes

- This is a local CLI application, not a web app.
- The storage file must exist before running the app.
- `STORAGE_PATH_ENV` must point to a valid JSON storage file.
- The project favors explicit, testable Python over framework-heavy architecture.

## Next Improvements

- Add a packaged console command such as `todo-app`
- Add non-interactive CLI commands for scripting
- Add a storage initialization command
- Add structured logging
- Add schema versioning for stored JSON data
- Consider SQLite for safer persistence if concurrent access becomes important
