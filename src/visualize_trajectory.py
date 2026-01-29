import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np


def visualize_trajectory(df_list, background_image, map_width, map_height, output_dir="output", group_label=""):
    """
    複数の軌跡データフレームを背景画像上に重ねてプロットし、単一の画像として保存する。

    Args:
        df_list (list): 座標変換後の軌跡データフレーム(pd.DataFrame)のリスト。
        background_image (PIL.Image): プロットの背景として使用する画像。
        map_width (int): マップの幅 (ピクセル)。
        map_height (int): マップの高さ (ピクセル)。
        output_dir (str): 出力ディレクトリ。
        group_label (str): グループラベル（'A'または'B'）。
    """
    # 呼び出し回数をカウントする
    if not hasattr(visualize_trajectory, "call_count"):
        visualize_trajectory.call_count = 0
    
    suffix = group_label if group_label else ("A" if visualize_trajectory.call_count % 2 == 0 else "B")
    visualize_trajectory.call_count += 1
    

    fig, ax = plt.subplots(figsize=(map_width / 100, map_height / 100), dpi=100)
    ax.imshow(background_image, extent=[0, map_width, map_height, 0])

    # 各軌跡を色分けするためのカラーマップ
    colors = plt.cm.jet(np.linspace(0, 1, len(df_list)))

    for i, df in enumerate(df_list):
        if df.empty or 'x_final' not in df or 'y_final' not in df:
            print(f"有効なデータがないため、プロットをスキップします。 index={i}")
            continue

        # 'stay'の値でデータをフィルタリング（欠損値も除去）
        df_filtered = df.dropna(subset=['x_final', 'y_final', 'stay'])
        stay_true = df_filtered[df_filtered['stay'] == True]
        stay_false = df_filtered[df_filtered['stay'] == False]
        
        # 軌跡ごとに異なる色でプロット
        color = colors[i]
        
        if not stay_false.empty:
            ax.scatter(stay_false['x_final'], stay_false['y_final'], 
                       c=[color], s=50, label=f'Trajectory {i+1} (移動中)', zorder=2, alpha=0.6)
        if not stay_true.empty:
            ax.scatter(stay_true['x_final'], stay_true['y_final'], 
                       c='red', s=70, label=f'Trajectory {i+1} (滞在中)', zorder=3, alpha=0.8)

    # グラフの装飾
    ax.set_title(f'全軌跡のマッピング結果 (グループ{suffix})', fontsize=18)
    ax.set_xlabel('幅[px]', fontsize=14)
    ax.set_ylabel('高さ[px]', fontsize=14)
    ax.set_xlim(0, map_width)
    ax.set_ylim(map_height, 0)
    
    # プロットされたデータがある場合のみ凡例を表示
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(handles, labels, fontsize=12, title="凡例")

    # レイアウトを整えて保存
    fig.tight_layout()
    filename = f"trajectory_combined_{suffix}.png"
    out_path = os.path.join(output_dir, filename)
    plt.savefig(out_path, dpi=300)
    plt.close(fig)
