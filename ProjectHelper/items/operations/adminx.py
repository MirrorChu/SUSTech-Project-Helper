import xadmin

from django.contrib.auth import get_user_model

from items.operations.models import UserCourse, UserAsk, UserComment, UserGroup, UserMessage

UserProfile = get_user_model()


class UserCourseAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["user_name", "course_name", "lab"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["course_name__name"]

    # 过滤器
    list_filter = ["user_name", "course_name", "lab"]

    # 可编辑
    list_editable = ["user_name", "course_name", "lab"]


class UserAskAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["user_name", "group_name"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["group_name__name"]

    # 过滤器
    list_filter = ["user_name", "group_name"]

    # 可编辑
    list_editable = ["user_name", "group_name"]


class UserCommentAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["user_name", "group_name", "comments"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["user_name__username"]

    # 过滤器
    list_filter = ["user_name", "group_name", "comments"]

    # 可编辑
    list_editable = ["user_name", "group_name", "comments"]


class UserGroupAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["user_name", "group_name"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["group_name__name"]

    # 过滤器
    list_filter = ["user_name", "group_name"]

    # 可编辑
    list_editable = ["user_name", "group_name"]


class UserMessageAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["receiver_name", "sender_name", "message", "is_read"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["receiver_name__username"]

    # 过滤器
    list_filter = ["receiver_name", "sender_name", "message", "is_read"]

    # 可编辑
    list_editable = ["receiver_name", "sender_name", "message", "is_read"]


xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserAsk,  UserAskAdmin)
xadmin.site.register(UserComment,  UserCommentAdmin)
xadmin.site.register(UserGroup,  UserGroupAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)

