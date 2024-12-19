import cv2 as cv

def gaussian():

    # 画像ファイルのパス
    input_img = "static/img.jpg" 
    output_img = "static/output.png"

    # 画像を読み込み
    img = cv.imread(input_img)

    # グレースケール変換
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # ガウシアンフィルタ
    dst = cv.GaussianBlur(gray, ksize=(15, 15), sigmaX=5.0)

    #グレースケールの画像を表示
    cv.imwrite(output_img, dst)

gaussian()