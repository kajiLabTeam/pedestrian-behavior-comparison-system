import logging
import numpy as np
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt

MAP_WIDTH_PX = 2837
MAP_HEIGHT_PX = 3742
GRID_SIZE_PX = 100


def create_single_heatmap(
    heatmap_data,
    background_image,
    run_dir,
    colorbar_label="滞在回数",
    logger=None,
    vmin=None,
    vmax=None,
):
    """単体のヒートマップデータを可視化し、保存する関数"""

    if logger is None:
        logger = logging.getLogger(__name__)
    log = logger

    # ヒートマップの描画
    log.info("単体ヒートマップの描画を開始します。")
    fig, ax = plt.subplots(figsize=(10, 15))
    ax.imshow(background_image, extent=(0, MAP_WIDTH_PX, MAP_HEIGHT_PX, 0))

    # 共通スケール指定があればそれを採用し、未指定部分はデータから補完する
    data_min = np.nanmin(heatmap_data)
    data_max = np.nanmax(heatmap_data)
    actual_vmin = vmin if vmin is not None else data_min
    actual_vmax = vmax if vmax is not None else data_max
    if actual_vmax == actual_vmin:
        actual_vmax = actual_vmin + 1e-9
    color_norm = Normalize(vmin=actual_vmin, vmax=actual_vmax)

    # alphaで透明度を設定して重ねる
    # cmapには単体の量を表すのに適した 'Reds' や 'viridis' などを指定
    im = ax.imshow(
        heatmap_data,
        cmap="Reds",
        alpha=0.6,
        extent=(0, MAP_WIDTH_PX, MAP_HEIGHT_PX, 0),
        norm=color_norm,
    )

    # カラーバーとラベルの設定
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(colorbar_label, fontsize=14)

    ax.axis("off")

    plt.savefig(run_dir, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    log.info("単体ヒートマップを保存しました: %s", run_dir)
    # print(f"単体ヒートマップを {output_path} に保存しました。")
