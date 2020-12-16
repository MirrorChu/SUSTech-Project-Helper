from datetime import datetime

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
    tag = models.ForeignKey(UserTag, on_delete=models.CASCADE, verbose_name="标签")

    class Meta:
        verbose_name = "用户点赞的标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name


# 记录每个项目发布页面下有谁评论了什么
class ProjectComment(BaseModel):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="评论用户的名称")
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="被评论项目的名称")
    comments = models.CharField(max_length=200, verbose_name="评论内容", default="")
    floor = models.CharField(max_length=200, verbose_name="类型", default="")

    class Meta:
        verbose_name = "项目评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project_name


class Event(BaseModel):
    publish_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目")
    type = models.CharField(max_length=200, verbose_name="类型", default="")
    parameter = models.TextField(max_length=65535, verbose_name="参数", default="")
    end_time = models.DateTimeField(default=datetime.now, verbose_name="截止日期")
    start_time = models.DateTimeField(default=datetime.now, verbose_name="开始日期")
    detail = models.TextField(max_length=65535, verbose_name="简介", default="")
    title = models.CharField(max_length=200, verbose_name="标题", default="")

    class Meta:
        verbose_name = "组件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project_id


# 记录每个项目有什么附件
class ProjectAttachment(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    group = models.ForeignKey(GroupOrg, on_delete=models.CASCADE, verbose_name="队伍")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="组件")
    file_path = models.CharField(max_length=200, verbose_name="文件路径", default="")

    class Meta:
        verbose_name = "项目附件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project


class Key(BaseModel):
    key_word = models.CharField(max_length=200, verbose_name="批次识别码", default="")

    class Meta:
        verbose_name = "老师上传项目附件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project


class ProjectFile(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目")
    file_path = models.CharField(max_length=200, verbose_name="文件路径", default="")

    class Meta:
        verbose_name = "老师上传项目附件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project


class EventGrades(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="组件")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    grade = models.IntegerField(verbose_name="成绩", default=0)
    comment = models.TextField(verbose_name="评论", default="", max_length=65535)

    class Meta:
        verbose_name = "项目成绩"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project


class ProjectGrades(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="组件")
    group = models.ForeignKey(GroupOrg, on_delete=models.CASCADE, verbose_name="队伍")
    grade = models.IntegerField(verbose_name="成绩", default=0)
    comment = models.TextField(verbose_name="评论", default="", max_length=65535)

    class Meta:
        verbose_name = "项目成绩"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project


# class ProjectDDL(BaseModel):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目")
#     ddl = models.DateTimeField(default=datetime.now, verbose_name="截止日期")
#     type = models.CharField(max_length=200, verbose_name="类型", default="")
#
#     class Meta:
#         verbose_name = "项目截止日期"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.project


class ChooseEvent(BaseModel):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="组件")
    choice = models.CharField(max_length=200, verbose_name="选择", default="")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")

    class Meta:
        verbose_name = "选择组件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.event_id


class ParticipantEvent(BaseModel):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="组件")
    end_time = models.DateTimeField(default=datetime.now, verbose_name="截止日期")
    start_time = models.DateTimeField(default=datetime.now, verbose_name="开始日期")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")

    class Meta:
        verbose_name = "时间选择组件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.event_id


class Authority(BaseModel):
    type = models.CharField(max_length=200, verbose_name="类型", default="")
    end_time = models.DateTimeField(default=datetime.now, verbose_name="截止日期")
    start_time = models.DateTimeField(default=datetime.now, verbose_name="开始日期")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type


class Annexation(BaseModel):
    a = models.CharField(max_length=200, verbose_name="a", default="")
    b = models.CharField(max_length=200, verbose_name="b", default="")
    c = models.CharField(max_length=200, verbose_name="c", default="")
    d = models.CharField(max_length=200, verbose_name="d", default="")
    e = models.CharField(max_length=200, verbose_name="e", default="")
    f = models.CharField(max_length=200, verbose_name="f", default="")
    g = models.CharField(max_length=200, verbose_name="g", default="")
    h = models.CharField(max_length=200, verbose_name="h", default="")
    i = models.CharField(max_length=200, verbose_name="i", default="")
    j = models.CharField(max_length=200, verbose_name="j", default="")

    class Meta:
        verbose_name = "Annexation"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.a

# # 记录谁向另一个人发送了聊天消息
# class UserMessage(BaseModel):
#     receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="接收方", default="")
#     sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="发送方", default="")
#     receiver_is_read = models.BooleanField(default=False, verbose_name="接收方是否已读")
#     sender_is_read = models.BooleanField(default=False, verbose_name="发送方是否已读")
#     content = models.TextField(verbose_name="内容", default="", max_length=65535)
#     send_time = models.DateTimeField(verbose_name="发送时间")
#
#     class Meta:
#         verbose_name = "聊天消息"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.receiver
#
#
# # 记录每个队都有谁申请加入
# class UserAsk(BaseModel):
#     receiver_group = models.ForeignKey(GroupOrg, on_delete=models.CASCADE, verbose_name="接收申请的队伍")
#     sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="发出申请的用户")
#
#     receiver_group_is_read = models.BooleanField(default=False, verbose_name="接收方是否已读")
#     sender_is_read = models.BooleanField(default=False, verbose_name="发送方是否已读")
#     is_accepted = models.BooleanField(default=False, verbose_name="是否已接受")
#
#     request_send_time = models.DateTimeField(verbose_name="申请发送时间")
#     request_receive_time = models.DateTimeField(verbose_name="申请接收时间")
#
#     reply_send_time = models.DateTimeField(verbose_name="申请回复发送时间")
#     reply_receive_time = models.DateTimeField(verbose_name="申请回复接收时间")
#
#     class Meta:
#         verbose_name = "组队申请"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.receiver_group
#
#
# # 记录每个队都有谁申请加入
# class UserInvite(BaseModel):
#     receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="接收邀请的用户")
#     sender_group = models.ForeignKey(GroupOrg, on_delete=models.CASCADE, verbose_name="发出邀请的用户")
#
#     receiver_is_read = models.BooleanField(default=False, verbose_name="接收方是否已读")
#     sender_group_is_read = models.BooleanField(default=False, verbose_name="发送方是否已读")
#     is_accepted = models.BooleanField(default=False, verbose_name="是否已接受")
#
#     request_send_time = models.DateTimeField(verbose_name="邀请发送时间")
#     request_receive_time = models.DateTimeField(verbose_name="邀请接收时间")
#
#     reply_send_time = models.DateTimeField(verbose_name="申请回复发送时间")
#     reply_receive_time = models.DateTimeField(verbose_name="申请回复接收时间")
#
#     class Meta:
#         verbose_name = "组队邀请"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.receiver