from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = (
    ("male", "男"),
    ("female", "女")
)


class BaseModel(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        abstract = True
    # BaseModel不需要对应有一个数据库，因此这里要让数据库不被创建


# 用户个人信息对应表的设计
class UserProfile(AbstractUser):
    # 后续完善功能时，可以用自定义字段来替换
    real_name = models.CharField(max_length=4, verbose_name="姓名", default="")
    student_id = models.CharField(max_length=8, verbose_name="学号", default="")
    gender = models.CharField(max_length=6, verbose_name="性别", choices=GENDER_CHOICES)
    address = models.CharField(max_length=50, verbose_name="住址", default="")
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    image = models.ImageField(verbose_name="头像", upload_to="head_image/%Y", default="head_image/%Y/default.jpg")
    # 用户上传的照片会自动保存到指定文件夹中，并以保持年份加月份来命名

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.real_name:
            return self.real_name
        else:
            return self.username
    # 支持用户修改姓名


