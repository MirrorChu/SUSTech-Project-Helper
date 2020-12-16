from django.db import models
from datetime import *
from items.users.models import BaseModel
from items.courses.models import Course


class Project(models.Model):
    group_ddl = models.DateTimeField(default=datetime.now, verbose_name="组队ddl")

    min_group_size = models.IntegerField(verbose_name="最小组队人数", default=4)

    name = models.CharField(verbose_name="项目名称", default="", max_length=50)

    introduction = models.TextField(verbose_name="项目名称", default="", max_length=65535)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="相应课程")
    # 多对一，Project是多，Course是一

    group_size = models.IntegerField(verbose_name="最大组队人数", default=4)

    class Meta:
        verbose_name = "项目信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

