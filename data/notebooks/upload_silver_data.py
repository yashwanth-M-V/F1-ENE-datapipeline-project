import os
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from tqdm import tqdm

# -------------------------------------------------
# Load secrets
# -------------------------------------------------
load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not CONNECTION_STRING:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING not found")

# -------------------------------------------------
# Config
# -------------------------------------------------
CONTAINER_NAME = "silver"
LOCAL_SILVER_PATH = Path("data/silver")

if not LOCAL_SILVER_PATH.exists():
    raise ValueError("Local Silver folder does not exist")

# -------------------------------------------------
# Azure client
# -------------------------------------------------
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# -------------------------------------------------
# Upload logic
# -------------------------------------------------
def upload_silver():
    files = list(LOCAL_SILVER_PATH.rglob("*.parquet"))

    if not files:
        raise RuntimeError("No parquet files found in Silver folder")

    print(f"📦 Found {len(files)} Silver parquet files to upload")

    for file in tqdm(files, desc="Uploading Silver"):
        blob_path = file.relative_to(LOCAL_SILVER_PATH).as_posix()

        with open(file, "rb") as f:
            container_client.upload_blob(
                name=blob_path,
                data=f,
                overwrite=True  # ✅ idempotent overwrite
            )

    print("✅ Silver upload completed successfully")

# -------------------------------------------------
# Entry
# -------------------------------------------------
if __name__ == "__main__":
    upload_silver()
