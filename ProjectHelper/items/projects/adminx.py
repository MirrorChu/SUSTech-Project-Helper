import xadmin

from items.projects.models import Project


class ProjectAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["name", "course", "introduction", "group_size", "min_group_size", "group_ddl"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["course__name"]

    # 过滤器
    list_filter = ["name", "course", "introduction", "group_size", "min_group_size", "group_ddl"]

    # 可编辑
    list_editable = ["name", "course", "introduction", "group_size", "min_group_size", "group_ddl"]


xadmin.site.register(Project, ProjectAdmin)
