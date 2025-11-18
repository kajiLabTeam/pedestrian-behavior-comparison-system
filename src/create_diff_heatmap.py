import	numpy as np
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt

MAP_WIDTH_PX = 2837
MAP_HEIGHT_PX = 3742
GRID_SIZE_PX = 100

def create_diff_heatmap(heatmap_data_A, heatmap_data_B, background_image, output_path, colorbar_label="差分"):
    
    

    # 差分データを計算
    diff_data = heatmap_data_A - heatmap_data_B
    
    # 色の範囲を0を中心に左右対称にする
    vmax = np.abs(diff_data).max()
    norm = Normalize(vmin=-vmax, vmax=vmax)
    
    # ヒートマップの描画
    fig, ax = plt.subplots(figsize=(10, 15))
    ax.imshow(background_image, extent=(0, MAP_WIDTH_PX, MAP_HEIGHT_PX, 0))
    
    # alphaで透明度を設定して重ねる
    im = ax.imshow(diff_data, cmap='RdBu_r', norm=norm, alpha=0.6, 
                   extent=(0, MAP_WIDTH_PX, MAP_HEIGHT_PX, 0))
    
    # カラーバーとラベルの設定
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(colorbar_label, fontsize=14)
    
    ax.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    print(f"差分ヒートマップを {output_path} に保存しました。")
    