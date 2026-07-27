# A2 — Connecting your CRUD to the database (SQLite)

## What this is
This takes the in-memory CRUD API from A1 and swaps its storage for a real
SQLite database. All five endpoints (`GET /tasks`, `GET /tasks/{id}`,
`POST /tasks`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`) behave exactly the
same as A1 — same request/response shapes, same status codes — but the
data now survives a server restart.

## Why SQLite
SQLite was used because it needs no separate server or install — it's a
single file (`tasks.db`) that Python's built-in `sqlite3` module can open
directly. For a small project like this, that's zero setup and zero moving
parts, while still giving real persistence: data written to the file stays
there across restarts, which an in-memory list can never do.

## Where the database lives
`tasks.db` sits in the project root, next to `main.py`. It's created
automatically the first time the app runs — opening a SQLite file that
doesn't exist yet creates it. The file is gitignored, so a fresh clone
always starts with a clean, freshly-seeded database rather than someone
else's data.

## How to run it
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
On first run, `tasks.db` and the `tasks` table are created automatically,
and three example tasks are seeded. Restarting the server does not
duplicate the seed data — it only inserts when the table is empty.

## Proving persistence
Created tasks via `POST /tasks`, then stopped and restarted the server —
the tasks were still present on the next `GET /tasks`. This is the first
point in the project where data survives a restart.

## Stage 4 — SQL explored by hand
Opened `tasks.db` directly in DB Browser for SQLite and ran queries against
it live, alongside the running API. Example:

```sql
SELECT COUNT(*) FROM tasks;
```
Returned the current row count matching what the API reported. Also ran
`UPDATE tasks SET done = 1;` and `DELETE FROM tasks WHERE done = 1;`
directly in DB Browser, then called `GET /tasks` from the API **without
restarting the server** — the change appeared instantly, confirming the
API and DB Browser read and write the exact same file with no syncing
step involved.

Screenshot: `db-browser-screenshot.png` (in this folder).

## Architecture note
Only the storage layer changed — routes and validation logic are otherwise
identical to A1. All queries use parameterized placeholders (`?`), values
are always passed separately from the SQL string, never concatenated in.