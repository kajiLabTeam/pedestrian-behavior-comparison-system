from __future__ import annotations
import logging
from pathlib import Path
from typing import Iterable
import numpy as np
import pandas as pd


def process_speed_data(
    input_csv: Path | str,
    output_csv: Path | str,
    *,
    run_dir: Path | str | None = None,
    logger: logging.Logger | None = None,
) -> None:
    input_path = Path(input_csv)

    if logger is None:
        logger = logging.getLogger(__name__)
    log = logger

    if run_dir is not None:
        output_path = Path(run_dir) / Path(output_csv).name
    else:
        output_path = Path(output_csv)

    df = pd.read_csv(input_path)
    required_columns: Iterable[str] = {"time", "x", "y"}
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"CSV file missing required columns: {sorted(missing_columns)}"
        )

    dt = df["time"].diff().replace(0, np.nan)
    dx = df["x"].diff()
    dy = df["y"].diff()
    ds = np.hypot(dx, dy)
    speed = pd.Series(ds / dt)

    df_speed = pd.DataFrame(
        {
            "time": df["time"].iloc[1:].reset_index(drop=True),
            "speed": speed.iloc[1:].reset_index(drop=True),
        }
    )

    window_speed = 5
    df_speed["low_speed"] = df_speed["speed"].rolling(window=window_speed).mean()

    log.info("Computed speed data for %s (%d rows)", input_path, len(df_speed))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_speed.to_csv(output_path, index=False)
    log.info("Saved speed CSV to %s", output_path)
