from hello_v1 import db
from hello_v1 import Role, User

# 创建相应的表
db.create_all()

# 插入行
admin_role = Role(name='Admin')
mod_role = Role(name='Moderator')
user_role = Role(name='User')
user_john = User(username='john', role=admin_role)
user_susan = User(username='susan', role=user_role)
user_david = User(username='david', role=user_role)

# 添加会话
db.session.add_all([admin_role, mod_role, user_role, user_john,
                    user_susan, user_david])

# 每次更改会话后，都需要提交会话
db.session.commit()

# 修改行:更改相关变量，再添加、提交会话

# 删除行 ps:删除相关角色
# db,session.delete(mod_role)
# db.session.commit()

"""
# 查询行 
 Role.query.all()
 User.query.all()
# 也可以使用过滤器
# 查找role=user_role的角色
User.query.filter_by(role=user_role).all()
"""

