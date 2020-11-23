from django.db import models

from django.contrib.auth import get_user_model

from items.users.models import BaseModel
from items.groups.models import GroupOrg
from items.courses.models import Course
from items.projects.models import Project

UserProfile = get_user_model()


class Tag(BaseModel):
    tag = models.CharField(verbose_name="标签", max_length=50, default="")

    # 加分项：不同类型的标签相应的颜色不同
    type = models.CharField(verbose_name="属性", max_length=50, default="")

    class Meta:
        verbose_name = "标签清单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


# 以下记录的都是多对多的关系
# 记录每个人都有上哪些课
class UserCourse(BaseModel):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户名称")
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="所在课程的名称")
    lab = models.CharField(verbose_name="实验班名称", max_length=1)

    class Meta:
        verbose_name = "课程清单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name


# 记录每个队都有谁申请加入
class UserAsk(BaseModel):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="申请用户的名称")
    group_name = models.ForeignKey(GroupOrg, on_delete=models.CASCADE, verbose_name="申请加入队伍的名称")

    class Meta:
        verbose_name = "组队申请"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group_name


# 记录每个队有谁评论了什么，队伍成员也能在评论区发表内容
class UserComment(BaseModel):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="评论用户的名称")
    group_name = models.ForeignKey(GroupOrg, on_delete=models.CASCADE, verbose_name="被评论队伍的名称")
    comments = models.CharField(max_length=200, verbose_name="评论内容")

    class Meta:
        verbose_name = "队伍评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group_name


# 记录所有用户组队的信息，还没实现：限制一门课只能组一个队
class UserGroup(BaseModel):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户的名称")
    group_name = models.ForeignKey(GroupOrg, on_delete=models.CASCADE, verbose_name="已加入队伍的名称")

    class Meta:
        verbose_name = "组队情况"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group_name


# 记录所有用户的聊天消息
class UserMessage(BaseModel):
    receiver_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                      verbose_name="接收方的用户名称", related_name='receiver')
    sender_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                    verbose_name="发出方的用户名称", related_name='sender')
    message = models.CharField(max_length=200, verbose_name="消息内容")
    is_read = models.BooleanField(default=False, verbose_name="消息是否已读取")
    # False代表没有读

    class Meta:
        verbose_name = "消息记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.receiver_name


class UserTag(BaseModel):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户名称")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="标签")
    visibility = models.IntegerField(verbose_name="可见度", default=1)

    class Meta:
        verbose_name = "用户拥有的标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name


class UserLikeTag(BaseModel):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户名称")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="标签")

    class Meta:
        verbose_name = "用户点赞的标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name


# 记录每个项目发布页面下有谁评论了什么
class ProjectComment(BaseModel):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="评论用户的名称")
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="被评论项目的名称")
    comments = models.CharField(max_length=200, verbose_name="评论内容")

    class Meta:
        verbose_name = "项目评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project_name
