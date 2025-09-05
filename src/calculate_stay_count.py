def calculate_stay_count(df_transformed, GRID_SIZE_PX):
    """
    軌跡データから各グリッドへの滞在回数を計算する。
    同じグリッドに留まり続けている場合は1回とカウントし、
    別のグリッドに移動したタイミングでカウントを増やす。

    Args:
        df_transformed (pd.DataFrame): 変換後の軌跡データ。'transformed_x', 'transformed_y' カラムを持つ。
        GRID_SIZE_PX (int): グリッドの1辺のピクセルサイズ。

    Returns:
        dict: 各グリッドIDをキー、滞在回数を値とする辞書。例: {(col, row): count}
    """

    df_transformed = df_transformed[df_transformed['stay'] == True].copy()

    if df_transformed.empty:
        return {}

    # 各点のグリッドIDを計算
    df_transformed['grid_col'] = (df_transformed['x_final'] // GRID_SIZE_PX).astype(int)
    df_transformed['grid_row'] = (df_transformed['y_final'] // GRID_SIZE_PX).astype(int)

    # 前の点とグリッドIDが異なる点のみを抽出（グリッドの移動を検出）
    grid_visits = df_transformed[
        (df_transformed['grid_col'] != df_transformed['grid_col'].shift(1)) |
        (df_transformed['grid_row'] != df_transformed['grid_row'].shift(1))
    ]

    # グリッドごとの訪問回数をカウント
    stay_counts = grid_visits.groupby(['grid_col', 'grid_row']).size().to_dict()

    return stay_counts