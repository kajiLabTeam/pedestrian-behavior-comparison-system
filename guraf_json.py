import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import json

matplotlib.rcParams['font.family'] = 'Hiragino Maru Gothic Pro'


# 四角の大きさ
width = 10
height = 6



with open("raw_0515.json", "r", encoding="utf-8") as f:
	data = json.load(f)

## estimatedデータをフラットに抽出
estimated_points = []
for traj in data['trajectories']:
    for point in traj['estimated']:
        estimated_points.append({
        'walked_at': point.get("walked_at", 0),  # time がなければ0を仮定
            'x': point["x"],
        
        	'y': point["y"]
        })
        

# pandasでデータフレーム化し、time順に並び替え
df = pd.DataFrame(estimated_points)


# 正規化
colors = np.linspace(0, 1, len(df))

# プロット
plt.figure(figsize=(6, 6))
plt.scatter(df["x"], df["y"], c=colors, cmap='coolwarm', s=100)
plt.plot(df["x"], df["y"], color="gray", alpha=0.3)  # 線でつなぐ
plt.title("歩行軌跡（青→赤）")
plt.xlabel("X座標")
plt.ylabel("Y座標")
plt.axis('equal')
plt.gca().invert_yaxis()
plt.colorbar(label='進行度')
plt.show()
