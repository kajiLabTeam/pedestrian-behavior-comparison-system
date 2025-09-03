
from setup_grid_and_background import setup_grid_and_background
from load_trajectory_data import load_trajectory_data
from transform_trajectory import transform_trajectory
from calculate_stay_time import calculate_stay_time

from PIL import Image, ImageDraw, ImageFont
import	numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'Hiragino Sans'
if __name__ == '__main__':
    
    # 1. 基本パラメータの設定
    MAP_WIDTH_PX = 2837
    MAP_HEIGHT_PX = 3742
    GRID_SIZE_PX = 100
    
    # 2. 背景画像とグリッド情報を準備
    background_image, grid_data, num_grids_x, num_grids_y = setup_grid_and_background(
        MAP_WIDTH_PX, MAP_HEIGHT_PX, GRID_SIZE_PX
    )
    
    print("画像を表示します。")
    background_image.show()
    
    
    # # 3. 処理対象の軌跡データと、それに対応する変換パラメータを設定
    TRAJECTORY_FILE_PATH = "./grid/data/threshold_trajectory_data.csv"
    
    # 座標変換パラメータ
    TRANSFORM_PARAMS = {
        'scale': 1.0,         #x 1mあたり1pxに変換
        'angle_deg': 180.0,     # 180度回転
        'initial_position': (14, 21) # 軌跡の開始地点
    }
    
    OUTPUT_IMAGE_PATH = "output/heatmap_result.png"

    # # 4. 一連の処理を実行
    # # 軌跡データの読み込み
    df_trajectory = load_trajectory_data(TRAJECTORY_FILE_PATH)
    
    # # 座標変換
    df_transformed = transform_trajectory(
        df_trajectory,
        TRANSFORM_PARAMS['scale'],
        TRANSFORM_PARAMS['angle_deg'],
        TRANSFORM_PARAMS['initial_position'],
        grid_data,
        GRID_SIZE_PX,
        background_image,
		MAP_WIDTH_PX,
		MAP_HEIGHT_PX
    )
    
    # 滞在時間の計算
    
    stay_times = calculate_stay_time(
		df_trajectory,
		MAP_WIDTH_PX,   # マップ幅を追加
		MAP_HEIGHT_PX,  # マップ高さを追加
		GRID_SIZE_PX    # グリッドサイズを追加
    )
    
    # # 結果の可視化と保存
    # visualize_and_save_heatmap(
    #     stay_times,
    #     background_image,
    #     num_grids_x,
    #     num_grids_y,
    #     MAP_WIDTH_PX,
    #     MAP_HEIGHT_PX,
    #     OUTPUT_IMAGE_PATH
    # )