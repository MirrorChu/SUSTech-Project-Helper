import os

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
import time
import json
import sys
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings

from items.groups.models import GroupOrg
from items.users.models import UserProfile
from items.operations.models import UserCourse, UserGroup, Tag, UserTag
from items.courses.models import Course
from items.projects.models import Project


class Login(View):
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
                return JsonResponse({"LoginCheck": "failed"})
            # 如果未能查询到用户
            else:
                for i in user:
                    if i.is_staff == 1:
                        return JsonResponse({"LoginCheck": "teacher"})
                    else:
                        return JsonResponse({"LoginCheck": "student"})
        except Exception as e:
            return JsonResponse({"LoginCheck": "failed"})


class ChangePassword(View):
    # 当用户按下登录按键时
    def post(self, request):
        try:
            print(request.body)

            student_id = eval(request.body.decode()).get("sid")
            old_password = eval(request.body.decode()).get("old")
            new_password = eval(request.body.decode()).get("new")

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.filter(username=student_id, password=old_password)
            # 如果能查询到相应记录
            if user.count() == 0:
                return JsonResponse({"ChangePasswordCheck": "failed"})
            # 如果未能查询到用户
            else:
                user.update(password=new_password)
                return JsonResponse({"ChangePasswordCheck": "success"})

        except Exception as e:
            return JsonResponse({"ChangePasswordCheck": "failed"})


class ShowPersonalData(View):
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

            for k in arr:
                file_name = k

            if file_name != '':
                file = request.FILES.get(file_name)
                path = default_storage.save('tmp/' + file_name + ".jpg",
                                            ContentFile(file.read()))  # 根据名字存图(无类型)

            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.filter(username=student_id, password=password)
            # 如果能查询到相应记录
            if user.count() == 0:
                return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData failed!"})
            # 如果未能查询到用户
            else:
                x = UserProfile.objects.get(username=student_id, password=password)

                return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData success!",
                                     "realname": x.real_name,
                                     "student_id": x.student_id,
                                     "gender": x.gender,
                                     "address": x.address,
                                     "email": x.email,
                                     "mobile": x.mobile,
                                     "image": None
                                     })

            # return JsonResponse({"ShowPersonalData": "success"})

        except Exception as e:
            print('exception')
            return JsonResponse({"ShowPersonalData": "failed"})


class ChangePersonalData(View):
    # {student_id:string, password:string, email: string, gender: string, mobile: string, address: string}
    def post(self, request):
        try:
            print(request.body)
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            email = eval(request.body.decode()).get("email")
            gender = eval(request.body.decode()).get("gender")
            mobile = eval(request.body.decode()).get("mobile")
            address = eval(request.body.decode()).get("address")

            query_set = UserProfile.objects.filter(username=student_id, password=password)
            if query_set.count() == 0:
                print('fail')
                return JsonResponse({"ChangePersonalData": "failed"})
            # 如果未能查询到用户
            else:
                print('success')
                query_set.update(email=email, gender=gender, mobile=mobile, address=address)
                return JsonResponse({"ChangePersonalData": "success"})

        except Exception as e:
            print('exception')
            return JsonResponse({"ChangePersonalData": "failed"})


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
        print('get')
        print(request.body)
        student_id = "11811002"
        password = "123"
        # get file

        file = open('LinuxLogo.jpg', 'wb+')
        print(file)
        path = default_storage.save('static\head_images' + 'LinuxLogo' + '.jpg',
                                    file)  # 根据名字存图(无类型)

        return JsonResponse({"ChangeHeadImage": "success"})

    def post(self, request):
        try:
            # file = request.FILES.get('file')
            # print(type(file))
            # path = default_storage.save('tmp/'+str(request.FILES.get('file')), ContentFile(file.read()))  # 根据名字存图
            # return JsonResponse({
            #                          "image": file
            #                          })
            print(request.POST)
            # print(request.POST)
            arr = request.FILES.keys()
            print(arr)
            file_name = ''
            for k in arr:
                file_name = k

            sid = ''
            pswd = ''
            for k in request.POST:
                print('k = ', k)
                if str(k) == 'sid':
                    sid = str(request.POST[k])
                else:
                    pswd = str(request.POST[k])

            print(sid, pswd)

            if file_name != '':
                file = request.FILES.get(file_name)
                path = default_storage.save('tmp/' + file_name + ".jpg",
                                            ContentFile(file.read()))  # 根据名字存图(无类型)
                print(path)

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.filter(username=sid, password=pswd)
            # 如果能查询到相应记录
            if user.count() == 0:
                print('avatar fail')
                return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData failed!"})
            # 如果未能查询到用户
            else:
                print('avatar success')
                x = UserProfile.objects.get(username=sid, password=pswd)

                return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData success!",
                                     # "realname": x.real_name,
                                     # "student_id": x.student_id,
                                     # "gender": x.gender,
                                     # "address": x.address,
                                     # "email": x.email,
                                     # "mobile": x.mobile,
                                     "image": None
                                     })

            # return JsonResponse({"ShowPersonalData": "success"})

        except Exception as e:
            print('avatar exception')
            return JsonResponse({"ShowPersonalData": "failed"})

    # def post(self, request):
    #         try:
    #             print(request.body)
    #             student_id = "11811002"
    #             password = "123"
    #             # get file
    #
    #             file = open('test.txt', 'wb+')
    #
    #             file_obj = request.FILES.get('file', None)
    #
    #             if not file_obj:
    #                 return JsonResponse({"ChangeHeadImage": "failed"})
    #             else:
    #                 print("file_obj", file_obj.name)
    #
    #                 # create path
    #                 file_path = os.path.join('static', 'head_images', student_id,
    #                                          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), file_obj.name)
    #
    #                 print("file_path", file_path)
    #
    #                 # store file
    #                 with open(file_path, 'wb+') as f:
    #                     for chunk in file_obj.chunks():
    #                         f.write(chunk)
    #
    #                 # update database path
    #                 UserProfile.objects.filter(username=student_id, password=password).update(image=file_path)
    #
    #                 return JsonResponse({"ChangeHeadImage": "success"})
    #
    #         except Exception as e:
    #             return JsonResponse({"ChangeHeadImage": "failed"})


class StudentGetsAllProjects(View):
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            # TODO: Delete this.
            # if student_id == '11810101' and password == '11810101':
            #     data = [{'course': 'CS301', 'project': '2.4G', 'start': '2020-12-01',
            #              'due': '2020-12-21'},
            #             {'course': 'CS303', 'project': 'IMP', 'start': '2020-11-15',
            #              'due': '2020-11-30'}]
            #     print(data)
            #     return JsonResponse({'courses': data})

            user = UserProfile.objects.filter(username=student_id, password=password)
            for i in user:
                course = UserCourse.objects.filter(user_name_id=i.id)
            courses = []
            name = ""
            for i in course:
                courseObject = Course.objects.filter(id=i.course_name_id)
                for j in courseObject:
                    name = j.name
                    projects = Project.objects.filter(course_id=j.id)
                for k in projects:
                    courses.append((k.id, name, k.name))
            return JsonResponse({"Data": courses})

        except Exception as e:
            return JsonResponse({"StudentGetsAllProjectsCheck": "failed"})
    # 返回{课程名：{项目ID:项目名，}，}


class StudentGetsSingleProjectInformation(View):
    def post(self, request):
        try:

            project_id = eval(request.body.decode()).get("project_id")
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            user = UserProfile.objects.filter(student_id=student_id, password=password)
            if user.count() == 0:
                return JsonResponse({"StudentGetsSingleGroupInformation": "failed"})
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

            return JsonResponse(
                {"project_name": project_name, "project_introduction": project_introduction,
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
                    groups[group_name] = {}
                    groups[group_name]["group_id"] = j.id

                    project_id = j.project_id
                    groups[group_name]["project_id"] = project_id
                    project = Project.objects.filter(id=project_id)
                    for k in project:
                        project_name = k.name
                        groups[group_name]["project_name"] = project_name
                        course_id = k.course_id
                        groups[group_name]["course_id"] = course_id
                        course = Course.objects.filter(id=course_id)
                        for l in course:
                            course_name = l.name
                            groups[group_name]["course_name"] = course_name
            return JsonResponse({"Data": groups})
        except Exception as e:
            return JsonResponse({"StudentGetsAllGroups": "failed"})

    # 返回{队伍名:{队伍id,项目id,项目名,课程id,课程名},}


class StudentGetsSingleGroupInformation(View):
    def post(self, request):
        try:
            group_id = eval(request.body.decode()).get("group_id")
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            query_set = GroupOrg.objects.filter(id=group_id)
            user = UserProfile.objects.filter(student_id=student_id, password=password)
            if user.count() == 0:
                return JsonResponse({"StudentGetsSingleGroupInformation": "failed"})

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

                query_set3 = Project.objects.filter(id=project_id)
                for j in query_set3:
                    project_name = j.name
                    course_id = j.course_id
                    query_set1 = Course.objects.filter(id=project_id)
                    for k in query_set1:
                        course_name = k.name

                query_set3 = UserProfile.objects.filter(id=captain_id)
                for j in query_set3:
                    captain_name = j.username

                query_set3 = UserGroup.objects.filter(id=group_id)
                for j in query_set3:
                    user_id = j.user_name_id
                    query_set1 = UserProfile.objects.filter(id=user_id)
                    for k in query_set1:
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


class StudentGetsGroupInformationInProject(View):
    def post(self, request):
        try:
            project_id = eval(request.body.decode()).get("project_id")
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            user = UserProfile.objects.filter(student_id=student_id, password=password)

            if user.count() == 0:
                return JsonResponse({"StudentGetsGroupInformationInProject": "failed"})

            for i in user:
                student_id = i.id

            group_id = 0

            group = UserGroup.objects.filter(user_name_id=student_id)

            if group.count() == 0:
                print('count', group)
                return JsonResponse(
                    {"project_id": project_id, "StudentGetsGroupInformationInProject": "no group"})
            for i in group:
                project = GroupOrg.objects.filter(id=i.group_name_id)
                for j in project:
                    if j.project_id == int(project_id):
                        group_id = j.id
            if group_id == 0:
                return JsonResponse(
                    {"project_id": project_id, "StudentGetsGroupInformationInProject": "no group"})
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

                query_set3 = Project.objects.filter(id=project_id)
                for j in query_set3:
                    project_name = j.name
                    course_id = j.course_id
                    query_set1 = Course.objects.filter(id=project_id)
                    for k in query_set1:
                        course_name = k.name

                query_set3 = UserProfile.objects.filter(id=captain_id)
                for j in query_set3:
                    captain_name = j.username

                query_set3 = UserGroup.objects.filter(id=group_id)
                for j in query_set3:
                    user_id = j.user_name_id
                    query_set1 = UserProfile.objects.filter(id=user_id)
                    for k in query_set1:
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
            return JsonResponse({"StudentGetsGroupInformationInProject": "failed"})
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
            query_set = GroupOrg.objects.filter(group_name=group_name, captain_name_id=captain_id,
                                                project_id=project_id)
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
            group_introduction = eval(request.body.decode()).get("group_introduction")

            GroupOrg.objects.filter(id=group_id).update(detail=group_introduction)

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
            group_name = eval(request.body.decode()).get("group_name")

            GroupOrg.objects.filter(id=group_id).update(group_name=group_name)

            return JsonResponse({"EditsGroupNameCheck": "success"})

        except Exception as e:
            return JsonResponse({"EditsGroupNameCheck": "failed"})


class GroupMemberValidation(View):
    def post(self, request):
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


class StudentGetAllGroupsInProject(View):
    def post(self, request):
        try:
            project_id = eval(request.body.decode()).get("project_id")
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            user = UserProfile.objects.filter(student_id=student_id, password=password)
            if user.count() == 0:
                return JsonResponse({"StudentGetAllGroupsInProjectCheck": "fail"})
            groups = GroupOrg.objects.filter(project_id=project_id)
            project = Project.objects.filter(id=project_id)
            group = {}
            for i in project:
                group["group_size"] = i.group_size
            for i in groups:
                group[i.id] = {}
                group[i.id]["group_name"] = i.group_name
                group[i.id]["member"] = i.member
                group[i.id]["captain_id"] = i.captain_name_id
                captain = UserProfile.objects.filter(student_id=i.captain_name_id)
                for j in captain:
                    group[i.id]["captain_name"] = j.username

            return JsonResponse({"Data": group, "StudentGetAllGroupsInProjectCheck": "success"})
        except Exception as e:
            return JsonResponse({"StudentGetAllGroupsInProjectCheck": "failed"})


class StudentGetAllStudentsInProject(View):
    def post(self, request):
        try:
            project_id = eval(request.body.decode()).get("project_id")
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            user = UserProfile.objects.filter(student_id=student_id, password=password)
            if user.count() == 0:
                return JsonResponse({"StudentGetAllStudentsInProjectCheck": "fail"})
            groups = GroupOrg.objects.filter(project_id=project_id)
            project = Project.objects.filter(id=project_id)
            group = {}
            groupList = []
            for i in project:
                group["group_size"] = i.group_size
                group["course_id"] = i.course_id
            for i in groups:
                group[i.id] = {}
                groupList.append(i.id)
                group[i.id]["group_name"] = i.group_name
                group[i.id]["member"] = i.member
            student = {}
            students = UserCourse.objects.filter(course_name_id=group["course_id"])
            for i in students:
                studentProfile = UserProfile.objects.filter(id=i.user_name_id)
                for j in studentProfile:
                    student[j.id] = {}
                    student[j.id]["username"] = j.username
                    student[j.id]["has_group"] = False
                    for k in groupList:
                        judge = UserGroup.objects.filter(group_name_id=k, user_name_id=j.id)
                        if judge.count() != 0:
                            student[j.id]["has_group"] = True
                            student[j.id]["group_id"] = k
                            student[j.id]["group_name"] = group[k]["group_name"]
                            student[j.id]["member"] = group[k]["member"]
                            break

            return JsonResponse({"Data": student, "StudentGetAllStudentsInProjectCheck": "success"})
        except Exception as e:
            return JsonResponse({"StudentGetAllStudentsInProjectCheck": "failed"})


class Image(View):
    def post(self, request):
        print(request.body)

        file_obj = request.FILES.get('image')

        print("file_obj", file_obj.name)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        file_path = os.path.join(BASE_DIR, 'static', 'head_images', file_obj.name)
        print("file_path", file_path)
        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        message = {}
        message['code'] = 200

        return JsonResponse(message)

    def post(self, request):
        try:
            # file = request.FILES.get('file')
            # print(type(file))
            # path = default_storage.save('tmp/'+str(request.FILES.get('file')), ContentFile(file.read()))  # 根据名字存图
            # return JsonResponse({
            #                          "image": file
            #                          })
            print(request.POST)
            arr = request.FILES.keys()
            print(arr)
            file_name = ''
            for k in arr:
                file_name = k

            sid = ''
            pswd = ''
            for k in request.POST:
                if str(k) == 'sid':
                    sid = str(request.POST[k])
                else:
                    pswd = str(request.POST[k])

            print(sid, pswd)

            if file_name != '':
                file = request.FILES.get(file_name)
                path = default_storage.save('tmp/' + file_name + ".jpg",
                                            ContentFile(file.read()))  # 根据名字存图(无类型)
                print(path)

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.filter(username=sid, password=pswd)
            # 如果能查询到相应记录
            if user.count() == 0:
                print('avatar fail')
                return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData failed!"})
            # 如果未能查询到用户
            else:
                print('avatar success')
                x = UserProfile.objects.get(username=sid, password=pswd)

                # TODO: Fix image.
                # file_path = x.image
                # file = open(file_path, "rb")

                return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData success!",
                                     # "realname": x.real_name,
                                     # "student_id": x.student_id,
                                     # "gender": x.gender,
                                     # "address": x.address,
                                     # "email": x.email,
                                     # "mobile": x.mobile,
                                     "image": None
                                     })

            # return JsonResponse({"ShowPersonalData": "success"})

        except Exception as e:
            print('avatar exception')
            return JsonResponse({"ShowPersonalData": "failed"})


class ChangeHeadImage(View):
    def post(self, request):
        try:
            print(request.POST)
            arr = request.FILES.keys()
            print(arr)
            file_name = ''
            for k in arr:
                file_name = k

            sid = ''
            pswd = ''
            path = " "

            for k in request.POST:
                if str(k) == 'sid':
                    sid = str(request.POST[k])
                else:
                    pswd = str(request.POST[k])

            print(sid, pswd)

            if file_name != '':
                file = request.FILES.get(file_name)
                path = default_storage.save('head_images/' + sid + "/" +
                                            time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
                                            + "/" + file_name + ".jpg",
                                            ContentFile(file.read()))  # 根据名字存图(无类型)
                print(path)

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.filter(username=sid, password=pswd)
            # 如果能查询到相应记录
            if user.count() == 0:
                print('avatar fail')
                return JsonResponse({"ChangeHeadImage": "failed"})
            # 如果未能查询到用户
            else:
                print('avatar success')
                UserProfile.objects.filter(username=sid, password=pswd).update(image=path)

                return JsonResponse({"ChangeHeadImage": "success"})

        except Exception as e:
            print('avatar exception')
            return JsonResponse({"ChangeHeadImage": "failed"})


class ShowHeadImage(View):
    # return path
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            head_image_path = ""

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            query_set = UserProfile.objects.filter(username=student_id, password=password)
            if query_set.count() == 0:
                return JsonResponse({"ShowHeadImage": "failed"})
            else:
                for i in query_set:
                    head_image_path = i.image
                return JsonResponse({"ShowHeadImage": head_image_path})

        except Exception as e:
            return JsonResponse({"ShowHeadImage": "failed"})


class TestAPI(View):
    def post(self, request):
        print(request.body)
        return JsonResponse({"message": "get it"})


class AddTag(View):
    # return path
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            tag_id = eval(request.body.decode()).get("tag_id")

            user_id = 0

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            query_set = UserProfile.objects.filter(username=student_id, password=password)
            if query_set.count() == 0:
                return JsonResponse({"AddTag": "failed"})
            else:
                for i in query_set:
                    user_id = i.id

            query_set = Tag.objects.filter(id=tag_id)
            if query_set.count() == 0:
                return JsonResponse({"AddTag": "failed"})
            else:
                for i in query_set:
                    tag_id = i.id

            # 验证是否有重复的记录
            query_set = UserTag.objects.filter(user_name_id=user_id, tag_id=tag_id)
            if query_set.count() != 0:
                return JsonResponse({"AddTag": "failed"})

            UserTag.objects.create(user_name_id=user_id, tag_id=tag_id)

            return JsonResponse({"AddTag": "success"})

        except Exception as e:
            return JsonResponse({"AddTag": "failed"})


class ShowTag(View):
    # return path
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            tag_id = eval(request.body.decode()).get("tag_id")

            user_id = 0

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            query_set = UserProfile.objects.filter(username=student_id, password=password)
            if query_set.count() == 0:
                return JsonResponse({"ShowTag": "failed"})
            else:
                for i in query_set:
                    user_id = i.id

            query_set = Tag.objects.filter(id=tag_id)
            if query_set.count() == 0:
                return JsonResponse({"ShowTag": "failed"})
            else:
                for i in query_set:
                    tag_id = i.id

            UserTag.objects.filter(user_name_id=user_id, tag_id=tag_id).update(visibility=1)

            return JsonResponse({"ShowTag": "success"})

        except Exception as e:
            return JsonResponse({"ShowTag": "failed"})


class UnshowTag(View):
    # return path
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            tag_id = eval(request.body.decode()).get("tag_id")

            user_id = 0

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            query_set = UserProfile.objects.filter(username=student_id, password=password)
            if query_set.count() == 0:
                return JsonResponse({"UnshowTag": "failed"})
            else:
                for i in query_set:
                    user_id = i.id

            query_set = Tag.objects.filter(id=tag_id)
            if query_set.count() == 0:
                return JsonResponse({"UnshowTag": "failed"})
            else:
                for i in query_set:
                    tag_id = i.id

            UserTag.objects.filter(user_name_id=user_id, tag_id=tag_id).update(visibility=0)

            return JsonResponse({"UnshowTag": "success"})

        except Exception as e:
            return JsonResponse({"UnshowTag": "failed"})


class GetTagVisibility(View):
    # return path
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            tag_id = eval(request.body.decode()).get("tag_id")

            user_id = 0

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            query_set = UserProfile.objects.filter(username=student_id, password=password)
            if query_set.count() == 0:
                return JsonResponse({"GetTagVisibility": "failed"})
            else:
                for i in query_set:
                    user_id = i.id

            query_set = Tag.objects.filter(id=tag_id)
            if query_set.count() == 0:
                return JsonResponse({"GetTagVisibility": "failed"})
            else:
                for i in query_set:
                    tag_id = i.id

            query_set = UserTag.objects.filter(user_name_id=user_id, tag_id=tag_id)
            if query_set.count() == 0:
                return JsonResponse({"GetTagVisibility": "failed"})
            else:
                for i in query_set:
                    visibility = i.visibility

            return JsonResponse({"GetTagVisibility": visibility})

        except Exception as e:
            return JsonResponse({"GetTagVisibility": "failed"})


class StudentGetsAllTags(View):
    # return path
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            user_id = 0
            tag_id = 0
            visibility = 1
            tags = {}

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            query_set = UserProfile.objects.filter(username=student_id, password=password)
            if query_set.count() == 0:
                return JsonResponse({"StudentGetsAllTags": "failed"})
            else:
                for i in query_set:
                    user_id = i.id

            query_set = UserTag.objects.filter(user_name_id=user_id)
            if query_set.count() == 0:
                return JsonResponse({"StudentGetsAllTags": "failed"})
            else:
                for i in query_set:
                    tag_id = i.tag_id
                    visibility = i.visibility

                query_set2 = Tag.objects.filter(id=tag_id)
                if query_set2.count() == 0:
                    return JsonResponse({"StudentGetsAllTags": "failed"})
                else:
                    for j in query_set:
                        tags[tag_id] = {"tag_name": str(j.tag), "visibility": visibility}

            return JsonResponse({"Data": tags})

        except Exception as e:
            return JsonResponse({"StudentGetsAllTags": "failed"})


class StudentGetValidGroupInProject(View):
    def post(self, request):
        try:

            project_id = eval(request.body.decode()).get("project_id")
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            user = UserProfile.objects.filter(student_id=student_id, password=password)
            if user.count() == 0:
                return JsonResponse({"StudentGetValidGroupInProject": "fail"})
            groups = GroupOrg.objects.filter(project_id=int(project_id))
            project = Project.objects.filter(id=int(project_id))
            group = {}
            for i in project:
                group["group_size"] = i.group_size
            for i in groups:
                group[i.id] = {}
                group[i.id]["group_name"] = i.group_name
                group[i.id]["member"] = i.member
                group[i.id]["captain_id"] = i.captain_name_id
                captain = UserProfile.objects.filter(student_id=i.captain_name_id)
                for j in captain:
                    group[i.id]["captain_name"] = j.username
                userGroup = UserGroup.objects.filter(group_name_id=i.id, user_name_id=student_id)
                if userGroup.count() == 1:
                    return JsonResponse(
                        {"Data": None, "StudentGetValidGroupInProjectCheck": "already has group"})
                if i.member == group["group_size"]:
                    group.pop(i.id)
            if len(group) == 0:
                return JsonResponse(
                    {"Data": None, "StudentGetValidGroupInProjectCheck": "no group to attend"})

            return JsonResponse({"Data": group, "StudentGetValidGroupInProjectCheck": "success"})
        except Exception as e:
            return JsonResponse({"StudentGetValidGroupInProjectCheck": "failed"})


class StudentGetProject(View):
    def post(self, request):
        try:

            # # TODO: Delete this.
            # sid = eval(request.body.decode()).get("sid")
            # pswd = eval(request.body.decode()).get("pswd")
            # course = eval(request.body.decode()).get("course")
            # project = eval(request.body.decode()).get("project")
            # if sid == '11810101' and pswd == '11810101' and course == 'CS303' and project == 'IMP':x
            #     data = {'description': 'This is a demo description',
            #             'inspectors': ['inspector1', 'inspector2'],
            #             'milestone': {'event1': 'datetime1', 'event2': 'datetime2'},
            #             'attachment': 'path to the attachment',
            #             'groupInfo': None}
            #     return JsonResponse({'projectDetail': data})

            project_id = eval(request.body.decode()).get("project_id")
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            user = UserProfile.objects.filter(student_id=student_id, password=password)
            if user.count() == 0:
                return JsonResponse({"StudentGetProjectCheck": "fail"})
            groups = GroupOrg.objects.filter(project_id=int(project_id))
            project = Project.objects.filter(id=int(project_id))
            group = {}
            for i in project:
                group["group_size"] = i.group_size
            for i in groups:
                group[i.id] = {}
                group[i.id]["group_name"] = i.group_name
                group[i.id]["member"] = i.member
                group[i.id]["captain_id"] = i.captain_name_id
                captain = UserProfile.objects.filter(student_id=i.captain_name_id)
                for j in captain:
                    group[i.id]["captain_name"] = j.username
                userGroup = UserGroup.objects.filter(group_name_id=i.id, user_name_id=student_id)
                if userGroup.count() == 1:
                    query_set = GroupOrg.objects.filter(id=i.id)

                    group_name = ""
                    group_detail = ""
                    project_name = ""
                    course_name = ""
                    captain_name = ""
                    captain_id = 0
                    project_id = 0
                    course_id = 0
                    members = []

                    for j in query_set:
                        group_name = j.group_name
                        group_detail = j.detail
                        captain_id = j.captain_name_id
                        project_id = j.project_id

                        query_set = Project.objects.filter(id=project_id)
                        for k in query_set:
                            project_name = k.name
                            course_id = k.course_id
                            query_set = Course.objects.filter(id=project_id)
                            for k in query_set:
                                course_name = k.name

                        query_set = UserProfile.objects.filter(id=captain_id)
                        for k in query_set:
                            captain_name = k.username

                        query_set = UserGroup.objects.filter(id=i.id)
                        for k in query_set:
                            user_id = k.user_name_id
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
                if i.member == group["group_size"]:
                    group.pop(i.id)

            return JsonResponse({"Data": group, "StudentGetProjectCheck": "success"})
        except Exception as e:
            return JsonResponse({"StudentGetProjectCheck": "failed"})


class SendMailToInvite(View):
    def post(self, request):
        try:
            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")
            tag_id = eval(request.body.decode()).get("t_sid")
            group_id = eval(request.body.decode()).get("group_id")

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            query_set = UserProfile.objects.filter(username=student_id, password=password)
            if query_set.count() == 0:
                return JsonResponse({"SendMailToInvite": "failed"})
            query_set = UserProfile.objects.filter(username=tag_id)
            if query_set.count() == 0:
                return JsonResponse({"SendMailToInvite": "failed"})
            else:
                for i in query_set:
                    email = i.email
            subject = '来自自强学堂的问候'
            text_content = '这是一封重要的邮件.'
            html_content = '''<p>这是一封<strong>重要的</strong>邮件.</p>'''
            msg = EmailMultiAlternatives(subject, text_content,
                                         student_id + '<11812710@mail.sustech.edu.cn>', [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return JsonResponse({"SendMailToInvite": "success"})

        except Exception as e:
            return JsonResponse({"SendMailToInvite": "failed"})


class MailUrl(View):
    def get(self, request):
        # sender = request.GET.get('s')
        reciver = request.GET.get('r')
        # type = request.GET.get('t')
        # password = request.GET.get('c')
        # send_mail('Subject here', 'Here is the message.', 'me'+'<11812710@mail.sustech.edu.cn>',
        #           ['11811002@mail.sustech.edu.cn'], fail_silently=False)
        subject = '来自自强学堂的问候'
        text_content = '这是一封重要的邮件.'
        html_content = '''<p>这是一封<strong>重要的</strong>邮件.</p>'''
        msg = EmailMultiAlternatives(subject, text_content, 'me' + '<11812710@mail.sustech.edu.cn>',
                                     [reciver])
        msg.attach_alternative(html_content, "text/html")
        msg.send()  # http://127.0.0.1:8000/mailurl/?r=目标邮箱 测试用例
        return HttpResponse("success")


# class Test(View):
#     def post(self, request):
#         print(request)
#         print(request.POST)
#         # print(request.body)
#         student_id = "admin"
#         password = "123"
#         # get file
#         user = UserProfile.objects.filter(username=student_id, password=password)
#         if user.count() == 1:
#             return HttpResponse("yes")
#
#         return HttpResponse("no")
#
#     def get(self, request):
#         p1 = request.GET.get('p1')
#         p2 = request.GET.get('p2')
#         return HttpResponse("p1 = " + p1 + "; p2 = " + p2)
