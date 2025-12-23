"""軌跡ファイルと変換パラメータの設定モジュール。

このモジュールには主にヒートマップ生成等で使用する軌跡ファイルのパス一覧と、
軌跡を地図上に合わせるためのデフォルト変換パラメータを定義する。

変数一覧
- TRAJECTORY_FILE_PATHS_A: グループ A の軌跡ファイル（リポジトリルートからの相対パスを想定）
- TRAJECTORY_FILE_PATHS_B: グループ B の軌跡ファイル（リポジトリルートからの相対パスを想定）
- DEFAULT_TRANSFORM_PARAM: 軌跡を地図座標に合わせるためのデフォルト変換パラメータ（辞書）
    - scale: スケール倍率（float）
    - angle_deg: 回転角（度、float）
    - initial_position: (x, y) のタプル（地図上の初期原点）

利用方法
- 他のモジュール（例: `src/main.py`）から import して利用する。

"""

TRAJECTORY_FILE_PATHS_A = [
    # "input/processed/A/20251127_ryuki_01.csv",
    # "input/processed/A/20251127_ryuki_02.csv",
    # "input/processed/A/20251204_ryuki_03.csv",
    # "input/processed/A/20251204_ryuki_04.csv",
    # "input/processed/A/20251204_ryuki_05.csv",
    # "input/processed/A/20251204_ryuki_06.csv",
    # "input/processed/A/20251204_ryuki_07.csv",
    # "input/processed/A/20251204_ryuki_08.csv",
    # "input/processed/A/20251204_ryuki_09.csv",
    # "input/processed/A/20251204_ryuki_10.csv",
    # "input/processed/A/20251211_ryuki_11.csv",
    # "input/processed/A/20251211_ryuki_12.csv",
    # "input/processed/A/20251211_ryuki_13.csv",
    # "input/processed/A/20251211_ryuki_14.csv",
    # "input/processed/A/20251211_ryuki_15.csv",
    "input/processed/A/20251203_ishii_01.csv",
    "input/processed/A/20251203_ishii_02.csv",
    "input/processed/A/20251203_ishii_03.csv",
    "input/processed/A/20251203_ishii_04.csv",
    "input/processed/A/20251203_ishii_05.csv",
    "input/processed/A/20251203_ishii_06.csv",
    "input/processed/A/20251203_ishii_07.csv",
    "input/processed/A/20251203_ishii_08.csv",
    "input/processed/A/20251203_ishii_09.csv",
    "input/processed/A/20251203_ishii_10.csv",
]

TRAJECTORY_FILE_PATHS_B = [
    # "input/processed/B/20251127_ryuki_01.csv",
    # "input/processed/B/20251127_ryuki_02.csv",
    # "input/processed/B/20251204_ryuki_03.csv",
    # "input/processed/B/20251204_ryuki_04.csv",
    # "input/processed/B/20251204_ryuki_05.csv",
    # "input/processed/B/20251211_ryuki_06.csv",
    # "input/processed/B/20251211_ryuki_07.csv",
    # "input/processed/B/20251211_ryuki_08.csv",
    # "input/processed/B/20251211_ryuki_09.csv",
    # "input/processed/B/20251211_ryuki_10.csv",
    "input/processed/B/20251203_ishii_01.csv",
    "input/processed/B/20251203_ishii_02.csv",
    "input/processed/B/20251203_ishii_03.csv",
    # "input/processed/B/20251203_ishii_04.csv",
    # "input/processed/B/20251203_ishii_05.csv",
    # "input/processed/B/20251203_ishii_06.csv",
    # "input/processed/B/20251203_ishii_07.csv",
    # "input/processed/B/20251203_ishii_08.csv",
    # "input/processed/B/20251203_ishii_09.csv",
    # "input/processed/B/20251203_ishii_10.csv",
]

DEFAULT_TRANSFORM_PARAM = {
    "scale": 1.0,
    "angle_deg": 0.0,
    "initial_position": (6, 28),
}
