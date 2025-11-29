from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd


def process_thresholded_trajectory(
    input_trajectory_csv: Path | str,
    input_speed_csv: Path | str,
    output_csv: Path | str,
    threshold: float = 0.5,
) -> None:
    traj_path = Path(input_trajectory_csv)
    speed_path = Path(input_speed_csv)
    out_path = Path(output_csv)

    # csvファイルの読み込み
    df_traj = pd.read_csv(traj_path)
    df_speed = pd.read_csv(speed_path)

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

    # Ensure output dir exists
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
