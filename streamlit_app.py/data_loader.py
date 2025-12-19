from pathlib import Path
import pandas as pd
import streamlit as st

# -------------------------------------------------
# Paths
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
GOLD_DIR = PROJECT_ROOT / "data" / "gold"

GOLD_LAPS_PATH = GOLD_DIR / "gold_laps.parquet"
GOLD_WEATHER_PATH = GOLD_DIR / "gold_weather.parquet"
GOLD_RESULTS_PATH = GOLD_DIR / "gold_results.parquet"


# -------------------------------------------------
# Internal helper
# -------------------------------------------------
def _load_parquet(path: Path, name: str) -> pd.DataFrame:
    if not path.exists():
        st.error(f"❌ {name} not found at {path}")
        return pd.DataFrame()

    try:
        return pd.read_parquet(path)
    except Exception as e:
        st.error(f"❌ Failed to load {name}: {e}")
        return pd.DataFrame()


# -------------------------------------------------
# Public loaders (cached)
# -------------------------------------------------
@st.cache_data(show_spinner="Loading race laps data...")
def load_laps() -> pd.DataFrame:
    df = _load_parquet(GOLD_LAPS_PATH, "gold_laps")

    if not df.empty:
        # Normalize column names once
        df.columns = df.columns.str.lower()

    return df


@st.cache_data(show_spinner="Loading weather data...")
def load_weather() -> pd.DataFrame:
    df = _load_parquet(GOLD_WEATHER_PATH, "gold_weather")

    if not df.empty:
        df.columns = df.columns.str.lower()

    return df


@st.cache_data(show_spinner="Loading race results...")
def load_results() -> pd.DataFrame:
    df = _load_parquet(GOLD_RESULTS_PATH, "gold_results")

    if not df.empty:
        df.columns = df.columns.str.lower()

    return df
