import cv2 as cv
import os

def inversion():

    # 画像ファイルのパス
    input_img = "static/img.png"
    output_img = "static/output.png"

    # ファイルの存在を確認
    if not os.path.exists(input_img):
        return

    # 画像を読み込み
    img = cv.imread(input_img)

    # 画像を反転
    flipped_img = cv.flip(img, 1)

    # 反転画像を表示
    cv.imwrite(output_img, flipped_img)
    
inversion()
