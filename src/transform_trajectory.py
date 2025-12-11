import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def transform_trajectory(
    df_trajectory,
    scale,
    correct_angle,
    initial_position,
    grid_data,
    grid_size,
    img,
    map_width,
    map_height,
):
    # 1. スケール補正係数と最終的なスケールを計算
    final_scale = 100 * scale

    df_trajectory["x_scaled"] = df_trajectory["x"] * final_scale
    df_trajectory["y_scaled"] = df_trajectory["y"] * final_scale

    # 2. 回転行列を用いて座標を回転
    angle_rad = np.deg2rad(correct_angle)
    cos_theta = np.cos(angle_rad)
    sin_theta = np.sin(angle_rad)

    df_trajectory["x_rotated"] = (
        df_trajectory["x_scaled"] * cos_theta - df_trajectory["y_scaled"] * sin_theta
    )
    df_trajectory["y_rotated"] = (
        df_trajectory["x_scaled"] * sin_theta + df_trajectory["y_scaled"] * cos_theta
    )

    # 原点を軌跡の開始点に合わせる
    df_trajectory["x_rotated"] -= df_trajectory["x_rotated"].iloc[0]
    df_trajectory["y_rotated"] -= df_trajectory["y_rotated"].iloc[0]

    start_grid_info = next(item for item in grid_data if item["id"] == initial_position)
    offset_x = start_grid_info["x_min"] + grid_size / 2
    offset_y = start_grid_info["y_min"] + grid_size / 2
    df_trajectory["x_final"] = df_trajectory["x_rotated"] + offset_x
    df_trajectory["y_final"] = df_trajectory["y_rotated"] + offset_y

    # プロットの設定
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img, extent=[0, map_width, map_height, 0])

    # 'time' 列を明示的に float 型（数値）に変換する
    c_values = df_trajectory["time"].astype(float)

    # 変換した c_values を c 引数に渡す
    scatter = ax.scatter(
        df_trajectory["x_final"],
        df_trajectory["y_final"],
        c=c_values,
        cmap="rainbow",
        s=40,
        label="歩行軌跡",
        zorder=2,
    )

    fig.colorbar(scatter, ax=ax, label="Time")

    # グラフの装飾
    plt.title("歩行軌跡をフロアマップにマッピングした結果", fontsize=24)
    plt.xlabel("幅[px]", fontsize=18)
    plt.ylabel("高さ[px]", fontsize=18)
    plt.legend(fontsize=16)
    # plt.show()
    plt.close(fig)

    return df_trajectory
