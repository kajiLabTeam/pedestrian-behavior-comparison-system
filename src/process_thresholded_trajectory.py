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
    """軌跡 CSV と速度 CSV を結合し、しきい値で滞在フラグを付けた CSV を出力する。

     概要
     ----
     指定した軌跡 CSV（`time`, `x`, `y` を含む）と、速度情報が入った CSV
    （`time`, `speed` を含む）を `time` 列で結合します。結合後、速度が
     `threshold` 以下であれば `stay=True` を設定し、結果を CSV として書き出します。

     パラメータ
     --------
     input_trajectory_csv:
         入力軌跡 CSV のパス（`Path` または `str`）。`time`, `x`, `y` 列が必要です。
     input_speed_csv:
         入力速度 CSV のパス（`Path` または `str`）。`time`, `speed` 列が必要です。
         実行時に `run_dir` を指定した場合、この関数は `Path(run_dir) / Path(input_speed_csv).name`
         を読み取ります（出力と同じ実行ディレクトリに速度 CSV を置いてある想定）。
     output_csv:
         出力先のファイル名またはパス（`Path` または `str`）。`run_dir` が指定されると
         `Path(run_dir) / Path(output_csv).name` に書き出されます。
     threshold:
         速度の閾値（inclusive）。この値以下の点を滞在（stay）と見なします。

     キーワード引数
     --------
     run_dir:
         実行ごとの出力ディレクトリ（`Path` または `str`）。指定すれば出力はその配下に保存されます。
     logger:
         使用する `logging.Logger`。省略時はモジュールロガーが使われます。

     例外
     ----
     必要な列が揃っていない場合は `ValueError` を送出します。
    """

    traj_path = Path(input_trajectory_csv)
    speed_path = Path(input_speed_csv)

    if logger is None:
        logger = logging.getLogger(__name__)
    log = logger

    if run_dir is not None:
        out_path = Path(run_dir) / Path(output_csv).name
    else:
        out_path = Path(output_csv)

    # csvファイルの読み込み（失敗時にログ出力して再送出）
    try:
        df_traj = pd.read_csv(traj_path)
        log.info("軌跡CSVを読み込みました: %s (%d行)", traj_path, len(df_traj))
    except Exception:
        log.exception("軌跡CSVの読み込みに失敗しました: %s", traj_path)
        raise

    speed_full_path = Path(f"{run_dir}/{speed_path.name}")
    try:
        df_speed = pd.read_csv(speed_full_path)
        log.info("速度CSVを読み込みました: %s (%d行)", speed_full_path, len(df_speed))
    except Exception:
        log.exception("速度CSVの読み込みに失敗しました: %s", speed_full_path)
        raise

    required_traj = {"time", "x", "y"}
    required_speed = {"time", "speed"}
    missing_traj = required_traj - set(df_traj.columns)
    missing_speed = required_speed - set(df_speed.columns)
    if missing_traj:
        # 短い警告ログを出力してから例外を送出
        log.warning("軌跡CSVに必要な列がありません: %s", sorted(missing_traj))
        raise ValueError(f"軌跡CSVに必要な列がありません: {sorted(missing_traj)}")
    if missing_speed:
        log.warning("速度CSVに必要な列がありません: %s", sorted(missing_speed))
        raise ValueError(f"速度CSVに必要な列がありません: {sorted(missing_speed)}")

    # Merge speed into trajectory on time
    df = pd.merge(df_traj, df_speed[["time", "speed"]], on="time", how="left")

    # Mark stays
    df["stay"] = df["speed"] <= threshold

    # 出力CSVの書き出し（失敗時はログ出力して再送出）
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_path, index=False)
        log.info("閾値処理済み軌跡CSVを保存しました: %s", out_path)
    except Exception:
        log.exception("閾値処理済み軌跡CSVの書き出しに失敗しました: %s", out_path)
        raise
