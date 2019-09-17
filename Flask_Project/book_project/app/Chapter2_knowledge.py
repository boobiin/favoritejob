# Flask用这个参数确定应用位置
"""初始化Flask"""
from flask import Flask
app = Flask(__name__)

# 客户端向Web服务器发送请求
# Web服务器再把请求发送给Flask应用实例
# 应用实例需要知道每个URL请求需要运行那些代码
# 应用实例需要保存URL到Python函数的映射关系，处理URL与函数关系称为路由

"""使用app.route装饰器声明路由"""
@app.route('/')
def index():
    return'<h1>Hello World!</h1>'

"""
使用app.add_url_rule()方法注册index()函数

def index():
    return '<h1>Hello World!</h1>'
# URL、端点名、视图函数为app.add_url_rule的三个参数
app.add_url_rule('/', 'index', index)
"""

# 可变的URL
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)