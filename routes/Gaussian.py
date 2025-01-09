import cv2 as cv
import os

def gaussian():

    # 画像ファイルのパス
    input_img = "static/img.png" 
    output_img = "static/output.png"

    # ファイルの存在を確認
    if not os.path.exists(input_img):
        return

    # 画像を読み込み
    img = cv.imread(input_img)

    # グレースケール変換
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # ガウシアンフィルタ
    dst = cv.GaussianBlur(gray, ksize=(15, 15), sigmaX=5.0)

    #グレースケールの画像を表示
    cv.imwrite(output_img, dst)

gaussian()
