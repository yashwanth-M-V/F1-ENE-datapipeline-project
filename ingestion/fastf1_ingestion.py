import fastf1
import pandas as pd
import yaml
import logging
from pathlib import Path
from datetime import datetime

from ingestion.utils import (
    load_config,
    setup_logging,
    write_bronze
)

fastf1.Cache.enable_cache("./fastf1_cache")


def ingest_session(season: int, round_no: int, session_type: str, cfg: dict):
    logging.info(f"Ingesting: Season={season}, Round={round_no}, Session={session_type}")

    try:
        session = fastf1.get_session(season, round_no, session_type)
        session.load()

        ingestion_ts = datetime.utcnow()

        if cfg["datasets"]["laps"]["enabled"]:
            laps = session.laps
            if not laps.empty:
                laps_df = laps.reset_index(drop=True)
                laps_df["season"] = season
                laps_df["event_round"] = round_no
                laps_df["session_type"] = session_type
                laps_df["ingestion_ts"] = ingestion_ts

                write_bronze(
                    df=laps_df,
                    table_name="laps",
                    cfg=cfg
                )

        if cfg["datasets"]["weather"]["enabled"]:
            weather = session.weather_data
            if not weather.empty:
                weather_df = weather.reset_index(drop=True)
                weather_df["season"] = season
                weather_df["event_round"] = round_no
                weather_df["session_type"] = session_type
                weather_df["ingestion_ts"] = ingestion_ts

                write_bronze(
                    df=weather_df,
                    table_name="weather",
                    cfg=cfg
                )

        if cfg["datasets"]["results"]["enabled"] and session_type == "R":
            results = session.results
            if results is not None:
                results_df = results.reset_index(drop=True)
                results_df["season"] = season
                results_df["event_round"] = round_no
                results_df["session_type"] = session_type
                results_df["ingestion_ts"] = ingestion_ts

                write_bronze(
                    df=results_df,
                    table_name="results",
                    cfg=cfg
                )

        logging.info(f"SUCCESS: Season={season}, Round={round_no}, Session={session_type}")

    except Exception as e:
        logging.error(
            f"FAILED: Season={season}, Round={round_no}, Session={session_type} | Error: {e}"
        )
        raise


def main():
    cfg = load_config("config/config.yaml")
    setup_logging(cfg)

    seasons = cfg["ingestion"]["seasons"]
    sessions = cfg["ingestion"]["sessions"]

    for season in seasons:
        schedule = fastf1.get_event_schedule(season)

        for _, event in schedule.iterrows():
            round_no = event["RoundNumber"]

            for session_type in sessions:
                ingest_session(season, round_no, session_type, cfg)


if __name__ == "__main__":
    main()
