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

Apache Airflow orchestrates the complete workflow while automated Data Quality Checks validate the pipeline before completion.

The project uses Docker Compose to containerize the PostgreSQL database and Apache Airflow environment, providing a consistent and reproducible setup for ETL execution while allowing the web application and Selenium scraper to run locally during development.

---

# ✨ Key Features

- Automated data collection using Selenium
- Layered PostgreSQL Data Warehouse
- Incremental ETL using PostgreSQL UPSERT
- Automated Data Mart refresh
- Apache Airflow orchestration
- Dockerized deployment
- Automated Data Quality validation
- Secure configuration using environment variables
- Modular Python architecture
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

---

# 🏗 System Architecture

```text
                    +---------------------------+
                    |   Trendify Web Platform   |
                    | React + Spring Boot API   |
                    +-------------+-------------+
                                  |
                                  |
                                  ▼
                    +---------------------------+
                    |   Selenium Data Scraper   |
                    +-------------+-------------+
                                  |
                                  |
                                  ▼
                    +---------------------------+
                    |     Excel Export Files    |
                    +-------------+-------------+
                                  |
                                  |
                                  ▼
                    +---------------------------+
                    |     PostgreSQL Raw Layer  |
                    +-------------+-------------+
                                  |
                                  |
                                  ▼
                    +---------------------------+
                    | Warehouse Incremental ETL |
                    | INSERT ... ON CONFLICT    |
                    +-------------+-------------+
                                  |
                                  |
                                  ▼
                    +---------------------------+
                    |       Data Mart Layer     |
                    |   Aggregated Analytics    |
                    +-------------+-------------+
                                  |
                                  |
                                  ▼
                    +---------------------------+
                    |    Data Quality Checks    |
                    +-------------+-------------+
                                  |
                                  |
                                  ▼
                    +---------------------------+
                    |    Ready for Analytics    |
                    +---------------------------+

             Apache Airflow orchestrates the ETL workflow
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
ecommerce-data-engineering
│
├── config/
├── dags/
├── ingestion/
├── warehouse/
├── mart/
├── quality/
├── scraper/
├── sql/
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
└── .env.example
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

The exported Excel files are loaded into the PostgreSQL **Raw** schema.

Purpose:

- Preserve original source data
- Separate ingestion from transformation
- Provide traceability
- Simplify debugging

Current Raw tables:

- fact_orders
- fact_order_items
- fact_payments
- fact_reviews
- fact_product_sales
- dim_products
- dim_inventory_status

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

The Mart layer stores aggregated business information for reporting and analytics.

Instead of incremental loading, Data Marts are refreshed using:

```text
TRUNCATE

↓

INSERT
```

Current Data Marts:

| Table            | Description             |
| ---------------- | ----------------------- |
| revenue_by_month | Monthly revenue summary |
| top_products     | Product performance     |
| payment_funnel   | Payment status analysis |

This strategy guarantees that reports always reflect the latest Warehouse data.

---

## 5. Data Quality Validation

The final stage validates the ETL pipeline before completion.

Current validation rules:

- Raw tables contain data
- Warehouse tables contain data
- Mart tables contain data

Example:

```text
Running Data Quality Check...

✓ raw.fact_orders: 195 rows
✓ warehouse.fact_orders: 195 rows
✓ mart.revenue_by_month: 7 rows

All quality checks passed.
```

If any validation fails, Apache Airflow marks the workflow as **Failed**.

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
python -m ingestion.load_raw

python -m warehouse.load_warehouse

python -m mart.load_mart

python -m quality.data_quality
```

---

# 📈 Future Improvements

Potential enhancements include:

- GitHub Actions (CI/CD)
- Unit Testing
- Integration Testing
- Additional Data Quality Rules
- Slowly Changing Dimensions (SCD)
- Monitoring & Alerting
- Cloud Deployment (AWS, Azure, or GCP)
- Power BI Dashboard
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

If you have any questions or suggestions, feel free to open an issue or connect with me on GitHub.
