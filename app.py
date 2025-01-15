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

@app.route('/register')  
def register():
    return render_template('register.html') 

@app.route('/login')  
def backlogin():
    return render_template('login.html') 


#user管理画面------------------------------------------------------------------------------------------------------
@app.route('/user', methods=['GET'])
def user():
    users = User.select()
    return render_template('user_manage.html', users=users)


if __name__ == '__main__':
    app.run(debug=True,port=8080)
