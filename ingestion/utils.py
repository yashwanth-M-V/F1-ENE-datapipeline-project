import yaml
import logging
from pyspark.sql import SparkSession


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def setup_logging(cfg: dict):
    logging.basicConfig(
        level=cfg["logging"]["level"],
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(cfg["logging"]["log_file"]),
            logging.StreamHandler()
        ]
    )


def write_bronze(df, table_name: str, cfg: dict):
    spark = SparkSession.builder.getOrCreate()
    spark_df = spark.createDataFrame(df)

    output_path = f"{cfg['storage']['bronze_path']}/{table_name}"

    (
        spark_df
        .write
        .format("delta")
        .mode("append")
        .partitionBy("season", "event_round", "session_type")
        .save(output_path)
    )
