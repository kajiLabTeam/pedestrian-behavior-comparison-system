import pandas as pd
import matplotlib.pyplot as plt

def visualize_trajectories(df, background_image, map_width, map_height):
    """
    複数の軌跡データフレームを結合し、背景画像上にプロットして保存する。

    Args:
        all_dfs (list): 座標変換後の軌跡データフレーム(pd.DataFrame)のリスト。
        background_image (PIL.Image): プロットの背景として使用する画像。
        map_width (int): マップの幅 (ピクセル)。
        map_height (int): マップの高さ (ピクセル)。
        output_path (str): プロット画像の保存先ファイルパス。
    """
    if df.empty or 'x_final' not in df or 'y_final' not in df:
        print("有効なデータがないため、プロットをスキップします。")
        return

    # プロットの準備
    fig, ax = plt.subplots(figsize=(map_width / 100, map_height / 100), dpi=100)
    ax.imshow(background_image, extent=[0, map_width, map_height, 0])

    # 'stay'の値でデータをフィルタリング

    # 'stay'の値でデータをフィルタリング（欠損値も除去）
    df_filtered = df.dropna(subset=['x_final', 'y_final', 'stay'])
    stay_true = df_filtered[df_filtered['stay'] == True]
    stay_false = df_filtered[df_filtered['stay'] == False]

 # stayの値で色分けして散布図をプロット
    if not stay_false.empty:
        ax.scatter(stay_false['x_final'], stay_false['y_final'], 
                   c='blue', s=50, label='stay = False (移動中)', zorder=2, alpha=0.6)
    if not stay_true.empty:
        ax.scatter(stay_true['x_final'], stay_true['y_final'], 
                   c='red', s=50, label='stay = True (滞在中)', zorder=3, alpha=0.6)
    # グラフの装飾
    ax.set_title('全軌跡のマッピング結果', fontsize=18)
    ax.set_xlabel('幅[px]', fontsize=14)
    ax.set_ylabel('高さ[px]', fontsize=14)
    ax.set_xlim(0, map_width)
    ax.set_ylim(map_height, 0)
    
    # プロットされたデータがある場合のみ凡例を表示
    if not stay_true.empty or not stay_false.empty:
        ax.legend(fontsize=12)

    # レイアウトを整えて保存・表示
    fig.tight_layout()
    plt.show()