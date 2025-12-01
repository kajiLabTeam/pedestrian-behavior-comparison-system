import logging
from load_trajectory_data import load_trajectory_data
from transform_trajectory import transform_trajectory
from calculate_stay_time import calculate_stay_time
from calculate_stay_count import calculate_stay_count
from visualize_trajectory import visualize_trajectory


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

MAP_WIDTH_PX = 2837
MAP_HEIGHT_PX = 3742
GRID_SIZE_PX = 100


def generate_heatmap_data(
    file_paths,
    transform_params_list,
    grid_data,
    background_image,
    num_grids_x,
    num_grids_y,
    calc_mode="count",
    logger=None,
):

    if logger is None:
        logger = logging.getLogger(__name__)
    log = logger
    log.info("ヒートマップデータの生成を開始します。")

    # 全軌跡の値を合算するための配列をゼロで初期化
    total_values = np.zeros((num_grids_y, num_grids_x))
    transformed_list = []

    for file_path, transform_params in zip(file_paths, transform_params_list):
        log.info(
            "(%s,%s)軌跡データの処理を開始します: %s",
            file_paths.index(file_path) + 1,
            len(file_paths),
            file_path,
        )
        df_trajectory = load_trajectory_data(file_path)

        # # 座標変換
        df_transformed = transform_trajectory(
            df_trajectory,
            transform_params["scale"],
            transform_params["angle_deg"],
            transform_params["initial_position"],
            grid_data,
            GRID_SIZE_PX,
            background_image,
            MAP_WIDTH_PX,
            MAP_HEIGHT_PX,
        )

        transformed_list.append(df_transformed)

        if calc_mode == "time":
            # 滞在時間の計算
            calculated_values = calculate_stay_time(
                df_transformed,
                GRID_SIZE_PX,
                MAP_WIDTH_PX,
                MAP_HEIGHT_PX,
            )
            colorbar_label = "滞在時間 (秒)"

        elif calc_mode == "count":
            calculated_values = calculate_stay_count(
                df_transformed,
                GRID_SIZE_PX,
            )
            colorbar_label = "滞在回数"

        # 計算結果を合算する
        for grid_id, value in calculated_values.items():
            col, row = grid_id
            if 0 <= row < total_values.shape[0] and 0 <= col < total_values.shape[1]:
                total_values[row, col] += value

        log.info(
            "(%s,%s)軌跡データの処理が完了しました: %s",
            file_paths.index(file_path) + 1,
            len(file_paths),
            file_path,
        )
        visualize_trajectory(
            df_list=transformed_list,
            background_image=background_image,
            map_width=MAP_WIDTH_PX,
            map_height=MAP_HEIGHT_PX,
            output_dir="output",
        )

    return total_values
