import cv2
import os

class negaposi():

    def __init__(self) -> None:

        self.img_name = os.path.join('static', 'img.png')
        print(self.img_name)

    def negaposi_ms(self):
        input_img : cv2.Mat = cv2.imread(self.img_name)
        if input_img is None:
            raise FileNotFoundError(f"画像ファイル '{self.img_name}' が見つかりません。パスを確認してください。")
        change_img : cv2.Mat = 255 - input_img
        output_path = os.path.join('static', 'output.png')
        cv2.imwrite(output_path, change_img)
        return change_img

if __name__ == '__main__':
    negaposi_x = negaposi()
    cv2.imshow('shougun', negaposi_x.negaposi_ms())
    cv2.waitKey(0)

       