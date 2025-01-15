from flask import render_template, request, redirect, url_for, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

# Blueprintの作成
login_bp = Blueprint('login', __name__, url_prefix='/login')

#ログイン用------------------------------------------------------------------------------------------------------
@login_bp.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # データベースからユーザーを取得
        user = User.get_or_none(User.username == username)
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id#id取得
            session['user_name'] = user.username#URLにユーザー名を表示させたいため取得
            print(f"user_id = {session['user_id']}")#確認用
            print(f"user_name = {session['user_name']}")#確認用
            #return render_template('index.html')
            return redirect(url_for('login.index', user_name = session['user_name']))
        else:
            return render_template('login.html')
    return render_template('login.html')


#ホーム画面------------------------------------------------------------------------------------------------------
@login_bp.route('/index/<user_name>')
def index(user_name):
    return render_template('index.html', user_name = user_name)


#ログアウト用------------------------------------------------------------------------------------------------------
@login_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login.login'))


# ユーザー登録用------------------------------------------------------------------------------------------------------
@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ユーザーがすでに存在するか確認
        if User.get_or_none(User.username == username):
            return redirect(url_for('register'))

        # 新しいユーザーを作成
        hashed_password = generate_password_hash(password)
        User.create(username=username, password=hashed_password)
        return redirect(url_for('login.login'))

    return render_template('register.html')

