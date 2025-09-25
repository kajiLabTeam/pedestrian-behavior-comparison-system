
from setup_grid_and_background import setup_grid_and_background
from load_trajectory_data import load_trajectory_data
from transform_trajectory import transform_trajectory
from calculate_stay_time import calculate_stay_time
from calculate_stay_count import calculate_stay_count
from visualize_and_save_heatmap import visualize_and_save_heatmap
from visualize_trajectory import visualize_trajectory

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
        "./grid/data/threshold_trajectory_data.csv",
        "./speed/slowly/data/threshold_trajectory_data.csv",
    ] 

    TRANSFORM_PARAMS_A = [

       {
            'scale': 1.0,         #x 1mあたり1pxに変換
            'angle_deg': 180.0,     # 180度回転
            'initial_position': (14, 21) # 軌跡の開始地点
        },
        {
            'scale': 1.0,         #x 1mあたり1pxに変換
            'angle_deg':180.0,     # 180度回転
            'initial_position': (8, 21) # 軌跡の開始
        },
    ]

    TRAJECTORY_FILE_PATHS_B = [
        "./part/1_straight_sit_quick/data/threshold_trajectory_data.csv",
        "./part/2_straight_quick_sit/data/threshold_trajectory_data.csv",
        "./part/3_straight_sit/data/threshold_trajectory_data.csv" 
    ] 
 

    # 座標変換パラメータ
    TRANSFORM_PARAMS_B = [
 
        {
            'scale': 1.0,         #x 1mあたり1pxに変換
            'angle_deg':-90.0,     
            'initial_position': (10, 21) # 軌跡の開始
        },
        {
            'scale': 1.0,         #x 1mあたり1pxに変換
            'angle_deg':-90.0,     
            'initial_position': (12, 21) # 軌跡の開始
        },
        {
            'scale': 1.0,         #x 1mあたり1pxに変換
            'angle_deg':180.0,     
            'initial_position': (10, 21) # 軌跡の開始
        },

    ]
    
    heatmap_A = generate_heatmap_data(TRAJECTORY_FILE_PATHS_A, TRANSFORM_PARAMS_B,grid_data, background_image, num_grids_x, num_grids_y,calc_mode='count')    
    heatmap_B = generate_heatmap_data(TRAJECTORY_FILE_PATHS_B, TRANSFORM_PARAMS_B,grid_data, background_image, num_grids_x, num_grids_y,calc_mode='count',) 

    create_diff_heatmap(
        heatmap_data_A=heatmap_A,
        heatmap_data_B=heatmap_B,
        background_image=background_image,
        output_path="./output/differential_heatmap.png",
        colorbar_label=f"滞在{'回数' if CALCULATION_MODE == 'count' else '時間'}の差 (A - B)"
    )