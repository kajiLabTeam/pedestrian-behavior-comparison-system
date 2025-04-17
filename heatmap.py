import pandas as pd  # Pandasライブラリをpdとして読み込む
import seaborn as sns  # Seabornライブラリをsnsとして読み込む
import matplotlib.pyplot as plt  # ヒートマップ画像の画像保存のために読み込む
import japanize_matplotlib 
import json



#jsonファイルの読み込み
with open("trajectoties.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    

## estimatedデータをフラットに抽出
estimated_points = []
for traj in data['trajectories']:
    for point in traj['estimated']:
        estimated_points.append(point)


# DataFrameに変換
df = pd.DataFrame(estimated_points)


# (x, y) 座標ごとの出現回数（人数）をカウント
heat = df.groupby(['y', 'x']).size().reset_index(name='count')
print(heat)

# ピボットテーブルでヒートマップ用データ作成
pivot = heat.pivot(index='y', columns='x', values='count').fillna(0)
print(pivot)
# ヒートマップ表示
plt.figure(figsize=(12, 4))
# sns.heatmap(pivot, cmap='YlOrRd', annot=True, cbar=True)
sns.heatmap(pivot, cmap='YlOrRd', cbar=True)
plt.title("ユーザ出現ヒートマップ")
plt.xlabel("X座標")
plt.ylabel("Y座標")
plt.gca().invert_yaxis()
# plt.tight_layout()
plt.show()
