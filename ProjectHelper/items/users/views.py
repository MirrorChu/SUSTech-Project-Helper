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

from items.users.models import UserProfile
from items.operations.models import UserCourse
from items.courses.models import Course
from items.projects.models import Project


class LoginView(View):
    @method_decorator(ensure_csrf_cookie)
    # def get(self, request, *args, **kwargs):
    #     return render(request, "login.html")

    # 当用户按下登录按键时
    def post(self, request):
        print(request.body)

        student_id = eval(request.body.decode()).get("sid")
        password = eval(request.body.decode()).get("pswd")

        # 通过用户名和密码确认数据库中是否有和user对应的记录
        user = UserProfile.objects.filter(student_id=student_id, password=password)
        # 如果能查询到相应记录
        if user.count() == 0:
            return JsonResponse({"LoginCheck": "Login failed!"})
        # 如果未能查询到用户
        else:
            return JsonResponse({"LoginCheck": "Login success!"})


class ChangePasswordView(View):
    # 当用户按下登录按键时
    def post(self, request):
        print(request.body)

        student_id = eval(request.body.decode()).get("sid")
        old_password = eval(request.body.decode()).get("old_pswd")
        new_password = eval(request.body.decode()).get("new_pswd")

        # 通过用户名和密码确认数据库中是否有和user对应的记录
        user = UserProfile.objects.filter(student_id=student_id, password=old_password)
        # 如果能查询到相应记录
        if user.count() == 0:
            return JsonResponse({"ChangePasswordCheck": "Change failed!"})
        # 如果未能查询到用户
        else:
            user.update(password=new_password)
            return JsonResponse({"ChangePasswordCheck": "Change success!"})


class ShowPersonalDataView(View):
    # 当用户按下登录按键时
    def post(self, request):
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
            path = default_storage.save('tmp/'+file_name, ContentFile(file.read()))  # 根据名字存图(无类型)

            message = {'code': 200}
        return JsonResponse(message)
        # student_id = eval(request.body.decode()).get("sid")
        # password = eval(request.body.decode()).get("pswd")
        #
        # # 通过用户名和密码确认数据库中是否有和user对应的记录
        # user = UserProfile.objects.filter(student_id=student_id, password=password)
        # # 如果能查询到相应记录
        # if user.count() == 0:
        #     return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData failed!"})
        # # 如果未能查询到用户
        # else:
        #     x = UserProfile.objects.get(student_id=student_id, password=password)
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
        print(request.body)

        file_obj = request.FILES.get('file', None)

        path = eval(request.body.decode()).get("sid")
        old_password = eval(request.body.decode()).get("old_pswd")

        if not file_obj:
            return JsonResponse({"UploadFileCheck": "failed"})
        else:
            try:
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
        print(request.body)

        path = eval(request.body.decode()).get("path")
        file_name = eval(request.body.decode()).get("file_name")

        file_obj = open(path, 'rb')

        response = HttpResponse(file_obj)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment;filename="+file_name
        return response


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


class StudentGetAllProject(View):
    def post(self, request):
        student_id = eval(request.body.decode()).get("sid")
        password = eval(request.body.decode()).get("pswd")
        user = UserProfile.objects.filter(student_id=student_id, password=password)
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
    #返回{课程名：{项目ID:项目名，}，}



