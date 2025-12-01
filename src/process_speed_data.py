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
    """CSV（軌跡）から速度を計算して CSV を出力する関数。

    概要
    ----
    与えられた軌跡 CSV（`time`, `x`, `y` 列を含む）を読み込み、隣接点間の
    距離を時間差で割ることで速度を計算します。計算結果は `time`, `speed`,
    `low_speed`（移動平均，window=5）を含む CSV として書き出されます。

    パラメータ
    --------
    input_csv:
        入力軌跡 CSV のパス（`Path` または `str`）。列 `time`, `x`, `y` を含む必要があります。
    output_csv:
        出力 CSV のパスまたはファイル名（`Path` または `str`）。
        `run_dir` が指定された場合は `Path(run_dir) / Path(output_csv).name` に書き出します。

    キーワード引数
    --------
    run_dir:
        実行ごとの出力ディレクトリ（`Path` または `str`）。省略時は `output_csv` のパスが使われます。
    logger:
        出力に使用する `logging.Logger`。省略した場合はモジュールロガーが使われます。

    例外
    ----
    必要な列（`time`, `x`, `y`）が存在しない場合は `ValueError` を送出します。

    例
    --
    process_speed_data(
        "input/trajectory.csv",
        "speed.csv",
        run_dir=logging_context.run_dir,
        logger=logging_context.logger,
    )
    """

    input_path = Path(input_csv)

    if logger is None:
        logger = logging.getLogger(__name__)
    log = logger

    if run_dir is not None:
        output_path = Path(run_dir) / Path(output_csv).name
    else:
        output_path = Path(output_csv)

    # 入力CSVの読み込み（失敗時はログ出力して再送出）
    try:
        df = pd.read_csv(input_path)
        log.info("CSVを読み込みました: %s (%d行)", input_path, len(df))
    except Exception:
        log.exception("軌跡CSVの読み込みに失敗しました: %s", input_path)
        raise

    required_columns: Iterable[str] = {"time", "x", "y"}
    missing_columns = set(required_columns) - set(df.columns)
    
    if missing_columns:
        log.warning("軌跡CSVに必要な列がありません: %s", sorted(missing_columns))
        raise ValueError(f"CSVに必要な列が不足しています: {sorted(missing_columns)}")

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
    # 速度データの計算完了ログ
    log.info("速度データを計算しました: %s (%d行)", input_path, len(df_speed))

    # 出力CSVの書き出し（失敗時はログ出力して再送出）
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df_speed.to_csv(output_path, index=False)
        log.info("スピードのCSVを保存しました: %s", output_path)
    except Exception:
        log.exception("速度CSVの書き出しに失敗しました: %s", output_path)
        raise