
from setup_grid_and_background import setup_grid_and_background
from load_trajectory_data import load_trajectory_data
from transform_trajectory import transform_trajectory
from calculate_stay_time import calculate_stay_time
from calculate_stay_count import calculate_stay_count
from visualize_and_save_heatmap import visualize_and_save_heatmap
from visualize_trajectory import visualize_trajectory

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

    # ==================================================================
    # ★ 計算モードを設定 ('count' または 'time')
    # 'count': 滞在回数でヒートマップを作成
    # 'time' : 滞在時間でヒートマップを作成
    CALCULATION_MODE = 'count'
    # ==================================================================
    
    # 2. 背景画像とグリッド情報を準備
    background_image, grid_data, num_grids_x, num_grids_y = setup_grid_and_background(
        MAP_WIDTH_PX, MAP_HEIGHT_PX, GRID_SIZE_PX
    )    
    
    # # 3. 処理対象の軌跡データと、それに対応する変換パラメータを設定
    TRAJECTORY_FILE_PATHS = [
        "./grid/data/threshold_trajectory_data.csv",
        "./speed/slowly/data/threshold_trajectory_data.csv",
    ] 
    # 座標変換パラメータ
    TRANSFORM_PARAMS_LIST = [
        {
            'scale': 1.0,         #x 1mあたり1pxに変換
            'angle_deg': 180.0,     # 180度回転
            'initial_position': (14, 21) # 軌跡の開始地点
        },
        {
            'scale': 1.0,         #x 1mあたり1pxに変換
            'angle_deg':180.0,     # 180度回転
            'initial_position': (8, 21) # 軌跡の開始
        }
    ]
    
    OUTPUT_IMAGE_PATH = "./grid/output/heatmap_result.png"

    
    ##  全軌跡の滞在時間を合算するための配列をゼロで初期化
    # total_stay_times = np.zeros((num_grids_y, num_grids_x))
    # 全軌跡の値を合算するための配列をゼロで初期化
    total_values = np.zeros((num_grids_y, num_grids_x))
        
    
    for file_path, transform_params in zip(TRAJECTORY_FILE_PATHS, TRANSFORM_PARAMS_LIST):
        print(f"Processing file: {file_path} with transform params: {transform_params}")
        df_trajectory = load_trajectory_data(file_path)

        # # 座標変換
        df_transformed = transform_trajectory(
            df_trajectory,
            transform_params['scale'],
            transform_params['angle_deg'],
            transform_params['initial_position'],
            grid_data,
            GRID_SIZE_PX,
            background_image,
            MAP_WIDTH_PX,
            MAP_HEIGHT_PX
        )

        print(f"df_transformed'{ df_transformed}")

        visualize_trajectory(
            df=df_transformed,
            background_image=background_image,
            map_width=MAP_WIDTH_PX,
            map_height=MAP_HEIGHT_PX
        )

        if CALCULATION_MODE == 'time':
                # 滞在時間の計算
            calculated_values = calculate_stay_time(
                df_transformed,
                GRID_SIZE_PX,
                MAP_WIDTH_PX,  
                MAP_HEIGHT_PX,
                
            )
            colorbar_label = "滞在時間 (秒)"

        elif CALCULATION_MODE == 'count':
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
    

    # 結果の可視化と保存
    visualize_and_save_heatmap(
        # total_stay_times,
        total_values,
        background_image,
        num_grids_x,
        num_grids_y,
        MAP_WIDTH_PX,
        MAP_HEIGHT_PX,
        OUTPUT_IMAGE_PATH,
        colorbar_label=colorbar_label
    )
    
