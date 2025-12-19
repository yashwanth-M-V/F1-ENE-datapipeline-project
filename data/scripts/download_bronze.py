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
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING not found in .env")

# -------------------------------------------------
# Configuration
# -------------------------------------------------
CONTAINER_NAME = "bronze"
LOCAL_BASE_PATH = Path("data/bronze")

LOCAL_BASE_PATH.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Azure client
# -------------------------------------------------
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# -------------------------------------------------
# Download logic
# -------------------------------------------------
def download_bronze():
    blobs = list(container_client.list_blobs())
    print(f"Found {len(blobs)} blobs in container '{CONTAINER_NAME}'")

    for blob in tqdm(blobs, desc="Downloading Bronze"):

        # 🔑 CRITICAL FIX:
        # Skip "folder marker" blobs like "laps" or "laps/"
        if "/" not in blob.name:
            continue

        # Optional extra safety
        if blob.size == 0:
            continue

        local_file_path = LOCAL_BASE_PATH / blob.name
        local_file_path.parent.mkdir(parents=True, exist_ok=True)

        if local_file_path.exists():
            continue

        with open(local_file_path, "wb") as f:
            data = container_client.download_blob(blob.name)
            f.write(data.readall())

    print("✅ Bronze download completed successfully")

# -------------------------------------------------
# Entry point
# -------------------------------------------------
if __name__ == "__main__":
    download_bronze()
