import xadmin

from items.groups.models import GroupOrg


class GroupAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["group_name", "captain_name", "members", "project"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["project__name"]

    # 过滤器
    list_filter = ["group_name", "captain_name", "members", "project"]

    # 可编辑
    list_editable = ["group_name", "captain_name", "members", "project"]


xadmin.site.register(GroupOrg, GroupAdmin)
