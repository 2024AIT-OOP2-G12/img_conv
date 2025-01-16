import cv2
import os
from skimage import transform
import numpy as np
import math

class SwirlCov:
    def __init__(self, strength=10):
        '''
        SwirlCovの初期化
        - 渦巻きの強さを設定する
        - 画像を格納するための変数を初期化する
        '''
        self.strength = strength  # 渦巻きの強さ
        self.image = None         # 元画像を格納する変数

    def load_image(self):
        '''
        'static' フォルダ内のデフォルト画像 'img.png' を読み込むメソッド
        - OpenCVを使用して画像を読み込む
        - 読み込み失敗時にエラーをスローする
        '''
        image_path = os.path.join("static", "img.png")
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"画像を読み込めませんでした。'{image_path}' が存在することを確認してください。")

        # OpenCV (BGR)形式をRGB形式に変換
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def set_strength(self, strength):
        '''
        渦巻き処理の強度を設定するメソッド
        Args:
            strength (int): 渦巻きの強度
        '''
        max_strength = 50  # 適切な最大強度を設定
        if strength < 1 or strength > max_strength:
            raise ValueError(f"強度は1以上{max_strength}以下にしてください。")
        self.strength = strength

    def swirl(self):
        '''
        画像に渦巻き処理を適用するメソッド
        - skimage.transform.swirl を使用して渦巻き効果を適用
        Returns:
            image_swirl: 渦巻き処理された画像
        '''
        if self.image is None:
            raise ValueError("画像がロードされていません。まずload_image()を使用してください。")

        # 画像の高さと幅を取得
        height, width, _ = self.image.shape

        # 対角線長さを計算
        diagonal = math.sqrt(height**2 + width**2)

        # 渦巻き効果を適用（radiusを対角線長さ以上に設定）
        image_swirl = transform.swirl(
            self.image,
            strength=self.strength,
            radius=diagonal,  # 画像全体に適用
            rotation=0,       # 回転量（任意で調整可能）
            mode='reflect'
        )

        # データ形式を0-255の範囲に戻して8bit整数に変換
        image_swirl = (image_swirl * 255).astype(np.uint8)

        return image_swirl

    def save_image(self, swirl_image):
        '''
        渦巻き処理後の画像を 'static' フォルダ内に保存するメソッド
        Args:
            swirl_image: 渦巻き処理された画像
        '''
        static_folder = "static"
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)

        # RGB形式をBGR形式に戻して保存
        swirl_image_bgr = cv2.cvtColor(swirl_image, cv2.COLOR_RGB2BGR)
        output_path = os.path.join(static_folder, "output.png")
        cv2.imwrite(output_path, swirl_image_bgr)
        print(f"渦巻き画像が保存されました: {output_path}")

if __name__ == '__main__':
    # SwirlCov クラスのインスタンス作成
    swirl_instance = SwirlCov()

    # 入力画像の読み込み
    swirl_instance.load_image()

    # 渦巻き処理の強度を設定（入力）
    n = input('強度を入力してください（1〜50）: ')
    n = int(n)
    swirl_instance.set_strength(n)

    # 渦巻き処理を実行
    swirl_image = swirl_instance.swirl()

    # 渦巻き画像を保存
    swirl_instance.save_image(swirl_image)