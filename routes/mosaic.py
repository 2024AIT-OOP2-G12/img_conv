import cv2
import os

class MosaicCov:
    def __init__(self, strength=10):
        '''
        MosaicCovの初期化
        - モザイクの強さを設定する
        - 画像を格納するための変数を初期化する
        '''
        self.strength = strength  # モザイクの強さ（縮小と拡大の比率）
        self.image = None         # 元画像を格納する変数

    def load_image(self):
        '''
        'static' フォルダ内のデフォルト画像 'img.png' を読み込むメソッド
        - OpenCVを使用して画像を読み込む
        - 読み込み失敗時にエラーをスローする
        '''
        # static フォルダ内の img.png を指定
        image_path = os.path.join("static", "img.png")
        self.image = cv2.imread(image_path)  # 画像を読み込む
        if self.image is None:  # 画像が読み込めなかった場合
            raise ValueError(f"画像を読み込めませんでした。'{image_path}' が存在することを確認してください。")

    def set_strength(self, strength):
        '''
        モザイク処理の強度を設定するメソッド
        - 強度は1以上の正の整数である必要がある
        Args:
            strength (int): モザイクの強度（縮小サイズの倍率）
        '''
        if strength < 1:  # 無効な強度をチェック
            raise ValueError("モザイクの強度は1以上にしてください。")
        self.strength = strength  # 強度を設定

    def mosaic(self):
        '''
        画像にモザイク処理を適用するメソッド
        - 画像を縮小し、その後に拡大することでモザイク効果を実現
        Returns:
            image_mosaic: モザイク処理された画像
        '''
        if self.image is None:  # 画像がロードされていない場合
            raise ValueError("画像がロードされていません。まずload_image()を使用してください。")

        # 画像の高さと幅を取得
        h, w = self.image.shape[:2]

        # 強度が画像サイズを超えないようにチェック
        if self.strength >= min(w, h):
            raise ValueError("モザイク強度が画像サイズを超えています。強度を小さくしてください。")

        # 縮小：画像をself.strengthの倍率で縮小
        small = cv2.resize(self.image, (w // self.strength, h // self.strength), interpolation=cv2.INTER_LINEAR)

        # 拡大：縮小された画像を元のサイズに拡大
        image_mosaic = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

        return image_mosaic  # モザイク処理後の画像を返す

    def save_image(self, mosaic_image):
        '''
        モザイク処理後の画像を 'static' フォルダ内に保存するメソッド
        Args:
            mosaic_image: モザイク処理された画像
        '''
        # static フォルダのパス
        static_folder = "static"
        if not os.path.exists(static_folder):  # static フォルダが存在しない場合は作成
            os.makedirs(static_folder)

        # 保存先のパスを設定
        output_path = os.path.join(static_folder, "output.png")
        cv2.imwrite(output_path, mosaic_image)  # 画像をファイルに書き込む
        print(f"モザイク画像が保存されました: {output_path}")

if __name__=='__main__':
    # MosaicCov クラスのインスタンス作成
    mosaic_instance = MosaicCov()

    # 入力画像の読み込み
    mosaic_instance.load_image()

    # モザイク処理の強度を設定（入力）
    n = input('強度: ')
    n = int(n)
    mosaic_instance.set_strength(n)

    # モザイク処理を実行
    mosaic_image = mosaic_instance.mosaic()

    # モザイク画像を保存
    mosaic_instance.save_image(mosaic_image)