# 歩行者行動比較システム (Pedestrian Behavior Comparison System)

## システムの説明

### 概要
施策前後のフロア内の歩行者の**滞在箇所**を可視化し、施策前後で比較するシステムである。歩行軌跡から滞在箇所を抽出する．滞在箇所をヒートマップで可視化する(滞在ヒートマップ)．通常・施策の滞在ヒートマップから差分をとり，施策による滞在箇所の変化を一目で把握する．

**滞在** = 歩行者が立ち止まっている箇所（歩行速度が0以下の状態）

### システムの目的
- 施策や環境変化による歩行者の行動変化を定量的に測定
- 施設内で歩行者が立ち止まる箇所（滞在地点）の可視化
- 施策前後の滞在パターンの比較分析

### 使用するデータ
- **歩行軌跡** : 時刻 [s] , x[m] , y[m]

歩行軌跡作成Webアプリで条件A/Bの軌跡を複数作成する．
- A(通常)
- B（施策）


### システム詳細
## 歩行情報蓄積
実装していない


## 滞在箇所の抽出

### 滞在ヒートマップ

### 差分ヒートマップ
#### 静止の判定方法
歩行速度から歩行状態と静止状態を判定します。

| 速さ (m/s)    | 判定 | 
| ------------ | ---- | 
| 0以下        | 静止 | 
| 0 より大きい | 歩行| 

#### 色のマッピング
滞在時間が長いほど赤くなります。

| 静止時間 | 色       | 
| -------- | -------- | 
| 長い     | 赤 🟥   | 
| 短い     | 黄色 🟨 | 
| なし     | グレー   |

### フロアマップ
<img width="500" alt="14号館5階フロアマップ.png (163.6 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2025/05/20/168726/0e02157b-9b27-4690-bd6d-c39a9067e2d0.png">

## システムのアーキテクチャ

### 処理流れ
```
センサーデータ (CSV)
     ↓
[1] データの読み込みと前処理
     ↓
[2] 軌跡データの座標変換
     ↓
[3] 移動速度の計算
     
[4] 静止状態の判定
     ↓
[5] 滞在回数の集計
     ↓
[6] グリッドベースのヒートマップデータ生成
     ↓
[7] ヒートマップの可視化と出力
```

### 主要なモジュール

| ファイル | 説明 |
|---------|------|
| `main.py` | メインプログラム。オプション処理と処理フロー管理 |
| `load_trajectory_data.py` | センサーデータの読み込みと前処理 |
| `transform_trajectory.py` | センサー座標から実空間座標への変換 |
| `generate_heatmap_data.py` | グリッド単位での滞在情報集計 |
| `visualize_and_save_heatmap.py` | ヒートマップの画像化と保存 |
| `setup_grid_and_background.py` | グリッドの初期化と背景画像の設定 |
| `calculate_stay_time.py` | 滞在時間の計算 |
| `calculate_stay_count.py` | 滞在回数の計算 |
| `process_speed_data.py` | 歩行速度の計算と統計 |
| `config/trajectory_lists.py` | 実験条件と測定データのマッピング設定 |

### 入力データの構造

```
input/
├── raw/            				# 生データ
│   ├── A/						# 通常条件 (Condition A)
│   │   ├── 20251127_ishii_01.csv
│   │   ├── 20251128_ishii_02.csv
│   │   └── ...
│   │
│   └── B/						# 施策条件 (Condition B)
│       ├── 20251127_ishii_01.csv
│       ├── 20251128_ishii_02.csv
│       └── ...
│   
│        						
└── processed/      				# 前処理済みデータ（滞在判定付き軌跡）
    ├── A/
    │   ├── 20251127_ishii_01_processed.csv
    │   ├── 20251128_ishii_02_processed.csv
    │   └── ...
    │
    ├── B/
        ├── 20251127_ishii_01_processed.csv
        ├── 20251128_ishii_02_processed.csv
        └── ...
    

```

#### raw/ディレクトリの構造
各条件ディレクトリ（A, B等）配下には以下ファイルが含まれます：
- `YYYYMMDD_name.csv` - 軌跡データ（時刻、x座標、y座標）

#### processed/ディレクトリの構造
rawと同じ条件別ディレクトリ構成で、前処理済みのデータを格納：
- `YYYYMMDD_name_processed.csv` - 前処理済み軌跡データ（速度、滞在情報等を付与）

### 出力データ
#### ① ヒートマップを出力
```
src/output/
├── 20260129_111302_heatmap_all/
│   ├── 20260129_111302.log                # 実行ログ
│   ├── heatmap_A.png                      # 条件Aのヒートマップ
│   ├── heatmap_B.png                      # 条件Bのヒートマップ
│   ├── differential_heatmap.png           # 差分ヒートマップ
│   ├── trajectory_combined_A.png          # 条件Aの軌跡図
│   └── trajectory_combined_B.png          # 条件Bの軌跡図
│
├── 20260129_113253_heatmap_all/
│   ├── 20260129_113253.log
│   ├── heatmap_A.png
│   ├── heatmap_B.png
│   ├── differential_heatmap.png
│   ├── trajectory_combined_A.png
│   └── trajectory_combined_B.png
│
└── ...
```

#### ファイルの説明
| ファイル | 説明 |
|---------|------|
| `.log` | 実行ログ（処理内容とタイムスタンプ） |
| `heatmap_A.png` | 条件A（通常）における滞在ヒートマップ |
| `heatmap_B.png` | 条件B（施策）における滞在ヒートマップ |
| `differential_heatmap.png` | 条件AとBの差分ヒートマップ（比較用） |
| `trajectory_combined_A.png` | 条件Aの歩行軌跡 |
| `trajectory_combined_B.png` | 条件Bの歩行軌跡 |


## 実行方法

### 環境構築

このプログラムは `python3.11.5` を使用しています。pythonの仮想環境（venv）を使用してください。

```bash
# 仮想環境を作成する
python -m venv .venv

# 仮想環境を有効化する
source .venv/bin/activate

# ライブラリをインストールする
pip install -r requirements.txt

# 仮想環境から抜ける（終了時）
deactivate
```

### 使用できるコマンド

#### 1. 実行ファイルのディレクトリに移動
```bash
cd pedestrian-behavior-comparison-system/src
```

#### 2. 滞在情報付きCSVの生成
特定の軌跡データから速度および滞在情報を付与したCSVファイルを作成します。

```bash
# A（滞在なし）の軌跡から滞在情報付きCSVを作成
python main.py -c "input/raw/A/input.csv" -a

# 別の軌跡データから生成
python main.py -c "<軌跡CSVファイルのパス>" -a
```

#### 3. ヒートマップの生成
**全ての**滞在情報付きCSVファイルから差分ヒートマップを作成します。
(input/processed/A(:B)/20251128_ishii_01_processed.csv)

```bash
# 差分ヒートマップを生成
python main.py -f
```

### コマンドラインオプション

| オプション | 説明 |
|----------|------|
| `-c <path>` | 指定されたCSVファイルから滞在情報付きCSVを生成 |
| `-a` | すべてのCSVファイルから滞在情報付きCSVを生成 |
| `-f` | 全ての滞在情報付きCSVから差分ヒートマップを生成 |
| `-h` | ヘルプを表示 |

## 実験条件の説明

### speed実験（歩行速度による比較）
歩行速度を変えた場合の歩行者行動の違いを観測

- **fastWalk/**: 高速歩行時の行動
- **normal/**: 通常速度での歩行
- **slowly/**: ゆっくりとした歩行
- **run/**: 走行時の行動

各ディレクトリには、加速度計とジャイロスコープのセンサーデータが含まれています。

### part実験（部分的な場所での測定）
特定の場所や状況での歩行者行動を測定
- **1_straight_sit_quick/**: 直進後に素早く座る動作
- **2_straight_quick_sit/**: 素早く直進してから座る動作
- **3_straight_sit/**: 直進してから通常速度で座る動作
- **4_gray_sit/**: グレーの環境での座る動作
- **A**, **B/**: 異なるシナリオの測定

### practice実験（予備測定）
- **0523/**, **0526/**, **0527/**: 日付ごとの測定

### 軌跡データ（csv/）
- **0516.csv**, **0519.csv**: 収集された軌跡データ
- **json/**: JSON形式の軌跡データ
  - `trajectories.json` - 全軌跡データ
  - `stop_trajectories.json` - 停止地点の軌跡


## 参考資料
システム実装については，esaに詳しくまとめています．．
(URL:https://kjlb.esa.io/posts/7828)