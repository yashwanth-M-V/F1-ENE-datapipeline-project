import streamlit as st
import pandas as pd
import altair as alt
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from streamlit_app.data_loader import load_gold_drivers, load_gold_results

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Season Performance",
    layout="wide"
)

st.title("📈 Season Performance")

# -------------------------------------------------
# Load data
# -------------------------------------------------
results = load_gold_results()
drivers = load_gold_drivers()

# -------------------------------------------------
# Validate data
# -------------------------------------------------
required_cols = {
    "driver", "session", "finish_position",
    "points", "laps_completed"
}

missing = required_cols - set(results.columns)
if missing:
    st.error(f"Gold results schema mismatch. Missing columns: {missing}")
    st.stop()

# -------------------------------------------------
# Sidebar filters
# -------------------------------------------------
st.sidebar.header("Filters")

sessions = sorted(results["session"].dropna().unique())
selected_session = st.sidebar.selectbox(
    "Session",
    sessions,
    index=sessions.index("R") if "R" in sessions else 0
)

session_df = results[results["session"] == selected_session]

if session_df.empty:
    st.warning("No data available for selected session")
    st.stop()

driver_ids = sorted(session_df["driver"].dropna().unique())

def driver_label(driver_id: str) -> str:
    row = drivers[drivers["DriverId"] == driver_id]
    return (
        row["FullName"].iloc[0]
        if not row.empty
        else driver_id.upper()
    )

driver_id = st.sidebar.selectbox(
    "Driver",
    driver_ids,
    format_func=driver_label
)

driver_df = session_df[session_df["driver"] == driver_id]

if driver_df.empty:
    st.warning("No race data available for selected driver")
    st.stop()

# -------------------------------------------------
# Driver header
# -------------------------------------------------
driver_row = drivers[drivers["DriverId"] == driver_id]

if not driver_row.empty:
    info = driver_row.iloc[0]
    st.subheader(info["FullName"])
    st.caption(f"{info['TeamName']} • {info['CountryCode']}")
else:
    st.subheader(driver_id.upper())
    st.caption("Driver metadata not available")

# -------------------------------------------------
# KPIs
# -------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Points",
    int(driver_df["points"].sum())
)

col2.metric(
    "Average Finish Position",
    round(driver_df["finish_position"].mean(), 2)
)

col3.metric(
    "Total Laps Completed",
    int(driver_df["laps_completed"].sum())
)

st.divider()

# -------------------------------------------------
# Finish position trend
# -------------------------------------------------
st.subheader("🏁 Finishing Position Trend")

finish_chart = (
    alt.Chart(driver_df.reset_index(drop=True))
    .mark_line(point=True)
    .encode(
        x=alt.X("index:O", title="Race Index"),
        y=alt.Y(
            "finish_position:Q",
            title="Finish Position",
            scale=alt.Scale(reverse=True)
        ),
        tooltip=[
            alt.Tooltip("finish_position:Q", title="Position"),
            alt.Tooltip("points:Q", title="Points"),
            alt.Tooltip("laps_completed:Q", title="Laps")
        ]
    )
    .properties(height=350)
)

st.altair_chart(finish_chart, use_container_width=True)

# -------------------------------------------------
# Points per race
# -------------------------------------------------
st.subheader("⭐ Points per Race")

points_chart = (
    alt.Chart(driver_df.reset_index(drop=True))
    .mark_bar()
    .encode(
        x=alt.X("index:O", title="Race Index"),
        y=alt.Y("points:Q", title="Points"),
        tooltip=["points:Q"]
    )
    .properties(height=300)
)

st.altair_chart(points_chart, use_container_width=True)

# -------------------------------------------------
# Raw data (optional)
# -------------------------------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(
        driver_df.reset_index(drop=True),
        use_container_width=True
    )
