## Purpose

Quick, actionable guidance for AI coding agents working on this repo. Focus on the project's concrete architecture, data flow, developer workflows, and the small, discoverable conventions an agent should follow.

## Big picture (what this repo is)

- FastAPI-based Todo REST API. App entry: `app/main.py` which includes routers from `routers/todos.py`.
- Persistence is a simple JSON file at `app/data/db.json` manipulated by `app/services/file_service.py`.
- Data model: Pydantic `Todo` in `app/schemas/todo.py` (fields: `id`, `title`, `description`, `completed`).

## Key files to read first

- `app/main.py` — app instance and router inclusion. Also defines a basic `/` and `/health` endpoint.
- `app/routers/todos.py` — existing endpoints: `GET /todos`, `POST /todos`. Intended to include `GET/PUT/DELETE /todos/{id}` per README.
- `app/services/file_service.py` — `read_db()` and `write_db()`; handles file creation and safe reads.
- `app/schemas/todo.py` — Pydantic model. Use `model_dump()` or `dict()` when writing JSON.
- `app/data/db.json` — runtime data file (may be missing; `read_db()` returns `[]`).
- `tests/test_todos.py` — currently empty; tests are expected and the README describes pytest-based tests.

## Data flow & service boundaries

- HTTP handlers in `routers/*.py` call `services/file_service.py` to read/write the full dataset. There is no database layer or ORM. All operations load the whole list, mutate it, and write it back.
- read_db() returns a list of dicts or an empty list on error — code should assume empty list is valid state.

## Project-specific conventions and gotchas

- ID generation: current `POST /todos` uses `len(todos) + 1`. This is known to be fragile (README points this out). Preferred approach: compute `max([t['id'] for t in todos], default=0) + 1`.
- When constructing objects use the Pydantic `Todo` model and call `model_dump()` before writing to JSON. `routers/todos.py` already uses `new_todo.model_dump()` for writes.
- `write_db()` expects a `list` and will raise `ValueError` otherwise. Keep this contract.
- `read_db()` swallows JSON decode errors and returns `[]`. Tests or handlers that depend on error visibility should not rely on exceptions from `read_db()`.

## Error handling & HTTP conventions

- Use FastAPI `HTTPException(status_code=..., detail=...)` for 404s and similar responses when a resource is missing. README explicitly suggests this for missing todos.
- Response models are used in `@router.get(..., response_model=...)`. Keep response models consistent with `schemas.todo.Todo` where appropriate.

## Tests & developer workflows

- Run tests with `pytest` (see `README.md`). `tests/test_todos.py` is empty — new tests should use the FastAPI TestClient pattern or call the functions directly.
- Development server: `uvicorn app.main:app --reload` per README. Use `--port` if 8000 is occupied.

## Typical change examples (copyable intent)

- Implement GET /todos/{todo_id} (pattern to follow):
  - call `todos = read_db()`
  - find the dict with matching `id` (`next((t for t in todos if t['id'] == todo_id), None)`)
  - if not found raise `HTTPException(status_code=404, detail='Not found')`
  - return `Todo(**found)`

- Implement PUT /todos/{todo_id}:
  - accept `Todo` body
  - call `read_db()` and locate the item; update fields but preserve `id`
  - `write_db(updated_list)` and return the updated `Todo` instance

- Implement DELETE /todos/{todo_id}:
  - filter list to exclude the target id, `write_db()` the new list, return a small dict like `{"message": "deleted"}` or 204

## What to preserve when editing code

- Keep the JSON storage location: `app/data/db.json`. Tests and the app expect that path.
- Preserve `read_db()`/`write_db()` contracts (inputs/outputs). Prefer small, local changes to router logic; do not introduce new persistence layers without updating README/tests.

## Example lines to reference in PRs or suggestions

- POST id bug: `app/routers/todos.py` line that sets `id=len(todos) + 1` — recommend replacing with `max(...)+1`.
- Persistence helpers: `app/services/file_service.py` — use as authoritative I/O functions.

## When to ask the human

- If a change requires introducing external services (DB, cloud storage) — ask for guidance and a migration plan.
- If a change modifies the storage path or file format, ask for test and data migration expectations.

---
If anything here is unclear or you'd like additional examples (unit tests, TestClient examples, or an ID-migration helper), tell me which part and I will expand or iterate.
