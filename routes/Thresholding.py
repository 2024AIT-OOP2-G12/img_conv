import cv2

def thresholding(input_file="static/img.png", output_file="static/output.png", threshold_value=128):
    
    # 画像を読み込み
    img = cv2.imread(input_file)

    # 入力画像が存在しない場合のエラー処理
    if img is None:
        print(f"エラー: 入力ファイル '{input_file}' が存在しないか、読み込むことができませんでした。")
        return
    
    # グレースケールへの変換
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 二値化
    _, binary_img = cv2.threshold(img_gray, threshold_value, 255, cv2.THRESH_BINARY)
    
    # 画像の保存
    cv2.imwrite(output_file, binary_img)
    print(f"二値化画像が '{output_file}' に保存されました。")

# スクリプトが直接実行された場合のみ以下を実行
if __name__ == "__main__":
    input_file = "static/img.png"  # 入力画像のパス
    output_file = "static/output.png"  # 出力画像の保存先
    thresholding(input_file, output_file)
