from models import initialize_database, History, User
from flask import Flask, render_template
from models import initialize_database
from routes import blueprints

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

#デフォルトページ
@app.route('/')
def index():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True,port=8080)
