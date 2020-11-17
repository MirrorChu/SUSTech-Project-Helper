import xadmin

from items.courses.models import Course


class GlobalSettings(object):
    # 设置左上角标题的内容
    site_title = "南科组队"

    # 设置底部角标题的内容
    site_footer = "SUSTech-Project-Helper"


# 设置装饰主题
class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class CourseAdmin(object):
    # 让后台管理系统预先显示指定列
    list_display = ["name"]

    # 让后台管理系统能搜索指定标签
    search_fields = ["name"]

    # 可编辑
    list_editable = ["name"]


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)