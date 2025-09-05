import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def visualize_and_save_heatmap(stay_time_per_grid, background_img, num_grids_x, num_grids_y, map_width_px, map_height_px, output_path, colorbar_label):
    """
    滞在時間データをヒートマップとして可視化し、画像として保存する。

    Args:
        stay_time_per_grid (pd.Series): グリッドごとの滞在時間
        background_img (PIL.Image): 背景画像
        num_grids_x (int): 横グリッド数
        num_grids_y (int): 縦グリッド数
        map_width_px (int): マップの幅
        map_height_px (int): マップの高さ
        output_path (str): 保存する画像のパス
    """
    print(f"\n--- ヒートマップの可視化と保存: {output_path} ---")

    #   # forループを以下のように修正
    # for grid_id, total_time in stay_time_per_grid.items():
    #     # grid_idが2つの要素を持つタプルであるかを確認
    #     if isinstance(grid_id, tuple) and len(grid_id) == 2:
    #         # このチェックを通過すれば、安全にアンパックできる
    #         col, row = grid_id
            
    #         # 範囲内の場合のみデータを更新
    #         if 0 <= row < num_grids_y and 0 <= col < num_grids_x:
    #             heatmap_data[row, col] = total_time
    #     else:
    #         # 予期せぬ形式のgrid_id（Noneなど）を無視し、警告を表示する
    #         print(f"範囲外または予期せぬgrid_idをスキップしました: {grid_id}")

    fig, ax = plt.subplots(figsize=(10,10), dpi=100)
    ax.imshow(background_img, extent=[0, map_width_px, map_height_px, 0])

    heatmap = ax.imshow(
        stay_time_per_grid, 
        cmap='rainbow', 
        alpha=0.6, 
        extent=[0, map_width_px, map_height_px, 0],
    )
    
    # ★引数で受け取ったラベルをカラーバーに設定
    cbar = fig.colorbar(heatmap, ax=ax, label=colorbar_label, shrink=0.8)
    ax.set_title('各グリッドにおける滞在時間のヒートマップ', fontsize=10)
    ax.set_xlabel('幅[px]', fontsize=10)
    ax.set_ylabel('高さ[px]', fontsize=10)
    ax.set_xlim(0, map_width_px)
    ax.set_ylim(map_height_px, 0)

    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.show()