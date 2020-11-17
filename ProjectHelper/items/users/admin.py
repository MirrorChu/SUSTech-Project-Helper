from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from items.users.models import UserProfile


# 让后台管理系统能管理用户信息
class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserAdmin)
# 会自动将存储进数据库的密码加密，不可反解
