# encoding: utf-8
import os

# 定义参数及session参数
DEBUG = True
SECRET_KEY = os.urandom(20)

# dialect+driver://username:password@host:port/database
# mysql连接配置参数
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'login_demo'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                       PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False