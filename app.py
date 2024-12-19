from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods = ['POST'])
def upload():
    # ファイルがアップロードされたか確認
    if 'file' not in request.files:
        return 'ファイルが選択されていません。', 400
    #ファイル名があるかどうかの確認(ファイル選択されるinputタグの名前はfileなので'file')
    file = request.files['file']
    if file.filename == '':
        return 'ファイルが選択されていません。', 400
    #ファイルが存在する場合、staticにimg.pngとして保存する
    if file:
        filepath = os.path.join('static', 'img.png')
        file.save(filepath)
        return redirect(url_for('conversion'))
    
@app.route('/conversion')
def conversion():
    render_template('conversion.html')

if __name__ =='__main__':
    app.run(port=8080, debug=True)