from setup_grid_and_background import setup_grid_and_background
from PIL import Image, ImageDraw, ImageFont
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
    TRAJECTORY_FILE_PATH = "data/threshold_trajectory_data.csv"
    
    # # 座標変換パラメータ
    # TRANSFORM_PARAMS = {
    #     'scale': 100.0,         # 1mあたり100pxに変換
    #     'angle_deg': 180.0,     # 180度回転
    #     'start_grid_id': (14, 21) # 軌跡の開始地点
    # }
    
    # OUTPUT_IMAGE_PATH = "output/heatmap_result.png"

    # # 4. 一連の処理を実行
    # # 軌跡データの読み込み
    # df_traj = load_trajectory_data(TRAJECTORY_FILE_PATH)
    
    # # 座標変換
    # df_transformed = transform_trajectory(
    #     df_traj,
    #     TRANSFORM_PARAMS['scale'],
    #     TRANSFORM_PARAMS['angle_deg'],
    #     TRANSFORM_PARAMS['start_grid_id'],
    #     grid_data,
    #     GRID_SIZE_PX
    # )
    
    # # 滞在時間の計算
    # stay_times = calculate_stay_time(
    #     df_transformed,
    #     GRID_SIZE_PX,
    #     MAP_WIDTH_PX,
    #     MAP_HEIGHT_PX
    # )
    
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