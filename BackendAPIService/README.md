# Food Recipe Backend (FastAPI)

FastAPI backend exposing REST APIs for recipes, menus, and search. Includes a SQLite fallback and seeds sample data so you can preview without configuring a database.

## Run locally

1) Create and activate a virtualenv (optional)
2) Install dependencies:
   pip install -r requirements.txt

3) Environment (optional):
   - Copy `.env.example` to `.env` and set values if needed.
   - If `DATABASE_URL` is unset, it defaults to `sqlite:///./app.db`.

4) Start the server:
   uvicorn app.main:app --host 0.0.0.0 --port 8000

Open API docs at:
- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

## Endpoints

- GET /recipes
- GET /recipes/{id}
- GET /search?q=
- GET /menus
- GET / : Health check

## Database

- Defaults to SQLite file `app.db`.
- If you configure `DATABASE_URL` for PostgreSQL, SQLAlchemy will use it.
- On startup, sample recipes and images are seeded if the database is empty.
