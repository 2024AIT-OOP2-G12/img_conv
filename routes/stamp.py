from PIL import Image
import os

class stamp:
    def __init__(self, strength=100):
        self.strength = strength
        self.base_image = None
        self.stamp_image = None

    def load_images(self):
        folder_path = "static"
        base_image_path = os.path.join(folder_path, "img.png")
        stamp1_image_path = os.path.join(folder_path, "stamp1.png")
        stamp2_image_path = os.path.join(folder_path, "stamp2.png")
        stamp3_image_path = os.path.join(folder_path, "stamp3.png")

        self.base_image = Image.open(base_image_path)
        self.stamp_images = {
            "stamp1": Image.open(stamp1_image_path),
            "stamp2": Image.open(stamp2_image_path),
            "stamp3": Image.open(stamp3_image_path)
        }

    def set_stamp_type(self, stamp_type):
        if stamp_type not in self.stamp_images:
            raise ValueError("指定されたスタンプが見つかりません。")
        self.stamp_image = self.stamp_images[stamp_type]

    def set_strength(self, strength):
        if strength < 1:
            raise ValueError("サイズは1以上にしてください。")
        self.strength = strength

    def resize_stamp(self):
        self.stamp_image = self.stamp_image.resize((self.strength, self.strength), Image.LANCZOS)

    def paste_stamp(self, x, y):
        if self.base_image is None or self.stamp_image is None:
            raise ValueError("画像が読み込まれていません。load_images()を呼び出してください。")
        position = (x, y)
        self.base_image.paste(self.stamp_image, position, self.stamp_image)

    def save_image(self):
        folder_path = "static"
        output_path = os.path.join(folder_path, "output.png")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        self.base_image.save(output_path)

if __name__ == "__main__":
    stamping = stamp()
    stamping.load_images()

    strength = int(input("スタンプ画像のサイズを入力してください（幅と高さ、1以上の整数）: "))
    stamping.set_strength(strength)

    x = int(input("スタンプを貼り付けるX座標を入力してください: "))
    y = int(input("スタンプを貼り付けるY座標を入力してください: "))

    stamping.paste_stamp(x, y)
    stamping.save_image()