# Apache Airflow (Docker Compose)

Quick start for running Airflow locally with Docker Compose.

## Prerequisites

- Docker Community Edition (CE)
- Docker Compose v2.14.0 or newer
- At least 4 GB of memory allocated to Docker

Fetch the official Compose file if you do not have it yet:

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.3.2/docker-compose.yaml'
```

## 1. Create required folders

```bash
mkdir -p ./dags ./logs ./plugins ./config
```

## 2. Set the current user in `.env`

On Linux, set `AIRFLOW_UID` so files created under `dags`, `logs`, `config`, and `plugins` are owned by your user:

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

On macOS / Windows you can ignore the `AIRFLOW_UID` warning, or create `.env` with:

```bash
echo -e "AIRFLOW_UID=50000" > .env
```

## 3. Add DAG files

Place your DAG Python files in the `./dags` folder. Airflow will pick them up automatically.

## 4. Initialize the database

Run database migrations and create the first user account:

```bash
docker compose up airflow-init
```

When initialization finishes successfully, you should see a message like:

```text
airflow-init-1 exited with code 0
```

Default login (official Compose quick-start):

- Username: `airflow`
- Password: `airflow`

## 5. Run Airflow

Start all services:

```bash
docker compose up
```

The Airflow UI / API server is available at [http://localhost:8080](http://localhost:8080).

## Useful commands

```bash
# Stop services
docker compose down

# Stop and remove volumes (resets the database)
docker compose down -v
```
