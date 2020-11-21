from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import sys
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from items.groups.models import GroupOrg
from items.users.models import UserProfile
from items.operations.models import UserCourse, UserGroup
from items.courses.models import Course
from items.projects.models import Project


class LoginView(View):
    @method_decorator(ensure_csrf_cookie)
    # def get(self, request, *args, **kwargs):
    #     return render(request, "login.html")

    # 当用户按下登录按键时
    def post(self, request):
        try:
            print(request.body)

            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.filter(username=student_id, password=password)
            # 如果能查询到相应记录
            if user.count() == 0:
                return JsonResponse({"LoginCheck": "Login failed!"})
            # 如果未能查询到用户
            else:
                return JsonResponse({"LoginCheck": "Login success!"})

        except Exception as e:
            return JsonResponse({"ChangePasswordCheck": "failed"})


class ChangePasswordView(View):
    # 当用户按下登录按键时
    def post(self, request):
        try:
            print(request.body)

            student_id = eval(request.body.decode()).get("sid")
            old_password = eval(request.body.decode()).get("old_pswd")
            new_password = eval(request.body.decode()).get("new_pswd")

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.filter(username=student_id, password=old_password)
            # 如果能查询到相应记录
            if user.count() == 0:
                return JsonResponse({"ChangePasswordCheck": "Change failed!"})
            # 如果未能查询到用户
            else:
                user.update(password=new_password)
                return JsonResponse({"ChangePasswordCheck": "Change success!"})

        except Exception as e:
            return JsonResponse({"ChangePasswordCheck": "failed"})


class ShowPersonalDataView(View):
    # 当用户按下登录按键时
    def post(self, request):
        try:
            # file = request.FILES.get('file')
            # print(type(file))
            # path = default_storage.save('tmp/'+str(request.FILES.get('file')), ContentFile(file.read()))  # 根据名字存图
            # return JsonResponse({
            #                          "image": file
            #                          })
            arr = request.FILES.keys()
            file_name = ''
            message = {}

            for k in arr:
                file_name = k

            if file_name != '':
                file = request.FILES.get(file_name)
                path = default_storage.save('tmp/' + file_name, ContentFile(file.read()))  # 根据名字存图(无类型)

                message = {'code': 200}
            return JsonResponse(message)

        except Exception as e:
            return JsonResponse({"ShowPersonalData": "failed"})
        # student_id = eval(request.body.decode()).get("sid")
        # password = eval(request.body.decode()).get("pswd")
        #
        # # 通过用户名和密码确认数据库中是否有和user对应的记录
        # user = UserProfile.objects.filter(username=student_id, password=password)
        # # 如果能查询到相应记录
        # if user.count() == 0:
        #     return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData failed!"})
        # # 如果未能查询到用户
        # else:
        #     x = UserProfile.objects.get(username=student_id, password=password)
        #     file_path = x.image
        #     file = open(file_path, "rb")
        #
        #     return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData success!",
        #                          "realname": x.real_name,
        #                          "student_id": x.student_id,
        #                          "gender": x.gender,
        #                          "address": x.address,
        #                          "email": x.email,
        #                          "mobile": x.mobile,
        #                          "image": file
        #                          })


class UploadFile(View):

    def post(self, request):
        try:
            print(request.body)

            file_obj = request.FILES.get('file', None)

            if not file_obj:
                return JsonResponse({"UploadFileCheck": "failed"})
            else:
                print("file_obj", file_obj.name)

                file_path = os.path.join('static', 'files_uploaded', file_obj.name)

                print("file_path", file_path)

                with open(file_path, 'wb+') as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)

                return JsonResponse({"UploadFileCheck": "success"})

        except Exception as e:
            return JsonResponse({"UploadFileCheck": "failed"})


class DownloadFile(View):
    def post(request):
        try:
            print(request.body)

            path = eval(request.body.decode()).get("path")
            file_name = eval(request.body.decode()).get("file_name")

            file_obj = open(path, 'rb')

            response = HttpResponse(file_obj)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = "attachment;filename=" + file_name
            return response
        except Exception as e:
            return JsonResponse({"DownloadFile": "failed"})


class Test(View):
    def get(self, request):
        print(request.body)
        message = {'code': 200}
        return JsonResponse(message)

    def post(self, request):
        print(request.body)

        file = open('static/11811002.zip', 'rb').read()
        response = HttpResponse(file)
        print(file)
        response['Content-Type'] = 'application/zip'
        response['Content-Disposition'] = 'attachment; filename=11811002.zip'

        return response


class StudentGetsAllProjects(View):
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            user = UserProfile.objects.filter(username=student_id, password=password)
            for i in user:
                course = UserCourse.objects.filter(user_name_id=i.id)
            courses = {}
            for i in course:
                courseObject = Course.objects.filter(id=i.course_name_id)
                for j in courseObject:
                    name = j.name
                    courses[name] = {}
                    projects = Project.objects.filter(course_id=j.id)
                for j in projects:
                    courses[name][j.id] = j.name
            return JsonResponse({"GetProjectsCheck": courses})

        except Exception as e:
            return JsonResponse({"StudentGetsAllProjects": "failed"})
    # 返回{课程名：{项目ID:项目名，}，}


class StudentGetsSingleProjectInformation(View):
    def post(self, request):
        try:
            project_id = eval(request.body.decode()).get("project_id")
            query_set = Project.objects.filter(id=project_id)

            project_name = ""
            project_introduction = ""
            course_name = ""

            for i in query_set:
                project_name = i.name
                project_introduction = i.introduction
                course = i.course_id
                query_set = Course.objects.filter(id=course)
                for j in query_set:
                    course_name = j.name

            return JsonResponse({"project_name": project_name, "project_introduction": project_introduction,
                                 "course_name": course_name})
        except Exception as e:
            return JsonResponse({"StudentGetsSingleProjectInformation": "failed"})

        # 返回{项目名, 项目简介, 课程名}


class StudentGetsAllGroups(View):
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            user = UserProfile.objects.filter(username=student_id, password=password)
            for i in user:
                # 获得学生参加的所有队伍
                group_id = UserGroup.objects.filter(user_name_id=i.id)

            groups = {}
            for i in group_id:
                group_obj = GroupOrg.objects.filter(id=i.group_name_id)
                for j in group_obj:
                    group_name = j.group_name
                    groups[group_name] = []
                    groups[group_name].append(j.id)

                    project_id = j.project_id
                    groups[group_name].append(project_id)
                    project = Project.objects.filter(id=project_id)
                    for k in project:
                        project_name = k.name
                        groups[group_name].append(project_name)
                        course_id = k.course_id
                        groups[group_name].append(course_id)
                        course = Course.objects.filter(id=course_id)
                        for l in course:
                            course_name = l.name
                            groups[group_name].append(course_name)
            return JsonResponse(groups)
        except Exception as e:
            return JsonResponse({"StudentGetsAllGroups": "failed"})

    # 返回{队伍名:[队伍id,项目id,项目名,课程id,课程名],}


class StudentGetsSingleGroupInformation(View):
    def post(self, request):
        try:
            group_id = eval(request.body.decode()).get("group_id")
            query_set = GroupOrg.objects.filter(id=group_id)

            group_name = ""
            group_detail = ""
            project_name = ""
            course_name = ""
            captain_name = ""
            captain_id = 0
            project_id = 0
            course_id = 0
            members = []

            for i in query_set:
                group_name = i.group_name
                group_detail = i.detail
                captain_id = i.captain_name_id
                project_id = i.project_id

                query_set = Project.objects.filter(id=project_id)
                for j in query_set:
                    project_name = j.name
                    course_id = j.course_id
                    query_set = Course.objects.filter(id=project_id)
                    for k in query_set:
                        course_name = k.name

                query_set = UserProfile.objects.filter(id=captain_id)
                for j in query_set:
                    captain_name = j.username

                query_set = UserGroup.objects.filter(id=group_id)
                for j in query_set:
                    user_id = j.user_name_id
                    query_set = UserProfile.objects.filter(id=user_id)
                    for k in query_set:
                        members.append(k.username)

            return JsonResponse({"group_name": group_name,
                                 "group_introduction": group_detail,
                                 "project_id": project_id,
                                 "project_name": project_name,
                                 "course_id": course_id,
                                 "course_name": course_name,
                                 "captain_name": captain_name,
                                 "members": members,
                                 })
        except Exception as e:
            return JsonResponse({"StudentGetsSingleGroupInformation": "failed"})
        # 返回{队伍名，队伍简介,项目id,项目名,课程id,课程名,队长学号,[队伍成员1学号,队伍成员2学号,...]}


class StudentCreatesGroup(View):
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            group_name = eval(request.body.decode()).get("group_name")
            introduction = eval(request.body.decode()).get("introduction")
            project_id = eval(request.body.decode()).get("project_id")

            query_set = UserProfile.objects.filter(username=student_id, password=password)
            captain_id = 0
            members = 1

            for i in query_set:
                captain_id = i.id

            # create group
            GroupOrg.objects.create(group_name=group_name,
                                    members=members,
                                    detail=introduction,
                                    captain_name_id=captain_id,
                                    project_id=project_id
                                    )

            # update user_group
            query_set = GroupOrg.objects.filter(group_name=group_name, captain_name_id=captain_id, project_id=project_id)
            for i in query_set:
                UserGroup.objects.create(group_name_id=i.id, user_name_id=captain_id)

            return JsonResponse({"CreatesGroupCheck": "success"})

        except Exception as e:
            return JsonResponse({"CreatesGroupCheck": "failed"})


class EditsGroupIntroduction(View):
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            group_id = eval(request.body.decode()).get("group_id")

            introduction = ""
            query_set = GroupOrg.objects.filter(id=group_id)
            for i in query_set:
                introduction = i.detail
                i.update(detail=introduction)

            # 后面可能要做站内信功能，记录谁修改了简介，所以先留着学号和密码

            return JsonResponse({"EditsGroupIntroductionCheck": "success"})

        except Exception as e:
            return JsonResponse({"EditsGroupIntroductionCheck": "failed"})


class EditsGroupName(View):
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            group_id = eval(request.body.decode()).get("group_id")

            group_name = ""
            query_set = GroupOrg.objects.filter(id=group_name)
            for i in query_set:
                group_name = i.group_name
                i.update(group_name=group_name)

            return JsonResponse({"EditsGroupNameCheck": "success"})

        except Exception as e:
            return JsonResponse({"EditsGroupNameCheck": "failed"})


class GroupMemberValidation(View):
    def get(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            group_id = eval(request.body.decode()).get("group_id")

            user_id = 0

            query_set = UserProfile.objects.filter(username=student_id, password=password)
            for i in query_set:
                user_id = i.id

            query_set = UserGroup.objects.filter(user_name_id=user_id, group_name_id=group_id)
            if query_set.count() == 0:
                return JsonResponse({"GroupMemberValidation": "guest"})

            query_set = GroupOrg.objects.filter(id=group_id, captain_name_id=user_id)
            if query_set.count() == 0:
                return JsonResponse({"GroupMemberValidation": "member"})
            else:
                return JsonResponse({"GroupMemberValidation": "captain"})

        except Exception as e:
            return JsonResponse({"GroupMemberValidation": "failed"})


class StudentQuitsGroup(View):
    def post(self, request):
        try:
            group_id = eval(request.body.decode()).get("group_id")
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            user = UserProfile.objects.filter(student_id=student_id, password=password)
            for i in user:
                user_id = i.id
            group = GroupOrg.objects.filter(group_name_id=group_id)
            mem = 0
            for i in group:
                mem = i.member - 1
            GroupOrg.objects.filter(group_name_id=group_id).update(member=mem)
            UserGroup.objects.delete(group_name_id=group_id, user_name_id=user_id)
            return JsonResponse({"StudentQuitGroupCheck": "success"})
        except Exception as e:
            return JsonResponse({"StudentQuitGroupCheck": "failed"})


class CaptainKickMember(View):
    def post(self, request):
        try:
            group_id = eval(request.body.decode()).get("group_id")
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            target_id = eval(request.body.decode()).get("t_sid")

            user = UserProfile.objects.filter(student_id=student_id, password=password)
            if user.count() == 0:
                return JsonResponse({"CaptainKickMemberCheck": "failed"})
            group = GroupOrg.objects.filter(group_name_id=group_id)
            mem = 0
            for i in group:
                mem = i.member - 1
            GroupOrg.objects.filter(group_name_id=group_id).update(member=mem)
            UserGroup.objects.delete(group_name_id=group_id, user_name_id=target_id)
            return JsonResponse({"CaptainKickMemberCheck": "success"})
        except Exception as e:
            return JsonResponse({"CaptainKickMemberCheck": "failed"})


class CaptainDismissGroup(View):
    def post(self, request):
        try:
            group_id = eval(request.body.decode()).get("group_id")
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            user = UserProfile.objects.filter(student_id=student_id, password=password)
            if user.count() == 0:
                return JsonResponse({"CaptainDismissGroupCheck": "failed"})
            GroupOrg.objects.delete(group_name_id=group_id)
            UserGroup.objects.delete(group_name_id=group_id)
            return JsonResponse({"CaptainDismissGroupCheck": "success"})
        except Exception as e:
            return JsonResponse({"CaptainDismissGroupCheck": "failed"})


class CaptainGiveCaptain(View):
    def post(self, request):
        try:
            group_id = eval(request.body.decode()).get("group_id")
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            target_id = eval(request.body.decode()).get("t_sid")

            user = UserProfile.objects.filter(student_id=student_id, password=password)
            if user.count() == 0:
                return JsonResponse({"CaptainGiveCaptainCheck": "fail"})
            GroupOrg.objects.filter(group_name_id=group_id).update(captain_name_id=target_id)
            return JsonResponse({"CaptainGiveCaptainCheck": "success"})

        except Exception as e:
            return JsonResponse({"CaptainGiveCaptainCheck": "failed"})

