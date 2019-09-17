
from flask import Flask, render_template, request, redirect, url_for, session
from models import User
from exts import db
import config


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 主页视图函数
@app.route('/')
def index():
    return render_template('index.html')

# 登录视图函数
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user_check = User.query.filter(User.username == username, User.password == password).first()
        if user_check:
            # 匹配以后，要想登录成功并且浏览器一直记住登录状态，需要设置cookie
            session['user_id'] = user_check.id
            # 想在31天内都不登陆(记住31天)
            # session.permanent = True
            return redirect(url_for('index'))
        else:
            return u' 用户名或者密码错误，请重试！ '

# 注册视图函数
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        password_check = request.form.get('password_check')

        # 判断用户名是否重复，并且判断第一次的密码与第二次的密码是否相同
        user = User.query.filter(User.username == username).first()
        # 找到用户
        if user:
            return u' 该用户名已被注册，请更改用户名! '

        # 未找到用户检查两次输入密码
        else:
            if password != password_check:
                return u' 两次密码输入不相同，请重试！ '

            # 检验正确，将数据写入数据库
            else:
                user_check = User(username=username, password=password)
                db.session.add(user_check)
                db.session.commit()
                # 如果注册成功，跳转到登录页面
                return redirect(url_for('login'))

# 注销函数
@app.route('/logout/')
def logout():

    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))


# 上下文钩子函数
@app.context_processor
def my_context_processor():
    # 通过session来判断用户是否登陆成功
    # 钩子函数返回的字典在所有文件中都可以用
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run(debug=True)