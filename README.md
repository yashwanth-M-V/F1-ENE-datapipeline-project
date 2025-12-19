
# 🏎️ Formula 1 End-to-End Data Engineering & ML Project

This project demonstrates a **production-style end-to-end data pipeline** using Formula 1 data, following **Medallion Architecture (Bronze → Silver → Gold)** and preparing the foundation for **machine learning and analytics applications**.

The goal is to showcase **data engineering skills**, **cloud architecture**, and **ML-readiness**, rather than just analysis.

---

## 🚀 Tech Stack

- **Data Source**: FastF1 Python package
- **Language**: Python, PySpark
- **Cloud**: Azure Blob Storage (Data Lake Gen2)
- **Processing**: Databricks (Spark)
- **Architecture**: Medallion (Bronze / Silver / Gold)
- **Storage Format**: Parquet
- **Version Control**: Git & GitHub
- **Future**: Streamlit, ML (XGBoost / SHAP)

---

## Architecture Overview

```

FastF1 API
↓
Bronze (Raw Parquet in Azure Blob)
↓
Silver (Cleaned, Typed, Normalized)
↓
Gold (Business & ML Ready Tables)
↓
Analytics (Streamlit) / ML Models

```

---

## 📂 Project Structure

```

F1-ENE-datapipeline-project/
│
├── ingestion/
│   ├── fastf1_ingestion.py
│   └── utils.py
│
├── data/
│   ├── bronze/        # Downloaded raw data (local mirror)
│   ├── silver/        # Cleaned local Silver data
│   └── notebooks/
│       ├── 01_explore_bronze_laps.ipynb
│       ├── 02_bronze_to_silver_laps.ipynb
│       ├── 03_bronze_to_silver_weather.ipynb
│       ├── 04_bronze_to_silver_results.ipynb
│       └── 05_gold_layer_creation.ipynb
│
├── config/
│   └── config.yaml
│
├── scripts/
│   ├── download_bronze.py
│   └── upload_silver.py
│
├── .gitignore
├── README.md
└── requirements.txt

```

---

## 🥉 Bronze Layer

- Raw data pulled using **FastF1**
- Stored as **partitioned Parquet** in Azure Blob Storage
- No schema enforcement
- Represents **source-of-truth**

**Datasets:**
- Laps
- Weather
- Results

---

## 🥈 Silver Layer

- Data cleaned and standardized locally using Pandas
- Key transformations:
  - Timedelta → numeric seconds
  - Dropped high-null / irrelevant columns
  - Consistent dtypes across all partitions
- Uploaded back to Azure Blob Storage

**Silver Tables:**
- `fact_laps`
- `fact_weather`
- `fact_results`

---

## 🥇 Gold Layer (Databricks)

Gold tables are analytics and ML ready.

### `gold_race_laps`
- Lap-level performance
- Tyre, stint, lap time features

### `gold_race_weather`
- Track and weather conditions
- Time-aligned weather metrics

### `gold_race_results`
- Race outcomes
- Grid position, finish position, points

**Row Counts (2024 Season):**
- Laps: 26,606
- Weather: 3,690
- Results: 479

---

## 📊 What This Project Demonstrates

- End-to-end data engineering pipeline
- Azure + Databricks integration
- Medallion architecture best practices
- Schema governance & partitioning
- Debugging real-world Spark issues
- ML-ready data modeling

---

## 🔜 Next Steps (Planned as if today 19-12)

- Gold feature table (laps + weather + results)
- ML model for lap time prediction
- SHAP explainability
- Streamlit analytics dashboard
- Streamlit ML demo app

---

## 👤 Author

**Yashwanth Madyala Venkata**  
Master’s student | Data Engineering & ML  
```
