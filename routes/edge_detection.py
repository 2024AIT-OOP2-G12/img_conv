import cv2

def edge_detection(input_file="static/img.png", output_file="static/edges.png", lower_threshold=100, upper_threshold=200):
    
    # 画像を読み込む
    img = cv2.imread(input_file)
    
    # 入力画像が存在しない場合のエラー処理
    if img is None:
        print(f"エラー: 入力ファイル '{input_file}' が存在しないか、読み込むことができませんでした。")
        return

    # グレースケールに変換
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # エッジ検出 (Canny)
    edges = cv2.Canny(img_gray, lower_threshold, upper_threshold)
    
    # 検出されたエッジ画像を保存
    cv2.imwrite(output_file, edges)
    print(f"エッジ検出結果が '{output_file}' に保存されました。")

# スクリプトが直接実行された場合のみ以下を実行
if __name__ == "__main__":
    input_file = "img.png"  # 入力画像ファイル名
    output_file = "edges.png"  # 出力画像ファイル名
    edge_detection(input_file, output_file)
