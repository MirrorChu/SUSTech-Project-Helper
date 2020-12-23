import xadmin

from items.users.models import UserProfile


# 让后台管理系统能管理用户信息
class UserProfileAdmin(object):
    pass


xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
# 会自动将存储进数据库的密码加密，不可反解
