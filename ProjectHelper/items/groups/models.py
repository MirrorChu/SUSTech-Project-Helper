from django.db import models
from django.contrib.auth import get_user_model

from items.users.models import BaseModel
from items.projects.models import Project

UserProfile = get_user_model()


class GroupOrg(models.Model):
    group_name = models.CharField(verbose_name="队伍名称", max_length=50, unique=True)

    # 队长是队伍的创始人，只有队长会收到申请，并且决定是否接受
    captain_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="队长名称")

    members = models.IntegerField(verbose_name="成员人数")

    detail = models.TextField(verbose_name="队伍详情")

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="相应项目", null=True)
    # 多对一，GroupOrg是多，Project是一

    class Meta:
        verbose_name = "队伍信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group_name
