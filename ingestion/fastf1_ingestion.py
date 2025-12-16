import fastf1
import pandas as pd
import os
import logging
from datetime import datetime

from ingestion.utils import (
    load_config,
    setup_logging,
    write_bronze
)

# =========================
# Cache Setup
# =========================
def setup_fastf1_cache(cfg: dict):
    cache_dir = cfg["fastf1"]["cache_dir"]

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        logging.info(f"Created FastF1 cache directory at {cache_dir}")

    if cfg["fastf1"]["enable_cache"]:
        fastf1.Cache.enable_cache(cache_dir)
        logging.info("FastF1 cache enabled")


# =========================
# Session Ingestion
# =========================
def ingest_session(season: int, round_no: int, session_type: str, cfg: dict):
    logging.info(
        f"Starting ingestion | Season={season}, Round={round_no}, Session={session_type}"
    )

    try:
        session = fastf1.get_session(season, round_no, session_type)
        session.load()

        ingestion_ts = datetime.utcnow()

        # -------- LAPS --------
        if cfg["datasets"]["laps"]["enabled"]:
            laps = session.laps
            if laps is not None and not laps.empty:
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

                logging.info(
                    f"LAPS ingested | rows={len(laps_df)}"
                )

        # -------- WEATHER --------
        if cfg["datasets"]["weather"]["enabled"]:
            weather = session.weather_data
            if weather is not None and not weather.empty:
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

                logging.info(
                    f"WEATHER ingested | rows={len(weather_df)}"
                )

        # -------- RESULTS (Race only) --------
        if cfg["datasets"]["results"]["enabled"] and session_type == "R":
            results = session.results
            if results is not None and not results.empty:
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

                logging.info(
                    f"RESULTS ingested | rows={len(results_df)}"
                )

        logging.info(
            f"SUCCESS | Season={season}, Round={round_no}, Session={session_type}"
        )

    except Exception as e:
        logging.error(
            f"FAILED | Season={season}, Round={round_no}, Session={session_type} | Error={e}",
            exc_info=True
        )


# =========================
# Main Orchestration
# =========================
def main():
    # Load config & logging
    cfg = load_config("config/config.yaml")
    setup_logging(cfg)

    # Setup FastF1 cache
    setup_fastf1_cache(cfg)

    seasons = cfg["ingestion"]["seasons"]
    sessions = cfg["ingestion"]["sessions"]
    max_events = cfg["ingestion"].get("max_events")

    for season in seasons:
        logging.info(f"Fetching event schedule for season {season}")
        schedule = fastf1.get_event_schedule(season)

        if schedule is None or schedule.empty:
            logging.warning(f"No events found for season {season}")
            continue

    events_processed = 0

    for _, event in schedule.iterrows():
        round_no = int(event["RoundNumber"])

        # Skip testing events
        if round_no < 1:
            logging.info("Skipping testing event (round 0)")
            continue

        if max_events is not None and events_processed >= max_events:
            logging.info("Max events limit reached, stopping early")
            break

        for session_type in sessions:
            ingest_session(
                season=season,
                round_no=round_no,
                session_type=session_type,
                cfg=cfg
            )

    events_processed += 1


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    main()
