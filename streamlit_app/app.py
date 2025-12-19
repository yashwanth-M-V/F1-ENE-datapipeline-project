import streamlit as st

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from data_loader import (
    load_gold_laps,
    load_gold_weather,
    load_gold_results,
)

st.set_page_config(
    page_title="F1 Analytics Dashboard",
    layout="wide",
)

st.title("🏎️ Formula 1 Analytics Dashboard")

# --------------------------------------------------
# Load data (once)
# --------------------------------------------------
laps = load_gold_laps()
weather = load_gold_weather()
results = load_gold_results()

# --------------------------------------------------
# Quick health check
# --------------------------------------------------
st.subheader("📊 Data Snapshot")

col1, col2, col3 = st.columns(3)

col1.metric("Laps", f"{len(laps):,}")
col2.metric("Weather records", f"{len(weather):,}")
col3.metric("Race results", f"{len(results):,}")

st.caption("Data loaded from local Gold cache (offline-safe)")
