import math
from PIL import Image, ImageDraw , ImageFont


def setup_grid_and_background(map_width_px, map_height_px, grid_size_px):
    # フロアマップの寸法（ピクセル単位）
    map_width = map_width_px
    map_height = map_height_px

    # 提案されたグリッドサイズ（ピクセル単位）
    grid_size = grid_size_px 

    num_grids_x = math.ceil(map_width / grid_size)
    num_grids_y = math.ceil(map_height / grid_size)

    # 2. フロアマップの読み込みと表示          
    img = Image.open("../docs/floorMap/building＝14,floor=5_freeSpace.png")

    draw = ImageDraw.Draw(img)

    # グリッド線を描画
    for x in range(0, map_width_px, grid_size_px):
        draw.line([(x, 0), (x, map_height_px)], fill='red', width=1)
    for y in range(0, map_height_px, grid_size_px):
        draw.line([(0, y), (map_width_px, y)], fill='red', width=1)
    

    # 4. 各グリッドにIDを割り振って描画
    grid_data = []

    try:
        font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
        font = ImageFont.truetype(font_path, size=30)
    except IOError:
        font = ImageFont.load_default()
      
    for y in range(num_grids_y):
        for x in range(num_grids_x):
            # グリッドの中心座標を計算
            center_x = x * grid_size + grid_size / 2
            center_y = y * grid_size + grid_size / 2
            grid_id_tuple = (x, y)
            draw.text((center_x, center_y), f"({x},{y})", fill ='black',anchor='mm', fontsize=100, font=font)

            # グリッドの情報を辞書として保存
            grid_info = {
                'id': grid_id_tuple,
                'x_min': x * grid_size,
                'y_min': y * grid_size,
                'x_max': (x + 1) * grid_size,
                'y_max': (y + 1) * grid_size
            }
            grid_data.append(grid_info)

    # img.show()
            
    return img, grid_data, num_grids_x, num_grids_y
