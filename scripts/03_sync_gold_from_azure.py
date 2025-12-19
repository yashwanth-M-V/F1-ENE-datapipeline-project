import os
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import pandas as pd
from io import BytesIO

# --------------------------------------------------
# Config
# --------------------------------------------------
load_dotenv()

AZURE_CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not AZURE_CONN_STR:
    raise RuntimeError("Missing AZURE_STORAGE_CONNECTION_STRING")

ACCOUNT_NAME = "f1pipelinestorageaccount"
GOLD_CONTAINER = "gold"

PROJECT_ROOT = Path(__file__).parents[1]
LOCAL_GOLD_DIR = PROJECT_ROOT / "data" / "gold"
LOCAL_GOLD_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Azure client
# --------------------------------------------------
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONN_STR)
container_client = blob_service_client.get_container_client(GOLD_CONTAINER)

# --------------------------------------------------
# Helper: download + merge parquet
# --------------------------------------------------
def download_gold_table(prefix: str, output_name: str):
    print(f"🔄 Syncing {output_name}")

    blobs = [
        blob.name
        for blob in container_client.list_blobs(name_starts_with=prefix)
        if blob.name.endswith(".parquet")
    ]

    if not blobs:
        print(f"⚠️ No files found for {output_name}")
        return

    dfs = []
    for blob_name in blobs:
        blob_client = container_client.get_blob_client(blob_name)
        data = blob_client.download_blob().readall()
        dfs.append(pd.read_parquet(BytesIO(data)))

    final_df = pd.concat(dfs, ignore_index=True)
    out_path = LOCAL_GOLD_DIR / f"{output_name}.parquet"
    final_df.to_parquet(out_path, index=False)

    print(f"✅ Saved {output_name} → {out_path} ({len(final_df)} rows)")

# --------------------------------------------------
# Entry
# --------------------------------------------------
if __name__ == "__main__":
    try:
        download_gold_table("gold_race_laps", "gold_laps")
        download_gold_table("gold_race_weather", "gold_weather")
        download_gold_table("gold_race_results", "gold_results")
        download_gold_table("gold_drivers", "gold_drivers")
        print("🎉 Gold sync completed successfully")
    except Exception as e:
        print("❌ Azure sync failed. Using local cache only.")
        print(str(e))
