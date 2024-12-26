import cv2
def thresholding():
    #闘値
    threshold_value = 128
    #変換する画像を変数に入れる
    input_file = "static/img.png"
    #画像をimgに読み込み
    img = cv2.imread(input_file)
    
    #グレースケールへの変換
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #2値化
    _, binary_img = cv2.threshold(img_gray, threshold_value , 255 , cv2.THRESH_BINARY)
    #画像の保存
    cv2.imwrite('static/output.png', binary_img )
    
thresholding()



