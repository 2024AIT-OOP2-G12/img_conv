import cv2 as cv
import numpy as np
import os

def add_noise():
    # 入力画像ファイルのパス
    input_img = "static/img.png"
    output_img = "static/output.png"

    # ファイルの存在を確認
    if not os.path.exists(input_img):
        return

    # 画像を読み込み
    img = cv.imread(input_img)

    # ノイズの生成
    noise = np.random.randint(0, 255, img.shape, dtype='uint8')

    # ノイズを追加
    noisy_img = cv.add(img, noise)

    # ノイズ画像を表示
    cv.imwrite(output_img, noisy_img)

# 関数を実行
add_noise()
