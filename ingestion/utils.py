import pandas as pd
import yaml
import logging
from azure.storage.blob import BlobServiceClient
import io


# =========================
# Config Loader
# =========================
def load_config(config_path: str) -> dict:
    """
    Load YAML configuration file.
    """
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


# =========================
# Logging Setup
# =========================
def setup_logging(cfg: dict):
    """
    Setup logging configuration.
    """
    log_level = cfg["logging"]["level"]
    log_file = cfg["logging"]["log_file"]

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


# =========================
# Bronze Writer
# =========================
def write_bronze(df: pd.DataFrame, table_name: str, cfg: dict):
    """
    Write a pandas DataFrame as Parquet to Azure Blob Storage (Bronze layer).
    """
    connection_string = cfg["azure"]["connection_string"]
    container = cfg["azure"]["bronze_container"]

    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string
    )

    container_client = blob_service_client.get_container_client(container)

    season = df["season"].iloc[0]
    round_no = df["event_round"].iloc[0]
    session = df["session_type"].iloc[0]

    blob_path = (
        f"{table_name}/"
        f"season={season}/"
        f"round={round_no}/"
        f"session={session}/"
        f"data.parquet"
    )

    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)

    container_client.upload_blob(
        name=blob_path,
        data=buffer,
        overwrite=True
    )
