# 存放数据库的相关模型的文件


from exts import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户名
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)