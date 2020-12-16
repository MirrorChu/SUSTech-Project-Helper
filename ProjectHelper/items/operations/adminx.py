import xadmin

from django.contrib.auth import get_user_model

from items.operations.models import UserCourse, UserComment, UserGroup, Tag, UserTag, UserLikeTag, UserLikeTag, \
    ProjectComment, Event, ProjectAttachment, ProjectFile, EventGrades, ProjectGrades, ChooseEvent, ParticipantEvent, \
    Authority

UserProfile = get_user_model()


class AuthorityAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["user", "start_time", "end_time", "type", "course"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["user__real_name"]

    # 过滤器
    list_filter = ["user", "start_time", "end_time", "type", "course"]

    # 可编辑
    list_editable = ["user", "start_time", "end_time", "type", "course"]


class ParticipantEventAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["event_id", "start_time", "end_time", "user"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["event_id__title"]

    # 过滤器
    list_filter = ["event_id", "start_time", "end_time", "user"]

    # 可编辑
    list_editable = ["event_id", "start_time", "end_time", "user"]


class ChooseEventAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["event_id", "choice", "user"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["event_id__title"]

    # 过滤器
    list_filter = ["event_id", "choice", "user"]

    # 可编辑
    list_editable = ["event_id", "choice", "user"]


class ProjectGradesAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["event", "group", "grade", "comment"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["group__name"]

    # 过滤器
    list_filter = ["event", "group", "grade", "comment"]

    # 可编辑
    list_editable = ["event", "group", "grade", "comment"]


class EventGradesAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["event", "user", "grade", "comment"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["user__real_name"]

    # 过滤器
    list_filter = ["event", "user", "grade", "comment"]

    # 可编辑
    list_editable = ["event", "user", "grade", "comment"]


class ProjectFileAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["project", "file_path"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["project__name"]

    # 过滤器
    list_filter = ["project", "file_path"]

    # 可编辑
    list_editable = ["project", "file_path"]


class ProjectAttachmentAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["project", "user", "event", "group", "file_path"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["event__title"]

    # 过滤器
    list_filter = ["project", "user", "event", "group", "file_path"]

    # 可编辑
    list_editable = ["project", "user", "event", "group", "file_path"]


class EventAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["project", "publish_user", "type", "parameter", "start_time", "end_time", "detail", "title"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["title"]

    # 过滤器
    list_filter = ["project", "publish_user", "type", "parameter", "start_time", "end_time", "detail", "title"]

    # 可编辑
    list_editable = ["project", "publish_user", "type", "parameter", "start_time", "end_time", "detail", "title"]



class ProjectCommentAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["project_name", "user_name", "comments", "floor"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["user_name__real_name"]

    # 过滤器
    list_filter = ["project_name", "user_name", "comments", "floor"]

    # 可编辑
    list_editable = ["project_name", "user_name", "comments", "floor"]


class UserLikeTagAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["tag", "user_name"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["user_name__real_name"]

    # 过滤器
    list_filter = ["tag", "user_name"]

    # 可编辑
    list_editable = ["tag", "user_name"]


class UserTagAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["tag", "user_name", "visibility"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["user_name__real_name"]

    # 过滤器
    list_filter = ["tag", "user_name", "visibility"]

    # 可编辑
    list_editable = ["tag", "user_name", "visibility"]


class TagAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["tag", "type"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["tag"]

    # 过滤器
    list_filter = ["tag", "type"]

    # 可编辑
    list_editable = ["tag", "type"]


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
    search_fields = ["user_name__real_name"]

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
    search_fields = ["receiver_name__real_name"]

    # 过滤器
    list_filter = ["receiver_name", "sender_name", "message", "is_read"]

    # 可编辑
    list_editable = ["receiver_name", "sender_name", "message", "is_read"]


xadmin.site.register(Authority, AuthorityAdmin)
xadmin.site.register(ParticipantEvent, ParticipantEventAdmin)
xadmin.site.register(ChooseEvent, ChooseEventAdmin)
xadmin.site.register(ProjectGrades, ProjectGradesAdmin)
xadmin.site.register(EventGrades, EventGradesAdmin)
xadmin.site.register(ProjectFile, ProjectFileAdmin)
xadmin.site.register(ProjectAttachment, ProjectAttachmentAdmin)
xadmin.site.register(Event, EventAdmin)
xadmin.site.register(ProjectComment, ProjectCommentAdmin)
xadmin.site.register(UserLikeTag, UserLikeTagAdmin)
xadmin.site.register(UserTag, UserTagAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
# xadmin.site.register(UserAsk,  UserAskAdmin)
xadmin.site.register(UserComment,  UserCommentAdmin)
xadmin.site.register(UserGroup,  UserGroupAdmin)
# xadmin.site.register(UserMessage, UserMessageAdmin)

