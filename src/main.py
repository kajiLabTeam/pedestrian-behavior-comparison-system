
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
    TRAJECTORY_FILE_PATHS_A = [
        "./part/3_straight_sit/data/threshold_trajectory_data.csv" 
     # "./part/2_straight_quick_sit/data/threshold_trajectory_data.csv" 

    ] 

    TRANSFORM_PARAMS_A = [
        {
            'scale': 1.0,         #x 1mあたり1pxに変換
            'angle_deg':180.0,
            'initial_position': (10, 21) # 軌跡の開始
        },

    ]

    TRAJECTORY_FILE_PATHS_B = [       
        "output_trajectories/demo/take4_4Hz/threshold_trajectory_data.csv"
    ] 
 

    # 座標変換パラメータ
    TRANSFORM_PARAMS_B = [

        {
            'scale': 1.0,         #x 1mあたり1pxに変換
            'angle_deg':0.0,     
            'initial_position': (6, 28) # 軌跡の開始
        },
    ]
    print(len(TRAJECTORY_FILE_PATHS_A))
    print(len(TRAJECTORY_FILE_PATHS_B))
    
    heatmap_A = generate_heatmap_data(TRAJECTORY_FILE_PATHS_A, TRANSFORM_PARAMS_A,grid_data, background_image, num_grids_x, num_grids_y,calc_mode=CALCULATION_MODE)    
    heatmap_B = generate_heatmap_data(TRAJECTORY_FILE_PATHS_B, TRANSFORM_PARAMS_B,grid_data, background_image, num_grids_x, num_grids_y,calc_mode=CALCULATION_MODE) 

    ## グループAの単体ヒートマップを可視化
    create_single_heatmap(
        heatmap_data=heatmap_A,
        background_image=background_image,
        output_path="./output/heatmap_A.png",
        colorbar_label="グループAの滞在回数"    
    )
    ## グループBの単体ヒートマップを可視化
    create_single_heatmap(
        heatmap_data=heatmap_B,
        background_image=background_image,
        output_path="./output/heatmap_B.png",
        colorbar_label="グループBの滞在回数"    
    )


    create_diff_heatmap(
        heatmap_data_A=heatmap_A,
        heatmap_data_B=heatmap_B,
        background_image=background_image,
        output_path="./output/differential_heatmap.png",
        colorbar_label=f"滞在{'回数' if CALCULATION_MODE == 'count' else '時間'}の差 (A - B)"
    )