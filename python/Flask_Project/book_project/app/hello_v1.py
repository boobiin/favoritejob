# 应用模板
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
# 时间戳
from flask_moment import Moment
from datetime import datetime

# 配置数据库
import os
from flask_sqlalchemy import SQLAlchemy

# 定义表单类
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# 创建迁移仓库————数据库迁移框架
from flask_migrate import Migrate


"""
flask db init 用来添加数据库迁移支持
使用FLASK-Migrate管理数据库模式变化步骤
1. 对模型做必要的更改
2. 执行 flask db migrate 自动创建迁移脚本
3. 检查自动生成脚本，根据对模型的实际改动调整
4. 把迁移脚本纳入版本控制
5. 执行flask db upgrade 命令，把迁移应用到数据库中

"""

"""
    NameForm表单中有一个name文本字段和submit提交按钮
    StringField类表示属性为type=‘text’的HTML<input>元素。
    SubmitField类表示属性为type= ‘submit’的html<input>元素
    validators指定一个由验证函数组成的列表，接收数据之前验证数据。
    验证函数DataRequired()确保提交的字段不为空
"""


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)


# 数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 初始化FLASK-Migrate
migrate = Migrate(app, db)

"""
定义数据库模型
在ORM中，模型一般是一个Python类
类中的属性对应数据库表中的列
"""


# 定义数据库Role和User模型
# tablename为表名， Column为属性
# __repr__方法返回一个具有可读性的字符串表示模型，供调试和测试用
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 定义关系,users属性代表关系的面向对象视角
    # users属性返回与角色相关联的列表（一个角色多个用户）
    # backref为反向关系 db.relationship 向User模型中添加一个role属性
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    # 定义关系，role_id被定义为外键
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


# 渲染模板
# render_template()函数把 Jinja2 模板引擎集成到应用中
# 函数第一个参数是模板文件名，随后参数都是键-值对，表示模板变量具体值
"""
version 1.0
# 简单的应用模板，时间戳
@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())
    
"""

"""
version 2.0
# 将用户姓名表单提交，若无则产生提示
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name, current_time=datetime.utcnow())

"""

"""
# version 3.0
# 重定向和用户会话
//////////////////////////////////////////////////////////
应用 前一个版本局部变量name中存储用户在表单中输入的名字
这个变量保存在用户会话中即session['name']中
redirect()辅助函数用于生成HTTP重定向响应，参数是重定向URL
这里可以写作redirect('/')，现在使用了URL生成函数url_for()
//////////////////////////////////////////////////////////
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())

"""

"""
# version 4.0
 增加闪现消息
////////////////////////////////////////////////
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name= session.get('name'), current_time=datetime.utcnow())

"""

# version 5.0
# 在视图函数中操作数据库


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False),
                           current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# 添加一个shell上下文处理器
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


if __name__ == '__main__':
    app.run(debug=True)