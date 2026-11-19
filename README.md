# uMthombolwazi Intelligence

## Local PostgreSQL

Prerequisites: Docker Engine with Docker Compose v2.

1. Copy the environment template: `cp .env.example .env`.
2. Set a local value for `POSTGRES_PASSWORD` in `.env`.
3. Set the same password in `UMTHOMBOLWAZI_DATABASE_URL`.
4. Start PostgreSQL from the repository root:

   `docker compose up -d database`

Check the service with `docker compose ps`. The database health check
must report healthy before it is used by the backend.

Stop the service with `docker compose down`. This preserves the named
database volume. Use `docker compose down -v` only when you intend to
delete the local database data.
