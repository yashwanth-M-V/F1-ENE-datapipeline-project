import streamlit as st
import pandas as pd
from pathlib import Path
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Driver Profile",
    layout="wide"
)

st.title("👤 Driver Profile")

# -------------------------------------------------
# Load gold_drivers (local only)
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "gold"
DRIVERS_PATH = DATA_DIR / "gold_drivers.parquet"

if not DRIVERS_PATH.exists():
    st.error(f"Gold drivers file not found at: {DRIVERS_PATH}")
    st.stop()

drivers = pd.read_parquet(DRIVERS_PATH)

# -------------------------------------------------
# Deduplicate drivers (safety)
# -------------------------------------------------
drivers = (
    drivers
    .drop_duplicates(subset=["DriverId"])
    .sort_values("FullName")
    .reset_index(drop=True)
)

# -------------------------------------------------
# Sidebar selection
# -------------------------------------------------
st.sidebar.header("Select Driver")

selected_driver_id = st.sidebar.selectbox(
    "Driver",
    drivers["DriverId"],
    format_func=lambda x: drivers.loc[
        drivers["DriverId"] == x, "FullName"
    ].values[0]
)

driver = drivers[drivers["DriverId"] == selected_driver_id].iloc[0]

# -------------------------------------------------
# Profile layout
# -------------------------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(driver["FullName"])
    st.caption("Formula 1 Driver")

    st.markdown(f"""
    **First Name:** {driver["FirstName"]}  
    **Last Name:** {driver["LastName"]}  
    **Country:** {driver["CountryCode"]}  
    **Team:** {driver["TeamName"]}
    """)

with col2:
    st.subheader("Overview")
    st.info(
        f"{driver['FullName']} is a Formula 1 driver representing "
        f"**{driver['CountryCode']}**, currently driving for "
        f"**{driver['TeamName']}**."
    )

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.divider()
st.caption("Data source: Gold Layer (local cached)")
