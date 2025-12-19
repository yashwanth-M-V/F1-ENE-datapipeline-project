from pathlib import Path
import pandas as pd
import streamlit as st

# --------------------------------------------------
# Resolve project root reliably (FILE-BASED)
# --------------------------------------------------
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[1]   # streamlit_app → project root
DATA_DIR = PROJECT_ROOT / "data" / "gold"

# --------------------------------------------------
# Internal loader
# --------------------------------------------------
@st.cache_data(show_spinner=False)
def _load_parquet(file_name: str) -> pd.DataFrame:
    path = DATA_DIR / file_name

    if not path.exists():
        raise FileNotFoundError(f"Gold file not found: {path}")

    return pd.read_parquet(path)

# --------------------------------------------------
# Public loaders
# --------------------------------------------------
def load_gold_laps() -> pd.DataFrame:
    return _load_parquet("gold_laps.parquet")

def load_gold_weather() -> pd.DataFrame:
    return _load_parquet("gold_weather.parquet")

def load_gold_results() -> pd.DataFrame:
    return _load_parquet("gold_results.parquet")

def load_gold_drivers():
    return _load_parquet("gold_drivers.parquet")
