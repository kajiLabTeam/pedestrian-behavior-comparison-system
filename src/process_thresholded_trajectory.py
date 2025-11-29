from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd


def process_thresholded_trajectory(
    input_trajectory_csv: Path | str,
    input_speed_csv: Path | str,
    output_csv: Path | str,
    threshold: float = 0.5,
    *,
    run_dir: Path | str | None = None,
    logger: logging.Logger | None = None,
) -> None:
    traj_path = Path(input_trajectory_csv)
    speed_path = Path(input_speed_csv)

    print(traj_path, speed_path)

    if logger is None:
        logger = logging.getLogger(__name__)
    log = logger

    if run_dir is not None:
        out_path = Path(run_dir) / Path(output_csv).name
    else:
        out_path = Path(output_csv)

    # csvファイルの読み込み
    df_traj = pd.read_csv(traj_path)
    speed_full_path = Path(f"{run_dir}/{speed_path.name}")
    df_speed = pd.read_csv(speed_full_path)

    required_traj = {"time", "x", "y"}
    required_speed = {"time", "speed"}
    missing_traj = required_traj - set(df_traj.columns)
    missing_speed = required_speed - set(df_speed.columns)
    if missing_traj:
        raise ValueError(f"trajectory CSV missing columns: {sorted(missing_traj)}")
    if missing_speed:
        raise ValueError(f"speed CSV missing columns: {sorted(missing_speed)}")

    # Merge speed into trajectory on time
    df = pd.merge(df_traj, df_speed[["time", "speed"]], on="time", how="left")

    # Mark stays
    df["stay"] = df["speed"] <= threshold

    log.info(
        "Merged trajectory (%s) with speed (%s); writing thresholded CSV to %s",
        traj_path,
        speed_path,
        out_path,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    log.info("Saved thresholded trajectory CSV to %s", out_path)
