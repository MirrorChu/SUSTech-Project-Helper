"""ProjectHelper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

import xadmin

from items.users.views import Login, ChangePassword, ShowPersonalData, \
    UploadFile, DownloadFile, Test, StudentGetsAllProjects, \
    StudentGetsSingleProjectInformation, StudentGetsAllGroups, \
    StudentGetsSingleGroupInformation, StudentCreatesGroup, \
    EditsGroupIntroduction, EditsGroupName, GroupMemberValidation, \
    StudentQuitsGroup, CaptainKickMember, CaptainDismissGroup, \
    CaptainGiveCaptain, ChangePersonalData, StudentGetAllGroupsInProject, \
    ShowHeadImage, ChangeHeadImage, StudentGetAllStudentsInProject, MailUrl, \
    SendMailToInvite, StudentGetProject, StudentGetsGroupInformationInProject, \
    StudentGetValidGroupInProject, ShowOtherPersonalData, StudentGetsAllTags, TeacherGetCourses, \
    StudentLikeTag, TeacherGetStudentsInCourse, TeacherCreateProject, TestFile, \
    SendKey, StudentGetsAllTagsCanAdd, UnshowTag, AddTag, StudentPublishRequest, \
    StudentPublishApply, StudentGetAllAd, GetIdentity, Logout, TeacherKickMember, \
    TeacherGetSituationInProject, TeacherGetSingleInProject, TeacherAddMember, \
    AddNewTag, SendMailToApply, GetPrivilegeList, GetEventList, GetAllPrivilegeList, \
    CreateEvent, GetEventDetail, DeleteEvent

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),

    # 配置首页的路径
    path('', TemplateView.as_view(template_name="index.html"), name="index"),

    path('login/', Login.as_view()),
    path('change_password/', ChangePassword.as_view()),
    path('show_personal_data/', ShowPersonalData.as_view()),
    path('change_personal_data/', ChangePersonalData.as_view()),
    path('upload_file/', UploadFile.as_view()),
    path('download_file/', DownloadFile.as_view()),
    path('test/', Test.as_view()),
    path('student_gets_all_projects/', StudentGetsAllProjects.as_view()),
    path('student_gets_single_project_information/', StudentGetsSingleProjectInformation.as_view()),
    path('student_gets_all_groups/', StudentGetsAllGroups.as_view()),
    path('student_gets_single_group_information/', StudentGetsSingleGroupInformation.as_view()),
    path('student_creates_group/', StudentCreatesGroup.as_view()),
    path('edits_group_introduction/', EditsGroupIntroduction.as_view()),
    path('edits_group_name/', EditsGroupName.as_view()),
    path('group_member_validation/', GroupMemberValidation.as_view()),
    path('student_quits_group/', StudentQuitsGroup.as_view()),
    path('captain_kick_member/', CaptainKickMember.as_view()),
    path('captain_dismiss_group/', CaptainDismissGroup.as_view()),
    path('captain_give_captain/', CaptainGiveCaptain.as_view()),
    path('student_get_all_groups_in_project/', StudentGetAllGroupsInProject.as_view()),
    path('student_get_all_students_in_project/', StudentGetAllStudentsInProject.as_view()),
    path('show_head_image/', ShowHeadImage.as_view()),
    path('change_head_image/', ChangeHeadImage.as_view()),
    path('send_mail_to_invite/', SendMailToInvite.as_view()),
    path('send_mail_to_apply/', SendMailToApply.as_view()),
    path('student_get_project/', StudentGetProject.as_view()),
    path('student_gets_group_information_in_project/', StudentGetsGroupInformationInProject.as_view()),
    path('student_get_valid_group_in_project/', StudentGetValidGroupInProject.as_view()),
    path('show_other_personal_data/', ShowOtherPersonalData.as_view()),
    path('student_gets_all_tags_can_add/', StudentGetsAllTagsCanAdd.as_view()),
    path('student_gets_all_tags/', StudentGetsAllTags.as_view()),
    path('teacher_get_courses/', TeacherGetCourses.as_view()),
    path('student_like_tag/', StudentLikeTag.as_view()),
    path('teacher_get_students_in_course/', TeacherGetStudentsInCourse.as_view()),
    path('teacher_create_project/', TeacherCreateProject.as_view()),
    path('test_file/', TestFile.as_view()),
    path('send_key/', SendKey.as_view()),
    path('unshow_tag/', UnshowTag.as_view()),
    path('add_tag/', AddTag.as_view()),
    path('add_new_tag/', AddNewTag.as_view()),
    path('student_publish_request/', StudentPublishRequest.as_view()),
    path('student_publish_apply/', StudentPublishApply.as_view()),
    path('student_gets_all_ad/', StudentGetAllAd.as_view()),
    path('get_identity/', GetIdentity.as_view()),
    path('logout/', Logout.as_view()),
    path('teacher_get_situation_in_project/', TeacherGetSituationInProject.as_view()),
    path('teacher_get_single_in_project/', TeacherGetSingleInProject.as_view()),
    path('teacher_kick_member/', TeacherKickMember.as_view()),
    path('teacher_add_member/', TeacherAddMember.as_view()),
    path('get_privilege_list/', GetPrivilegeList.as_view()),
    path('get_all_privilege_list/', GetAllPrivilegeList.as_view()),
    path('get_event_list/', GetEventList.as_view()),
    path('create_event/', CreateEvent.as_view()),
    path('delete_event/', DeleteEvent.as_view()),
    path('get_event_detail/', GetEventDetail.as_view()),
    url(r'^mailurl/$', MailUrl.as_view()),

    # 传入name使得不同子目录也能对应同一个网页，比如path('login2', LoginView.as_view(), name="login")也能对应登录网页

]
# 访问函数view的实现方法可以基于类(class base view)，也可以基于函数(function base view)，而这里选择前者是因为它便于维护
# curl -H "Content-Type:application/json" -X POST --data "{'sid': '3012345', 'pswd': '3012345'}" http://localhost:8000/teacher_get_courses/
