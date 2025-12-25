import logging
import numpy as np
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt

MAP_WIDTH_PX = 2837
MAP_HEIGHT_PX = 3742
GRID_SIZE_PX = 100


def create_diff_heatmap(
    heatmap_data_A,
    heatmap_data_B,
    background_image,
    run_dir,
    colorbar_label="差分",
    logger=None,
):

    if logger is None:
        logger = logging.getLogger(__name__)
    log = logger

    # 差分データを計算
    diff_data = heatmap_data_B - heatmap_data_A

    # 色の範囲を0を中心に左右対称にする
    with np.errstate(all="ignore"):
        vmax = np.nanmax(np.abs(diff_data))
    if not np.isfinite(vmax) or vmax == 0:
        vmax = 1
    norm = Normalize(vmin=-vmax, vmax=vmax)

    # ヒートマップの描画
    log.info("差分ヒートマップの描画を開始します。")
    fig, ax = plt.subplots(figsize=(10, 15))
    ax.imshow(background_image, extent=(0, MAP_WIDTH_PX, MAP_HEIGHT_PX, 0))

    # alphaで透明度を設定して重ねる
    im = ax.imshow(
        diff_data,
        cmap="RdBu_r",
        norm=norm,
        alpha=0.6,
        extent=(0, MAP_WIDTH_PX, MAP_HEIGHT_PX, 0),
    )

    # カラーバーとラベルの設定
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(colorbar_label, fontsize=14)

    ax.axis("off")
    plt.savefig(run_dir, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    log.info("差分ヒートマップを保存しました: %s", run_dir)
    # print(f"差分ヒートマップを {output_path} に保存しました。")
