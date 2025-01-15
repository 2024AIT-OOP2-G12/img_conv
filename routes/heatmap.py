import cv2 as cv
import os

def heatmap():
    # 入力画像ファイルのパス
    input_img = "static/img.png"
    output_img = "static/output.png"

    # ファイルの存在を確認
    if not os.path.exists(input_img):
        return

    # 画像を読み込み
    img = cv.imread(input_img)

    # グレースケール変換
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # ヒートマップ変換
    heatmap_img = cv.applyColorMap(gray, cv.COLORMAP_JET)

    # ヒートマップ画像を表示
    cv.imwrite(output_img, heatmap_img)

# 関数を実行
heatmap()
