from pathlib import Path
from typing import Literal
from logging_config import setup_logging
from process_speed_data import process_speed_data
from process_thresholded_trajectory import process_thresholded_trajectory
from setup_grid_and_background import setup_grid_and_background
from load_trajectory_data import load_trajectory_data
from transform_trajectory import transform_trajectory
from calculate_stay_time import calculate_stay_time
from calculate_stay_count import calculate_stay_count
from visualize_and_save_heatmap import visualize_and_save_heatmap
from visualize_trajectory import visualize_trajectory
from create_single_heatmap import create_single_heatmap

from generate_heatmap_data import generate_heatmap_data
from create_diff_heatmap import create_diff_heatmap
from config import trajectory_lists as cfg

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import click
import glob

plt.rcParams["font.family"] = "Hiragino Sans"


@click.command()
@click.option(
    "--csv",
    "-c",
    "csv_input",
    type=click.Path(exists=True),
    default=None,
    help="入力軌跡CSVのパスを指定すると速度・滞在情報付きCSVを作成して終了します。使用例: --csv path/to/input.csv",
)
@click.option(
    "-a",
    "--pattern-a",
    "pattern",
    flag_value="A",
    help="csvデータの処理を行う時、処理対象をグループAのデータに設定します。",
)
@click.option(
    "-b",
    "--pattern-b",
    "pattern",
    flag_value="B",
    help="csvデータの処理を行う時、処理対象をグループBのデータに設定します。",
)
@click.option(
    "-f",
    "--all-files",
    "is_all",
    is_flag=True,
    help="ヒートマップ生成時に全ての軌跡データを処理対象とします。",
)
def main(
    csv_input: str, pattern: Literal["A", "B"] | None = None, is_all: bool = False
) -> None:

    if csv_input is not None:
        # csvオプションが指定されている場合

        if is_all:
            raise click.UsageError(
                "--all-filesオプションはCSV処理時には使用できません。"
            )

        csv_pattern = pattern if pattern is not None else "A"
        logging_context = setup_logging(mode="csv", pattern=csv_pattern)
    else:
        # ヒートマップ生成の場合

        if pattern is not None:
            raise click.UsageError("--patternオプションはCSV処理時にのみ使用できます。")

        logging_context = setup_logging(mode="heatmap")

    logger = logging_context.logger
    run_dir = logging_context.run_dir

    if csv_input:

        split_path = Path(csv_input).parts
        file_name = split_path[-1]

        # 指定された入力ファイルで CSV を作成して終了
        logger.info("条件%sでCSV処理を実行します。", f"({pattern})")
        process_speed_data(
            input_csv=csv_input,
            output_csv="speed.csv",
            run_dir=run_dir,
            logger=logger,
        )

        process_thresholded_trajectory(
            input_trajectory_csv=csv_input,
            input_speed_csv="speed.csv",
            output_csv=file_name,
            run_dir=run_dir,
            logger=logger,
        )
        logger.info(
            "速度・滞在情報付きCSVを出力しました: %s, %s",
            "speed.csv",
            file_name,
        )
        return

    # 1. 基本パラメータの設定
    MAP_WIDTH_PX = 2837
    MAP_HEIGHT_PX = 3742
    GRID_SIZE_PX = 100

    # ==================================================================
    # ★ 計算モードを設定 ('count' または 'time')
    # 'count': 滞在回数でヒートマップを作成
    # 'time' : 滞在時間でヒートマップを作成
    CALCULATION_MODE = "count"
    # ==================================================================

    # 2. 背景画像とグリッド情報を準備
    background_image, grid_data, num_grids_x, num_grids_y = setup_grid_and_background(
        MAP_WIDTH_PX, MAP_HEIGHT_PX, GRID_SIZE_PX
    )

    if is_all:
        # 全ファイルを対象とする場合 input/processed 以下の全csvを対象にする
        logger.info("全ての軌跡データを処理対象とします。")
        trj_files_a = glob.glob("input/processed/A/*.csv")
        trj_files_b = glob.glob("input/processed/B/*.csv")

        TRAJECTORY_FILE_PATHS_A = (
            trj_files_a if trj_files_a else cfg.TRAJECTORY_FILE_PATHS_A
        )
        TRAJECTORY_FILE_PATHS_B = (
            trj_files_b if trj_files_b else cfg.TRAJECTORY_FILE_PATHS_B
        )
    else:
        logger.info("設定ファイルの軌跡データを処理対象とします。")
        # 通常は設定ファイルの内容を使う
        TRAJECTORY_FILE_PATHS_A = cfg.TRAJECTORY_FILE_PATHS_A
        TRAJECTORY_FILE_PATHS_B = cfg.TRAJECTORY_FILE_PATHS_B

    # # 3. 処理対象の軌跡データと、それに対応する変換パラメータを設定
    TRANSFORM_PARAMS_A = cfg.DEFAULT_TRANSFORM_PARAM
    # 座標変換パラメータ
    TRANSFORM_PARAMS_B = cfg.DEFAULT_TRANSFORM_PARAM

    print(len(TRAJECTORY_FILE_PATHS_A))
    print(len(TRAJECTORY_FILE_PATHS_B))

    logger.info("Aのヒートマップを生成します。")
    heatmap_A = generate_heatmap_data(
        TRAJECTORY_FILE_PATHS_A,
        TRANSFORM_PARAMS_A,
        grid_data,
        background_image,
        num_grids_x,
        num_grids_y,
        calc_mode=CALCULATION_MODE,
        logger=logger,
    )
    logger.info("Bのヒートマップを生成します。")
    heatmap_B = generate_heatmap_data(
        TRAJECTORY_FILE_PATHS_B,
        TRANSFORM_PARAMS_B,
        grid_data,
        background_image,
        num_grids_x,
        num_grids_y,
        calc_mode=CALCULATION_MODE,
        logger=logger,
    )
    ## グループAの単体ヒートマップを可視化
    create_single_heatmap(
        heatmap_data=heatmap_A,
        background_image=background_image,
        colorbar_label="グループAの滞在回数",
        logger=logger,
        run_dir=Path(run_dir, "heatmap_A.png"),
    )
    ## グループBの単体ヒートマップを可視化
    create_single_heatmap(
        heatmap_data=heatmap_B,
        background_image=background_image,
        colorbar_label="グループBの滞在回数",
        logger=logger,
        run_dir=Path(run_dir, "heatmap_B.png"),
    )

    create_diff_heatmap(
        heatmap_data_A=heatmap_A,
        heatmap_data_B=heatmap_B,
        background_image=background_image,
        colorbar_label=f"滞在{'回数' if CALCULATION_MODE == 'count' else '時間'}の差 (B-A)",
        logger=logger,
        run_dir=Path(run_dir, "differential_heatmap.png"),
    )


if __name__ == "__main__":
    main()
