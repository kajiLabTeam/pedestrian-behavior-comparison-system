import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def calculate_stay_time(
    df_trajectory, grid_size, map_width, map_height, excluded_grids=None
):
    # diff()で前後の行との差を計算し、最初の行はNaNになるため0で埋める
    df_trajectory["time_diff"] = df_trajectory["time"].diff().fillna(0)

    def find_grid_id(x, y, grid_size, map_width_px, map_height_px):
        """
        座標(x, y)がどのグリッドIDに属するかを計算する。
        マップ範囲外の場合は-1を返す。
        """
        # print(f"x: {x}, y: {y},grid_size{grid_size}, map_width_px: {map_width_px}, map_height_px: {map_height_px}")
        if not (0 <= x < map_width_px and 0 <= y < map_height_px):
            return -1  # マップの範囲外

        # 座標がどのグリッドの列・行に位置するかを計算
        grid_col = int(x // grid_size)
        grid_row = int(y // grid_size)

        return (grid_col, grid_row)

    df_trajectory["grid_id"] = df_trajectory.apply(
        lambda row: find_grid_id(
            row["x_final"], row["y_final"], grid_size, map_width, map_height
        ),
        axis=1,
    )
    # 'stay'がTrueで、かつ有効なグリッドIDを持つデータのみをフィルタリング
    stay_points = df_trajectory[
        (df_trajectory["stay"] == True) & (df_trajectory["grid_id"].notna())
    ].copy()

    if excluded_grids:
        excluded_set = {grid for grid in excluded_grids if grid is not None}
        if excluded_set:
            stay_points = stay_points[~stay_points["grid_id"].isin(excluded_set)].copy()
            if stay_points.empty:
                return {}

    # グリッドIDごとに滞在時間('time_diff')を合計
    stay_time_per_grid = stay_points.groupby("grid_id")["time_diff"].sum()
    if stay_time_per_grid.empty:
        return {}

    # 結果の表示 (滞在時間があったグリッドのみ)
    # print("--- グリッドごとの滞在時間 ---")
    # print(stay_time_per_grid[stay_time_per_grid > 0])
    # print("-" * 20)

    return stay_time_per_grid.to_dict()
