from flask import render_template, request, redirect, url_for, send_file, session, Blueprint
import os
from routes.negaposi import negaposi
from routes.mosaic import MosaicCov
from routes.Gaussian import gaussian
from routes.Thresholding import thresholding
from routes.edge_detection import edge_detection
from routes.img_quality import enhance_image_advanced
from routes.Inversion import inversion
from models import History, User
import base64
import datetime
from routes.convert2crayon_style import convert_to_crayon_style
from routes.stamp import stamp
from routes.add_noise import add_noise
from routes.heatmap import heatmap


# Blueprintの作成
change_bp = Blueprint('change', __name__, url_prefix='/change')

#ボタンを押して画像をstatic内に保存されるようにする-----------------------------------------------------------------------------------------------
@change_bp.route('/upload', methods=['POST'])
def upload():
    # ファイルがアップロードされたか確認(本当はアラートを出したいがjsを使わなければならないので、時間が余ったら実装する)
    if 'file' not in request.files:
        return 'ファイルが選択されていません。', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'ファイルが選択されていません。', 400
    
    if file:
        filepath = os.path.join('static', 'img.png')
        file.save(filepath)
        return redirect(url_for('change.change', user_name = session['user_name']))


#change.htmlのエンドポイント------------------------------------------------------------------------------------------------------
@change_bp.route('/<user_name>')
def change(user_name):
    # ページ番号を取得
    page = request.args.get('page', 1, type=int)
    # 1ページあたりの履歴数
    per_page = 10
    # 現在のユーザーの履歴を取得
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    total_histories = History.select().where(History.user == user).count()
    histories = History.select().where(History.user == user).order_by(History.times.desc()).paginate(page, per_page)
    return render_template('change.html', histories=histories, user_name=user_name, page=page, total_pages=(total_histories // per_page) + 1)

#画像変換ようのエンドポイント------------------------------------------------------------------------------------------------------
@change_bp.route('/conv',  methods=['POST'])
def conv():
     #変換用モジュールのインスタンス化
    nega = negaposi()
    mosic = MosaicCov()
    stamp_instance = stamp()
    input_file_name = "static/img.png"
    output_file_name = "static/output.png"
    # `select` タグで選択された値を取得
    selected_value = request.form.get('selected_option')
    if selected_value=="":
        return '変換方法を選択してください', 400
    elif selected_value == "1":
        nega.negaposi_ms()
        conv_message = "画像の画像内の濃淡を入れ替える変換です。画像内の明るい画素を暗い画素に、暗い画素を明るい画素に変換する処理です。"
    elif selected_value == "2":
        # モザイク処理の強度取得
        mosaic_strength = request.form.get('mosaic_strength', type=int)
        if mosaic_strength is None or mosaic_strength < 1:
            return "モザイクの強度は1以上にしてください。", 400
        mosic.load_image()
        mosic.set_strength(mosaic_strength)
        mosic_img = mosic.mosaic()
        mosic.save_image(mosic_img)
        conv_message = "アップロードした画像にモザイク処理を施す"
    elif selected_value == "3":
        gaussian()
        conv_message = "アップロードした画像にガウシアンフィルタを施す"
    elif selected_value == "4":
        thresholding(input_file_name, output_file_name)
        conv_message = "アップロードした画像に二値化処理を施す"
    elif selected_value == "5":
        edge_detection(input_file_name, output_file_name)
        conv_message = "アップロードした画像にエッジ処理を施す"
    elif selected_value == "6":
        enhance_image_advanced(input_file_name)
        conv_message = "アップロードされた画像に色彩処理を施す"
    elif selected_value == "7":
        inversion()
        conv_message = "アップロードした画像に左右反転を施す"
    elif selected_value == "8":
        stamp_instance.load_images()
        stamp_choice = request.form.get('stamp_choice', type=str)
        x = request.form.get('stamp_x', type=int)
        y = request.form.get('stamp_y', type=int)
        stamp_instance.set_stamp_type(stamp_choice)
        stamp_instance.resize_stamp()
        stamp_instance.paste_stamp(x, y)
        stamp_instance.save_image()
        conv_message = "アップロードした画像にスタンプを施す"
    elif selected_value == "9":
        convert_to_crayon_style(input_file_name, output_file_name)
        conv_message = "アップロードした画像をクレヨン風な画像に変換する"
    elif selected_value == "10":
        add_noise()
        conv_message = "アップロードした画像にノイズを加える"
    elif selected_value == "11":
        heatmap()
        conv_message = "アップロードした画像をサーモグラフィ風の画像に変換する"

    #change.html内で変換された画像とメッセージが表示されるようにする
    output_path = os.path.join('static', 'output.png')
    file_exists = os.path.exists(output_path)

    #bace64を用いて画像データをエンコードする
    with open(output_path, "rb") as output_file:
        encord_img_data = base64.b64encode(output_file.read())

    # 現在のログインユーザーを取得
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    print(f"user={user}")

    #Historyデータベースにエンコードした画像データと変換日時を代入する
    History.create(
        user = user,
        times = datetime.datetime.now(),
        image_data = encord_img_data
    )

    #Historyデータの抽出
    histories = History.select().where(History.user == user).order_by(History.times.desc()).paginate(1, 10)
    print(f"his={histories}")
    return render_template('change.html', 
                           file_exists=file_exists, 
                           message=conv_message, 
                           histories = histories, 
                           user_name = session['user_name'],
                           page=1,
                           total_pages=(History.select().where(History.user == user).count() // 10) + 1)

#スタンプ画像用のエンドポイント------------------------------------------------------------------------------------------------------
@change_bp.route('/upload_stamp', methods=['POST'])
def upload_stamp():
    if 'file' not in request.files:
        return 'スタンプ画像が選択されていません。', 400

    file = request.files['file']
    if file.filename == '':
        return 'スタンプ画像が選択されていません。', 400

    if file:
        filepath = os.path.join('static', f'{file.filename}')
        file.save(filepath)

    return redirect(url_for('index'))

#変換画像ダウンロード用のエンドポイント------------------------------------------------------------------------------------------------------
@change_bp.route('/download', methods=['POST'])
def download():
    output_path = os.path.join('static', 'output.png')
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True, download_name='output.png')
    else:
        return "変換された画像が見つかりません。", 404


