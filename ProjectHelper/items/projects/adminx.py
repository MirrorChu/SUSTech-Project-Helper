import xadmin

from items.projects.models import Project


class ProjectAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["project_name", "course"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["course__name"]

    # 过滤器
    list_filter = ["project_name", "course"]

    # 可编辑
    list_editable = ["project_name", "course"]


xadmin.site.register(Project, ProjectAdmin)
