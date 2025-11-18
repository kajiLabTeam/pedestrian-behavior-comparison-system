import  numpy as np
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt

MAP_WIDTH_PX = 2837
MAP_HEIGHT_PX = 3742
GRID_SIZE_PX = 100

def create_single_heatmap(heatmap_data, background_image, output_path, colorbar_label="滞在回数"):
    """単体のヒートマップデータを可視化し、保存する関数"""
    
    # ヒートマップの描画
    fig, ax = plt.subplots(figsize=(10, 15))
    ax.imshow(background_image, extent=(0, MAP_WIDTH_PX, MAP_HEIGHT_PX, 0))
    
    # alphaで透明度を設定して重ねる
    # cmapには単体の量を表すのに適した 'Reds' や 'viridis' などを指定
    im = ax.imshow(heatmap_data, cmap='Reds', alpha=0.6, 
                   extent=(0, MAP_WIDTH_PX, MAP_HEIGHT_PX, 0))
    
    # カラーバーとラベルの設定
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(colorbar_label, fontsize=14)
    
    ax.axis('off')
    
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    print(f"単体ヒートマップを {output_path} に保存しました。")