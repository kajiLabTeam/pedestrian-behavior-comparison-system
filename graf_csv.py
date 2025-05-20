import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np


matplotlib.rcParams['font.family'] = 'Hiragino Maru Gothic Pro'

# 四角の大きさ
width = 10
height = 6

# df = pd.read_csv("walk_trace.csv")
df = pd.read_csv("0516.csv")

# 正規化
colors = np.linspace(0, 1, len(df))

# プロット
plt.figure(figsize=(6, 6))
plt.scatter(df["x"], df["y"], c=colors, cmap='coolwarm', s=100)
plt.plot(df["x"], df["y"], color="gray", alpha=0.3)  # 線でつなぐ
plt.title("歩行軌跡（青→赤）")
plt.xlabel("X座標[cm]")
plt.ylabel("Y座標[cm]")
plt.axis('equal')
plt.colorbar(label='進行度')
plt.show()