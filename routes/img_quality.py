import cv2
import numpy as np

def enhance_image_advanced(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return

    # ステップ1: 明るさとコントラストの調整
    alpha = 1.2
    beta = 30
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # ステップ2: ガンマ補正
    gamma = 1.5
    look_up_table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255 for i in range(256)]).astype("uint8")
    gamma_corrected = cv2.LUT(adjusted, look_up_table)

    # ステップ3: ヒストグラム均等化
    ycrcb = cv2.cvtColor(gamma_corrected, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)
    y_eq = cv2.equalizeHist(y)
    ycrcb_eq = cv2.merge([y_eq, cr, cb])
    hist_eq = cv2.cvtColor(ycrcb_eq, cv2.COLOR_YCrCb2BGR)

    # ステップ4: 色彩バランスの調整
    balance_ratio = [1.2, 1.1, 1.0]
    balanced = hist_eq.copy()
    for i in range(3):
        balanced[:, :, i] = cv2.multiply(balanced[:, :, i], balance_ratio[i])
    balanced = np.clip(balanced, 0, 255).astype("uint8")

    # ステップ5: 軽度のノイズ除去
    denoised = cv2.fastNlMeansDenoisingColored(balanced, None, 15, 15, 7, 21)

    # ステップ6: シャープ化
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)

    # ステップ7: アンシャープマスキング
    gaussian_blur = cv2.GaussianBlur(sharpened, (9, 9), 10.0)
    unsharp_mask = cv2.addWeighted(sharpened, 1.5, gaussian_blur, -0.5, 0)

    # 処理結果を保存
    cv2.imwrite("static/output.png", unsharp_mask)

if __name__ == "__main__":
    input_image = "routes/img.png"
    enhance_image_advanced(input_image)