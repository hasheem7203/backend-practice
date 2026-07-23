# Week 3 — Postgres in Docker + Repository Swap

## What this is
The Week 2 Task API (FastAPI, in-memory storage) now runs against a real
Postgres database in Docker, with the whole stack (app + db) started by a
single `docker compose up`.

## Architecture
The service and route logic from Week 2 were **not changed**. The only
thing that changed is which repository gets injected into the service:

```python
REPOSITORY_TYPE = os.getenv("REPOSITORY_TYPE", "memory")
repository = PostgresTaskRepository() if REPOSITORY_TYPE == "postgres" else InMemoryTaskRepository()
service = TaskService(repository)
```

Both `InMemoryTaskRepository` and `PostgresTaskRepository` implement the
same abstract interface (`app/repository.py`): `get_all`, `get_by_id`,
`create`, `update`, `delete`. `TaskService` and every route in `main.py`
call only these methods and have zero knowledge of what's underneath —
proving the storage swap really is a one-file change.

## Running it

```powershell
cd week3
docker compose up --build
```

This starts:
- `db` — Postgres 16, with a named volume (`pgdata`) so data survives
  container restarts, and `init.sql` auto-run on first startup to create
  the `tasks` table.
- `app` — the FastAPI app, waiting for `db` to report healthy before
  starting (via `depends_on: condition: service_healthy`).

API available at `http://localhost:8000/tasks`.
Postgres is reachable from the host at `localhost:5433` (mapped off the
container's internal `5432`, to avoid clashing with a native Postgres
install already using 5432 on this machine).

## Configuration
Connection info lives in `.env` (gitignored). `.env.example` is committed
with the same keys and placeholder values so anyone cloning the repo
knows what to set.

## Proving persistence
Steps actually run to verify this:

1. Started the stack: `docker compose up --build`
2. Created a task via the API:
   ```powershell
   Invoke-RestMethod -Uri http://localhost:8000/tasks -Method Post -ContentType "application/json" -Body '{"title": "persistence check"}'
   ```
3. Confirmed it existed directly in Postgres (bypassing the app):
   ```powershell
   docker compose exec db psql -U taskuser -d taskdb -c "SELECT * FROM tasks;"
   ```
4. Fully tore down the stack: `docker compose down` (removes containers,
   keeps the named volume)
5. Brought it back up: `docker compose up`
6. Re-ran both the API GET and the direct `psql` query — the row
   (`id: 1, "persistence check"`) was still present in both, confirming
   data survived a full container + app restart because it lives in the
   `pgdata` volume, not inside the disposable container.

## A bug hit along the way (kept here honestly, per assignment instructions)
`.env` initially had `REPOSITORY_TYPE=postgresql`, but the check in
`main.py` compares against the string `"postgres"`. That mismatch meant
the app silently fell back to `InMemoryTaskRepository` for a while —
tasks appeared to "work" through the API but never showed up in direct
Postgres queries, and vanished on restart. Fixed by correcting the env
var to `REPOSITORY_TYPE=postgres`.