# Ecommerce Data Engineering Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.10.5-red?logo=apacheairflow)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)
![CI](https://img.shields.io/badge/CI-compileall%20%2B%20pytest-success?logo=githubactions)

An end-to-end data engineering portfolio project that collects e-commerce data,
loads it into a layered PostgreSQL warehouse, builds analytical marts, and
validates the result through an Apache Airflow workflow.

## Architecture

```text
Trendify web application
        |
        v
Selenium scraper -> Excel export files
        |
        v
PostgreSQL raw schema
        |
        v
Incremental warehouse ETL (INSERT ... ON CONFLICT DO UPDATE)
        |
        v
Data marts (revenue, products, payment funnel)
        |
        v
Data quality checks -> Power BI / analytics
```

Airflow runs the data pipeline in this order:

```text
extract_raw -> warehouse_incremental -> mart_refresh -> quality_check
```

## What is containerized

Docker Compose provides the database and workflow-orchestration environment:

- PostgreSQL 16
- pgAdmin 4
- Apache Airflow webserver
- Apache Airflow scheduler

The Airflow services are built from `Dockerfile.airflow`, which installs the
pinned Python dependencies from `requirements.txt`. The React frontend, Spring
Boot backend, Selenium browser, and Chrome driver are currently run on the host;
they are not included as Docker Compose services.

## Project structure

```text
.
|-- config/                 Environment and logging configuration
|-- dags/                   Airflow DAG
|-- ingestion/              Excel-to-raw loading
|-- warehouse/              Incremental warehouse loader
|-- mart/                   Data mart refresh
|-- quality/                Data quality rules
|-- scraper/                Selenium data collection
|-- sql/                    Schema, warehouse, and mart SQL
|-- tests/                  Automated Python tests
|-- .github/workflows/      Continuous integration
|-- Dockerfile              Standalone ingestion image
|-- Dockerfile.airflow      Airflow image with project dependencies
`-- docker-compose.yml      Local database and Airflow services
```

## Warehouse design

### Raw

The raw schema preserves the exported source data with minimal transformation.
The loader truncates each raw table before loading the newest Excel export.

### Warehouse

The warehouse schema standardizes types and applies incremental UPSERTs. Primary
and composite keys make repeated executions idempotent for the current model.

Main tables include:

- `warehouse.dim_products`
- `warehouse.fact_orders`
- `warehouse.fact_order_items`
- `warehouse.fact_payments`
- `warehouse.fact_reviews`
- `warehouse.fact_product_sales`
- `warehouse.dim_inventory_status`

### Mart

The mart layer uses `TRUNCATE + INSERT` to rebuild small analytical tables after
the warehouse load:

| Mart | Purpose |
| --- | --- |
| `mart.revenue_by_month` | Monthly orders, revenue, discounts, and customers |
| `mart.top_products` | Product sales and order performance |
| `mart.payment_funnel` | Payment-status counts and amounts |

## Data quality validation

The quality task uses one database connection for the complete validation run.
Schema and table names are quoted with `psycopg2.sql.Identifier` rather than
interpolated into SQL strings.

The current rules verify:

- important Raw, Warehouse, and Mart tables are not empty;
- key columns are not `NULL`;
- primary and composite business keys are not duplicated;
- order items do not reference missing orders;
- order, item, payment, product, sales, and inventory values are not negative;
- review ratings are within the 1-5 range;
- monthly Mart revenue matches the monthly Warehouse aggregation.

Any failed rule raises an error, so Airflow marks the quality task and DAG run as
failed.

## Getting started

### Prerequisites

- Git
- Docker Desktop with Docker Compose
- Python 3.11 for running modules or tests directly
- Access to the separate Trendify frontend/backend when collecting new exports

### 1. Clone and configure

```bash
git clone https://github.com/DuyAnhNguyen1902/ecommerce-data-engineering.git
cd ecommerce-data-engineering
cp .env.example .env
```

On Windows PowerShell, use:

```powershell
Copy-Item .env.example .env
```

Replace every `change_me` value and set application/scraper paths as needed.
Generate a long random value for `AIRFLOW_SECRET_KEY`; do not commit `.env`.

### PostgreSQL ports: host versus Docker network

There are two valid PostgreSQL endpoints because Docker publishes a different
host port:

| Caller | Host | Port | Example |
| --- | --- | ---: | --- |
| Python/Power BI/psql on your computer | `localhost` | `5433` | `localhost:5433` |
| Airflow or another Compose service | `postgres` | `5432` | `postgres:5432` |

The mapping in Compose is `5433:5432`: port 5433 belongs to the host, while port
5432 remains PostgreSQL's internal container port. `.env.example` therefore uses
`DB_HOST=localhost` and `DB_PORT=5433` for host-side commands; Compose overrides
these values inside Airflow with `postgres:5432`.

### 2. Prepare input files

Place the exported Excel workbook in `./file_export`. Compose mounts this relative
directory at `/data/file_export` for both Airflow services, so the setup works
regardless of the repository's absolute location.

To collect a fresh export on the host, configure `APP_URL`, `LOGIN_EMAIL`,
`LOGIN_PASSWORD`, `FRONTEND_PATH`, `BACKEND_PATH`, and `BASE_FOLDER`, then run:

```bash
python -m scraper.scraping
```

### 3. Start the services

```bash
docker compose up --build -d
docker compose ps
```

Service URLs:

- Airflow: <http://localhost:8088>
- pgAdmin: <http://localhost:5050>
- PostgreSQL from host tools: `localhost:5433`

Trigger `ecommerce_data_pipeline` from the Airflow UI after the Excel export is
available.

### 4. Run pipeline stages manually

With the Python dependencies installed and the host-side database settings in
`.env`:

```bash
python -m ingestion.load_raw
python -m warehouse.load_warehouse
python -m mart.load_mart
python -m quality.data_quality
```

## Development and tests

Create a virtual environment and install the pinned dependencies:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Run the same checks used by GitHub Actions:

```bash
python -m compileall -q .
pytest -q
```

The CI workflow runs both commands on pushes and pull requests with Python 3.11.
The current unit tests exercise the quality-check connection lifecycle and input
validation without requiring a live database. The full pipeline remains an
integration test and requires PostgreSQL plus a representative Excel export.

## Power BI

Connect Power BI Desktop to PostgreSQL using:

- Server: `localhost:5433`
- Database: the value of `POSTGRES_DB` (default `ecommerce_dw`)
- Tables: `mart.revenue_by_month`, `mart.top_products`, and
  `mart.payment_funnel`

Suggested report pages and KPIs:

- Executive overview: total revenue, total orders, unique customers, and average
  order value;
- Revenue trend: monthly revenue and discount trend;
- Product performance: top products by revenue and quantity;
- Payments: payment-status funnel and total payment amount.

Refresh the report after a successful Airflow DAG run. Store credentials in the
Power BI data-source settings rather than in the `.pbix` documentation or Git.

## Portfolio screenshots to add

Add sanitized images under `docs/screenshots/` and reference them from this
README. A strong portfolio walkthrough should include:

1. Airflow graph view showing all four tasks in a successful DAG run.
2. pgAdmin schema browser showing `raw`, `warehouse`, `mart`, and `metadata`.
3. A warehouse entity-relationship diagram with key relationships.
4. Data quality task logs showing representative passing rules.
5. A Power BI dashboard with the KPIs and charts listed above.

Do not include passwords, email credentials, tokens, or customer personal data
in screenshots.

## Current limitations and next steps

- Airflow metadata and analytical tables currently share one PostgreSQL database;
  separate them for a production-style deployment.
- The scraper depends on a separately running Trendify application and local
  Chrome environment.
- Add PostgreSQL integration tests with seeded fixtures.
- Add alerting, lineage, and freshness checks.
- Consider dbt for transformation testing and documentation.
- Containerize the source application and browser only if full end-to-end local
  deployment becomes a project goal.

## Author

**Duy Anh Nguyen**

Built as a portfolio demonstration of Python, PostgreSQL, Airflow, Docker,
Selenium, incremental ETL, data marts, and data quality engineering.
