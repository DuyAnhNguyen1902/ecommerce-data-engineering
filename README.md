# 🛒 Ecommerce Data Engineering Pipeline

This project is an end-to-end Data Engineering pipeline built around an e-commerce dataset. It demonstrates how raw business data can be collected, processed, transformed, and organized into a layered data warehouse for analytics. The project follows a common data engineering architecture by separating data into Raw, Warehouse, and Mart layers while using Apache Airflow to orchestrate the entire workflow.

The pipeline starts by loading exported e-commerce data into the Raw layer of PostgreSQL. The data is then transformed into a structured Warehouse layer using an incremental loading strategy based on PostgreSQL's `ON CONFLICT DO UPDATE`, allowing existing records to be updated without recreating tables. After that, aggregated business metrics are generated in the Mart layer to support reporting and analytical queries. Before the workflow finishes, a Data Quality Check validates that the data has been loaded successfully and meets basic quality requirements.

To make the project closer to a real production environment, the entire system is containerized with Docker, sensitive configuration is managed through environment variables (`.env`), and the ETL pipeline is orchestrated with Apache Airflow. The codebase is organized into independent modules for data ingestion, transformation, data quality validation, and workflow orchestration, making it easier to maintain and extend in the future.

Although this project is designed as a portfolio project, its overall architecture and implementation follow many of the practices commonly used in modern Data Engineering workflows, including incremental ETL, layered data warehousing, workflow automation, modular project structure, and automated data validation.

---

# 🏗️ System Architecture

The project follows a layered data architecture to separate raw data ingestion, data transformation, and analytical reporting. This design improves maintainability, scalability, and simplifies future enhancements.

```text
                    +----------------------+
                    |   Trendify Exports   |
                    |    (Excel Files)     |
                    +----------+-----------+
                               |
                               |
                               v
                    +----------------------+
                    |      Raw Layer       |
                    |   PostgreSQL Schema  |
                    +----------+-----------+
                               |
                               |
                               v
                    +----------------------+
                    |   Warehouse Layer    |
                    | Incremental ETL      |
                    | (UPSERT / ON CONFLICT)|
                    +----------+-----------+
                               |
                               |
                               v
                    +----------------------+
                    |      Mart Layer      |
                    | Aggregated Data Marts|
                    +----------+-----------+
                               |
                               |
                               v
                    +----------------------+
                    |  Data Quality Check  |
                    +----------+-----------+
                               |
                               |
                               v
                    +----------------------+
                    | Ready for Analytics  |
                    +----------------------+

               Apache Airflow orchestrates the entire pipeline
```

The ETL workflow is orchestrated by Apache Airflow, where each stage is executed as an independent task. Data is first loaded into the Raw layer, transformed into the Warehouse layer using an incremental loading strategy, refreshed into analytical Data Marts, and finally validated through automated Data Quality Checks before the pipeline completes successfully.

---

# 🛠️ Technology Stack

| Category                | Technology              |
| ----------------------- | ----------------------- |
| Programming Language    | Python 3.11             |
| Database                | PostgreSQL              |
| Workflow Orchestration  | Apache Airflow          |
| Containerization        | Docker & Docker Compose |
| Data Processing         | Pandas                  |
| Web Automation          | Selenium                |
| Version Control         | Git & GitHub            |
| Database Administration | pgAdmin 4               |

---

# 📂 Project Structure

```text
ecommerce-data-engineering
│
├── config/                 # Project configuration
├── dags/                   # Apache Airflow DAGs
├── ingestion/              # Load raw data into PostgreSQL
├── warehouse/              # Warehouse loading process
├── mart/                   # Data Mart generation
├── quality/                # Data quality validation
├── scraper/                # Selenium data collection
├── sql/                    # SQL scripts
│   ├── warehouse_init.sql
│   ├── warehouse_incremental.sql
│   ├── mart_init.sql
│   └── mart_refresh.sql
│
├── logs/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── main.py
```

---

# ⚙️ ETL Workflow

The ETL pipeline consists of four independent stages managed by Apache Airflow.

### 1. Extract Raw Data

The pipeline loads exported e-commerce Excel files into the **Raw** schema in PostgreSQL. Existing raw tables are truncated before each load to ensure that the latest exported data is always available for downstream processing.

### 2. Warehouse Incremental Loading

The Warehouse layer transforms raw data into a structured format suitable for analytics. Instead of recreating tables every time, the project uses PostgreSQL's **UPSERT** mechanism (`INSERT ... ON CONFLICT DO UPDATE`) to incrementally update existing records and insert new ones. This approach prevents duplicate records and better reflects how production ETL pipelines are commonly implemented.

### 3. Mart Refresh

The Mart layer contains aggregated business data for reporting and analytics. Since these tables are derived entirely from the Warehouse layer, each execution refreshes the mart tables using a **TRUNCATE + INSERT** strategy to ensure that analytical results always reflect the latest warehouse data.

### 4. Data Quality Validation

Before the workflow finishes, a Data Quality Check validates that the ETL process completed successfully. The current validation verifies that critical tables contain data after loading. If any validation fails, the Airflow pipeline stops immediately and marks the workflow as failed.

---

# 🗄️ Data Warehouse Design

The project follows a three-layer data architecture commonly used in modern Data Engineering solutions.

## Raw Layer

The **Raw** schema stores data exactly as it is exported from the source system. No business transformations are applied at this stage, allowing the original data to be preserved for traceability and future processing.

Main tables:

- `fact_orders`
- `fact_order_items`
- `fact_payments`
- `fact_reviews`
- `fact_product_sales`
- `dim_products`
- `dim_inventory_status`

---

## Warehouse Layer

The **Warehouse** schema contains cleaned and standardized data that is optimized for analytical processing.

Unlike the Raw layer, the Warehouse implements **Incremental ETL** using PostgreSQL's `INSERT ... ON CONFLICT DO UPDATE` strategy. Existing records are updated while new records are inserted automatically, preventing duplicate data and allowing the pipeline to run repeatedly without recreating tables.

Key characteristics:

- Incremental Loading
- Primary Keys
- UPSERT Strategy
- Structured Data Types
- Analytics-ready Tables

---

## Mart Layer

The **Mart** schema contains aggregated datasets designed for reporting and business analysis.

Instead of storing detailed transactional records, the Mart layer summarizes information into business-friendly tables.

Current Data Marts include:

| Table            | Description             |
| ---------------- | ----------------------- |
| revenue_by_month | Monthly revenue summary |
| top_products     | Best-selling products   |
| payment_funnel   | Payment status analysis |

Because Mart tables are derived entirely from the Warehouse layer, each execution refreshes the data using a **TRUNCATE + INSERT** strategy to ensure consistency.

---

# 🌬️ Apache Airflow Workflow

Apache Airflow is responsible for orchestrating the complete ETL workflow.

The pipeline is divided into four independent tasks executed sequentially.

```text
extract_raw
      │
      ▼
warehouse_incremental
      │
      ▼
mart_refresh
      │
      ▼
quality_check
```

### Task Description

| Task                  | Description                                 |
| --------------------- | ------------------------------------------- |
| extract_raw           | Load Excel files into PostgreSQL Raw schema |
| warehouse_incremental | Incrementally update Warehouse tables       |
| mart_refresh          | Refresh analytical Data Mart tables         |
| quality_check         | Validate ETL output                         |

Each task is isolated so that failures can be detected quickly. If any task fails, the downstream tasks are not executed.

---

# ✅ Data Quality Validation

To ensure that analytical data is reliable, the pipeline performs an automated Data Quality Check after all ETL stages have completed.

Current validation rules include:

- Verify that Raw tables contain data
- Verify that Warehouse tables contain data
- Verify that Mart tables contain data

Example output:

```text
Running Data Quality Check...

✓ raw.fact_orders: 195 rows
✓ warehouse.fact_orders: 195 rows
✓ mart.revenue_by_month: 7 rows

All quality checks passed.
```

If any validation fails, an exception is raised and Apache Airflow marks the workflow as **Failed**.

This quality gate prevents incomplete or invalid data from reaching downstream analytical layers.

---

# 🚀 Getting Started

## Clone the repository

```bash
git clone https://github.com/<your-username>/ecommerce-data-engineering.git

cd ecommerce-data-engineering
```

---

## Configure Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
DB_HOST=postgres
DB_PORT=5432
DB_NAME=ecommerce_dw
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## Start Docker Services

```bash
docker compose up -d
```

This starts:

- PostgreSQL
- pgAdmin
- Apache Airflow

---

## Run the ETL Pipeline

The recommended way is to trigger the workflow from Apache Airflow.

Pipeline:

```text
extract_raw
      ↓
warehouse_incremental
      ↓
mart_refresh
      ↓
quality_check
```

Alternatively, each stage can be executed manually:

```bash
python -m ingestion.load_raw

python -m warehouse.load_warehouse

python -m mart.load_mart

python -m quality.data_quality
```

---

# 📈 Future Improvements

Although the current pipeline is fully functional, several enhancements can further improve scalability and maintainability.

Planned improvements include:

- CI/CD pipeline using GitHub Actions
- Unit and integration testing
- Additional Data Quality validation rules
- Slowly Changing Dimension (SCD) implementation
- Cloud deployment (AWS, Azure, or GCP)
- Data lineage and metadata management
- Monitoring and alerting
- Migration to dbt for transformation management
- Integration with Apache Kafka for streaming ingestion

---

# 👨‍💻 Author

Developed as a personal Data Engineering portfolio project to demonstrate practical experience with ETL pipelines, PostgreSQL, Apache Airflow, Docker, and modern Data Warehouse architecture.

If you have any questions or suggestions, feel free to open an issue or connect via GitHub.
