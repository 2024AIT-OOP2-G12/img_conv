import cv2
import numpy as np

def resize_with_width(image, width=1080):
    """
    画像をアスペクト比を変わらない上で1080Pに変える
    """
    original_height, original_width = image.shape[:2]

    scale = width / original_width
    new_width = width
    new_height = int(original_height * scale)

    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    return resized_image

def convert_to_crayon_style(image_path, output_path):
    # 画像を読み込む
    image = cv2.imread(image_path)
    if image is None:
        return

    # 画像を1080Pにする
    image = resize_with_width(image, width=1080)

    # ステップ1: ノイズ除去と平滑化
    denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    bilateral = cv2.bilateralFilter(denoised, 9, 75, 75)

    # ステップ2: 色の量子化処理
    Z = bilateral.reshape((-1,3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    K = 64
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    quantized = center[label.flatten()]
    quantized = quantized.reshape((bilateral.shape))
    
    # ステップ3: カラースムージングの追加
    quantized = cv2.GaussianBlur(quantized, (5, 5), 0)
    smoothed = cv2.edgePreservingFilter(quantized, flags=1, sigma_s=60, sigma_r=0.4)
    
    # ステップ4: エッジ処理の改善
    gray = cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    kernel = np.ones((2,2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    edges = cv2.GaussianBlur(edges, (3,3), 0)
    
    # ステップ5: ディテール保持フィルタリングの追加
    detail_preserved = cv2.detailEnhance(smoothed, sigma_s=10, sigma_r=0.15)
    
    # ステップ7: 最終合成
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    edges_colored_inv = cv2.bitwise_not(edges_colored)
    edges_colored_inv = cv2.GaussianBlur(edges_colored_inv, (3,3), 0)
    
    alpha_blend = 0.9
    result = cv2.addWeighted(smoothed, alpha_blend, edges_colored_inv, 1-alpha_blend, 0)

    
    # ステップ8: 最終的な色調整
    # 彩度を上げる
    hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    hsv[:,:,1] = cv2.multiply(hsv[:,:,1], 1.2)
    final_result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # 結果を保存
    cv2.imwrite(output_path, final_result)
    return final_result

if __name__ == "__main__":
    input_path = "routes/img.png"
    output_path = "static/output.png"
    convert_to_crayon_style(input_path, output_path)
