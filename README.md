# 🛒 Ecommerce Data Engineering Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)
![Apache Airflow](https://img.shields.io/badge/Apache-Airflow-red?logo=apacheairflow)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![GitHub](https://img.shields.io/badge/GitHub-Portfolio-black?logo=github)

An end-to-end **Data Engineering pipeline** that automates data collection, ETL processing, data warehousing, workflow orchestration, and data quality validation for an e-commerce platform.

The project demonstrates how transactional business data can be collected from a web application, transformed through a layered PostgreSQL Data Warehouse, and prepared for business analytics using modern Data Engineering practices.

---

# 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Project Highlights](#-project-highlights)
- [Skills Demonstrated](#-skills-demonstrated)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Data Collection](#-data-collection)
- [Project Structure](#-project-structure)
- [ETL Workflow](#-etl-workflow)
- [Data Warehouse Design](#-data-warehouse-design)
- [Apache Airflow Workflow](#-apache-airflow-workflow)
- [Data Quality Validation](#-data-quality-validation)
- [Getting Started](#-getting-started)
- [Screenshots](#-screenshots)
- [Future Improvements](#-future-improvements)
- [License](#-license)
- [Author](#-author)

---

# 📌 Overview

This project simulates a complete Data Engineering workflow for an e-commerce system.

Unlike many portfolio projects that rely on static CSV datasets, this project begins with an automated **data collection process**. Selenium interacts with the Trendify e-commerce web application, authenticates users, exports business data into Excel files, and provides the input for the ETL pipeline.

The exported data is loaded into PostgreSQL using a layered architecture consisting of **Raw**, **Warehouse**, and **Mart** schemas.

The Warehouse layer implements **Incremental ETL** using PostgreSQL's `INSERT ... ON CONFLICT DO UPDATE` strategy, allowing the pipeline to insert new records while updating existing ones without creating duplicates.

The Mart layer refreshes analytical datasets using a **TRUNCATE + INSERT** strategy, ensuring that reports always reflect the latest Warehouse data.

The processed business data can also be explored through an interactive Power BI dashboard for KPI monitoring and business reporting.

Apache Airflow orchestrates the complete workflow while automated Data Quality Checks validate the pipeline before completion.

The project uses Docker Compose to containerize the PostgreSQL database and Apache Airflow environment, providing a consistent and reproducible setup for ETL execution while allowing the web application and Selenium scraper to run locally during development.

---

# ✨ Key Features

- Automated data collection from the Trendify platform using Selenium
- Automated ingestion of the latest Excel export
- Layered PostgreSQL architecture: Raw → Warehouse → Mart
- Schema contracts and validation for Raw data
- Incremental and idempotent Warehouse loading using PostgreSQL UPSERT
- Automated Data Mart refresh for analytics
- End-to-end workflow orchestration with Apache Airflow
- Automated Data Quality validation with 19 checks
- Centralized ETL audit logging in `metadata.etl_job_log`
- Retry, timeout, and error-handling mechanisms
- Dockerized development and deployment environment
- Secure configuration management using environment variables
- Modular and maintainable Python architecture
- Power BI-ready analytical datasets
- GitHub-ready project structure

---

# 📊 Project Highlights

| Feature                   | Status |
| ------------------------- | ------ |
| Automated Data Collection | ✅     |
| PostgreSQL Data Warehouse | ✅     |
| Raw Layer                 | ✅     |
| Warehouse Layer           | ✅     |
| Mart Layer                | ✅     |
| Incremental ETL           | ✅     |
| Airflow Workflow          | ✅     |
| Docker                    | ✅     |
| Data Quality              | ✅     |
| Modular Python Project    | ✅     |
| Power BI Dashboard        | ✅     |

---

# 💡 Skills Demonstrated

This project demonstrates practical experience with:

- Python ETL Development
- PostgreSQL Database Design
- Incremental Loading Strategies
- Data Warehouse Architecture
- Data Mart Design
- Apache Airflow
- Docker & Docker Compose
- Selenium Web Automation
- Data Quality Validation
- Workflow Orchestration
- SQL Data Transformation
- Git & GitHub
- Power BI Dashboard Development
- Business Intelligence Reporting
- Data Visualization
- DAX

---

# 🛠 Technology Stack

| Category                | Technology              |
| ----------------------- | ----------------------- |
| Programming Language    | Python 3.11             |
| Database                | PostgreSQL              |
| Workflow Orchestration  | Apache Airflow          |
| Containerization        | Docker & Docker Compose |
| Data Processing         | Pandas                  |
| Web Automation          | Selenium                |
| Database Administration | pgAdmin 4               |
| Version Control         | Git & GitHub            |
| Business Intelligence   | Power BI Desktop        |

---

# 🏗 System Architecture

```text
                    +---------------------------+
                    |   Trendify Web Platform   |
                    | React + Spring Boot API   |
                    +-------------+-------------+
                                  |
                                  ▼
                    +---------------------------+
                    |   Selenium Data Scraper   |
                    |   Runs on Local Machine   |
                    +-------------+-------------+
                                  |
                                  ▼
                    +---------------------------+
                    |    Latest Excel Export    |
                    |     7 Source Sheets       |
                    +-------------+-------------+
                                  |
                                  ▼
                    +---------------------------+
                    |    PostgreSQL Raw Layer   |
                    | Schema Contract Validation|
                    +-------------+-------------+
                                  |
                                  ▼
                    +---------------------------+
                    | PostgreSQL Warehouse Layer|
                    | Incremental UPSERT Loading|
                    +-------------+-------------+
                                  |
                                  ▼
                    +---------------------------+
                    | PostgreSQL Data Mart Layer|
                    |   Analytics Aggregations  |
                    +-------------+-------------+
                                  |
                      +-----------+-----------+
                      |                       |
                      ▼                       ▼
        +---------------------------+   +---------------------------+
        |    Data Quality Checks    |   |    Power BI Dashboard     |
        |      19 Validations       |   |   Business Analytics      |
        +---------------------------+   +-------------+-------------+
                                                    |
                                                    ▼
                                      +---------------------------+
                                      |     Business Insights     |
                                      +---------------------------+

        Apache Airflow orchestrates:
        Raw Load → Warehouse Load → Mart Load → Data Quality

        All ETL executions are recorded in:
        metadata.etl_job_log
```

---

# 🕷 Data Collection

Unlike many ETL projects that use pre-existing CSV datasets, this project starts with automated data acquisition.

The Selenium scraper performs the following operations:

1. Launches the Trendify web application.
2. Authenticates with a valid administrator account.
3. Navigates through the administration pages.
4. Exports business data into Excel files.
5. Stores exported files locally for downstream ETL processing.

The exported Excel files become the input source for the Apache Airflow ETL pipeline.

---

# 📂 Project Structure

```text
ecommerce-data-engineering/
│
├── config/
│   ├── logging_config.py          # Centralized logging configuration
│   └── settings.py                # Environment and database settings
│
├── dags/
│   └── ecommerce_pipeline_dag.py  # Airflow DAG for the ETL workflow
│
├── ingestion/
│   ├── audit.py                   # ETL execution audit logging
│   ├── database.py                # PostgreSQL connection and SQL execution
│   ├── excel_reader.py            # Latest Excel file discovery and reading
│   ├── loader.py                  # Bulk loading into PostgreSQL
│   ├── load_raw.py                # Raw-layer ingestion entry point
│   ├── raw_schema.py              # Raw schema contracts
│   └── table_creator.py           # Table creation and schema validation
│
├── warehouse/
│   └── load_warehouse.py          # Warehouse initialization and UPSERT loading
│
├── mart/
│   └── load_mart.py               # Analytical Data Mart refresh
│
├── quality/
│   └── data_quality.py            # Automated Data Quality checks
│
├── scraper/
│   ├── browser.py                 # Selenium browser configuration
│   ├── login.py                   # Trendify authentication
│   ├── scraping.py                # Excel export automation
│   └── server.py                  # Local Trendify service startup
│
├── sql/
│   ├── warehouse_init.sql         # Warehouse tables and constraints
│   ├── warehouse_incremental.sql  # Incremental Warehouse UPSERT logic
│   ├── mart_init.sql              # Data Mart table definitions
│   └── mart_refresh.sql           # Data Mart refresh queries
│
├── logs/                          # Local pipeline logs
│
├── Dockerfile                     # Airflow/Python container image
├── docker-compose.yml             # PostgreSQL, Airflow and pgAdmin services
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
├── .gitignore
└── README.md
```

---

# ⚙️ ETL Workflow

The ETL pipeline is orchestrated by Apache Airflow and consists of four independent stages.

Each stage has a single responsibility and only starts after the previous stage has completed successfully.

## 1. Data Collection

Business data is collected automatically from the Trendify web application using Selenium.

The scraper:

- Opens the Trendify application
- Authenticates using administrator credentials
- Navigates through administration pages
- Exports business data into Excel files
- Saves exported files locally

---

## 2. Raw Layer

The latest exported Excel file is automatically discovered and loaded into the PostgreSQL `raw` schema.

The Raw Layer preserves source-level records while standardizing column names to `snake_case` for consistent downstream processing.

### Purpose

- Preserve source-level data before business transformations
- Separate data ingestion from transformation logic
- Validate source columns using predefined schema contracts
- Provide traceability through centralized ETL audit logs
- Simplify debugging and pipeline recovery

### Ingestion Process

- Selects the latest Excel export automatically
- Loads only the seven approved source sheets
- Skips non-source sheets, including existing Mart exports
- Validates table structures against schema contracts
- Bulk loads records into PostgreSQL
- Records execution status, row counts, duration, and errors in `metadata.etl_job_log`

### Raw Tables

- `fact_orders`
- `fact_order_items`
- `fact_payments`
- `fact_reviews`
- `fact_product_sales`
- `dim_products`
- `dim_inventory_status`

---

## 3. Warehouse Layer

The Warehouse layer transforms raw data into standardized analytical tables.

Unlike a full refresh approach, the Warehouse implements **Incremental ETL** using PostgreSQL's UPSERT functionality.

```sql
INSERT ...
ON CONFLICT (...)
DO UPDATE
```

Advantages:

- Prevents duplicate records
- Supports repeated pipeline execution
- Updates existing records automatically
- Reduces processing time
- Simulates production ETL practices

---

## 4. Mart Layer

The Mart Layer contains aggregated, analytics-ready datasets derived from the Warehouse Layer for reporting and Power BI dashboards.

Unlike the incremental UPSERT strategy used in the Warehouse Layer, Data Marts are rebuilt using a full-refresh approach:

```text
TRUNCATE
   ↓
INSERT
```

### Purpose

- Provide business-focused analytical datasets
- Pre-aggregate frequently used reporting metrics
- Simplify Power BI data modeling
- Improve dashboard query performance
- Ensure reports reflect the latest successfully loaded Warehouse data

### Data Marts

| Table                  | Description                                       |
| ---------------------- | ------------------------------------------------- |
| `revenue_by_month`     | Monthly revenue and order summary                 |
| `top_products`         | Product sales and performance analysis            |
| `customer_segments`    | Customer segmentation and purchasing behavior     |
| `payment_funnel`       | Payment method and payment status analysis        |
| `category_performance` | Revenue and sales performance by product category |

The full-refresh process is automatically executed by the `load_mart` Airflow task after the Warehouse load completes successfully.

---

## 5. Data Quality Validation

The final stage validates data completeness, integrity, and consistency before the ETL workflow is marked as successful.

The pipeline performs 19 automated Data Quality checks across the Raw, Warehouse, and Mart layers.

### Validation Rules

- Required tables exist and contain data
- Primary key columns do not contain null values
- Primary key values are unique
- Warehouse records maintain valid relationships
- Numeric business values are non-negative
- Mart aggregations are consistent with Warehouse data
- Analytical tables contain valid reporting results

Example output:

```text
Running Data Quality Checks...

✓ raw.fact_orders: 195 rows
✓ warehouse.fact_orders: 195 rows
✓ mart.revenue_by_month: 7 rows
✓ Primary key validation passed
✓ Duplicate validation passed
✓ Referential integrity validation passed
✓ Non-negative value validation passed
✓ Mart consistency validation passed

All 19 Data Quality checks passed.
```

The `data_quality` task runs only after the Raw, Warehouse, and Mart loading tasks have completed successfully.

If any validation fails, the process raises an error and Apache Airflow marks the `data_quality` task and the entire workflow as **Failed**, preventing invalid data from being treated as analytics-ready.

---

# 🗄️ Data Warehouse Design

The project follows a classic three-layer Data Warehouse architecture.

```text
Source System
      │
      ▼
Raw Layer
      │
      ▼
Warehouse Layer
      │
      ▼
Mart Layer
```

## Raw Layer

Stores exported business data exactly as received from the source system.

Characteristics:

- Minimal transformation
- Source of truth
- Easy to reload
- Easy to audit

---

## Warehouse Layer

Stores cleaned and standardized business data.

Characteristics:

- Structured schema
- Incremental loading
- UPSERT strategy
- Primary Keys
- Analytics-ready

---

## Mart Layer

Stores aggregated business metrics.

Characteristics:

- Optimized for reporting
- Simplified business queries
- Refresh after Warehouse update
- Supports BI dashboards

---

# 🌬️ Apache Airflow Workflow

The ETL workflow is orchestrated using Apache Airflow.

Current DAG:

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

Task Description

| Task                  | Description                                          |
| --------------------- | ---------------------------------------------------- |
| extract_raw           | Load exported Excel files into PostgreSQL Raw schema |
| warehouse_incremental | Perform Incremental ETL into Warehouse               |
| mart_refresh          | Refresh analytical Data Marts                        |
| quality_check         | Validate loaded data                                 |

Each task executes independently.

If any task fails:

- Downstream tasks are skipped
- Airflow marks the DAG as Failed
- Error logs are available for debugging

---

# 📊 Business Intelligence Dashboard

To demonstrate the Business Intelligence layer of the project, an interactive Power BI dashboard is included.

The dashboard was developed on the original SQL Server implementation of the data warehouse and is preserved in this repository as part of the complete analytics workflow.

Although the ETL pipeline has been upgraded to PostgreSQL, Docker, and Apache Airflow, the dashboard design remains applicable for business reporting and KPI analysis.

### Dashboard Pages

#### Executive Overview

- Total Revenue
- Total Orders
- Average Order Value
- Revenue Trend
- Revenue by Payment Method
- Order Status Distribution

#### Product Analytics

- Top Selling Products
- Revenue by Product
- Revenue by Category
- Product Ranking

#### Payment Analytics

- Payment Status
- Payment Method Distribution
- Successful Payments
- Failed Payments

### Business Value

The dashboard enables business users to:

- Monitor sales performance
- Analyze customer purchasing behavior
- Track payment performance
- Identify top-performing products
- Support data-driven business decisions

---

# 🐳 Docker Environment

The project is fully containerized using Docker Compose.

Current services include:

- PostgreSQL
- Apache Airflow Webserver
- Apache Airflow Scheduler
- pgAdmin

Benefits:

- Reproducible environment
- Easy deployment
- Consistent development setup
- Simplified dependency management

---

# 🚀 Getting Started

## Prerequisites

Install:

- Python 3.11
- Docker Desktop
- Git

---

## Clone Repository

```bash
git clone https://github.com/DuyAnhNguyen1902/ecommerce-data-engineering.git

cd ecommerce-data-engineering
```

---

## Configure Environment Variables

Create a `.env` file from `.env.example`.

### Running inside Docker

```env
DB_HOST=postgres
DB_PORT=5432
DB_NAME=ecommerce_dw
DB_USER=postgres
DB_PASSWORD=your_password
```

Airflow containers communicate with PostgreSQL using the Docker network, so the hostname is `postgres` and the internal PostgreSQL port is `5432`.

### Running from your local machine

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=ecommerce_dw
DB_USER=postgres
DB_PASSWORD=your_password
```

When connecting from Windows (VS Code, pgAdmin or Python running outside Docker), PostgreSQL is exposed on port **5433** through Docker Compose.

---

## Start Docker

```bash
docker compose up -d
```

This starts:

- PostgreSQL
- pgAdmin
- Apache Airflow

---

### Verify PostgreSQL Connection

If you are running Python scripts or pgAdmin on your **local machine**, connect to PostgreSQL using:

```text
Host: localhost
Port: 5433
Database: ecommerce_dw
```

The Docker Compose configuration maps PostgreSQL's internal port `5432` to port `5433` on the host machine.

If you are running services **inside Docker** (such as Apache Airflow), use:

```text
Host: postgres
Port: 5432
Database: ecommerce_dw
```

Containers communicate through Docker's internal network, so the PostgreSQL service is reachable by its service name `postgres`.

---

## Run the Pipeline

The recommended approach is to trigger the DAG from Airflow.

Pipeline execution:

```text
extract_raw
      ↓
warehouse_incremental
      ↓
mart_refresh
      ↓
quality_check
```

Or execute each stage manually:

```bash
docker compose exec airflow_scheduler bash -lc "cd /opt/airflow/project && python -m ingestion.load_raw"
docker compose exec airflow_scheduler bash -lc "cd /opt/airflow/project && python -m warehouse.load_warehouse"
docker compose exec airflow_scheduler bash -lc "cd /opt/airflow/project && python -m mart.load_mart"
docker compose exec airflow_scheduler bash -lc "cd /opt/airflow/project && python -m quality.data_quality"
```

---

# 📈 Future Improvements

Potential enhancements include:

- Unit Testing
- Integration Testing
- Slowly Changing Dimensions (SCD)
- Monitoring & Alerting
- Cloud Deployment (AWS, Azure, or GCP)
- dbt Integration

---

# 📄 License

This project is intended for educational purposes and as a personal Data Engineering portfolio project.

---

# 👨‍💻 Author

**Duy Anh Nguyen**

This project was developed to demonstrate practical knowledge of:

- Python
- PostgreSQL
- Apache Airflow
- Docker
- Selenium
- Data Warehousing
- Incremental ETL
- Data Quality Validation
