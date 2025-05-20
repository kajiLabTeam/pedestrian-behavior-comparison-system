import math
import pandas as pd
import numpy as np

# CSVファイルを読み込み
df = pd.read_csv("data/csv/0516.csv")

# 必要な列があるか確認
if not set(['x', 'y', 'time']).issubset(df.columns):
    raise ValueError("CSVに'x', 'y', 'time'列が必要です")

# 座標差分と時間差分を計算
dx = df['x'].diff()
dy = df['y'].diff()
dt = df['time'].diff()

# 移動距離と速度を計算（速度 = 距離 / 時間）
distance = np.sqrt(dx**2 + dy**2)
speed = distance / dt

# 1行目はNaNになるので除外
speed = speed[1:].reset_index(drop=True)

# 結果をDataFrameにまとめる
result_df = pd.DataFrame({'speed': speed})

# 出力ファイル名
output_csv = "output_speed.csv"

# CSV出力
result_df.to_csv(output_csv, index=False)

# 結果を表示
print(result_df)
