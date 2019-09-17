
# 通过Flask-Script以通过命令行的形式来操作Flask
# 通过命令行来操作迁移数据库

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from login_demo import app
from exts import db

# 需要在manage中导入模型，才能将模型映射到数据库中
from models import User

# 初始化 Manger
manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本到manger中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

