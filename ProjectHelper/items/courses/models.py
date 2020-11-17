from django.db import models

from items.users.models import BaseModel


class Course(BaseModel):
    name = models.CharField(verbose_name="课程名称", max_length=50)

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    # 让后台管理系统把name显示为对象名称，而非Course Object
    def __str__(self):
        return self.name
