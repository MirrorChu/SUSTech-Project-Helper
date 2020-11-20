import os

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from items.users.models import UserProfile
from ProjectHelper.settings import BASE_DIR


class Login(View):
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


class ChangePassword(View):
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


class ShowPersonalData(View):
    # 当用户按下登录按键时
    def get(self, request):
        print(request.body)

        student_id = eval(request.body.decode()).get("sid")
        password = eval(request.body.decode()).get("pswd")

        # 通过用户名和密码确认数据库中是否有和user对应的记录
        user = UserProfile.objects.filter(student_id=student_id, password=password)
        # 如果能查询到相应记录
        if user.count() == 0:
            return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData failed!"})
        # 如果未能查询到用户
        else:
            x = UserProfile.objects.get(student_id=student_id, password=password)
            file_path = x.image
            file = open(file_path, "rb")

            return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData success!",
                                 "realname": x.real_name,
                                 "student_id": x.student_id,
                                 "gender": x.gender,
                                 "address": x.address,
                                 "email": x.email,
                                 "mobile": x.mobile,
                                 "image": file
                                 })


class Image(View):

    def post(self, request):
        print(request.body)

        file_obj = request.FILES.get('image')

        print("file_obj", file_obj.name)

        file_path = os.path.join(BASE_DIR, 'static', 'head_images', file_obj.name)

        print("file_path", file_path)

        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        message = {}
        message['code'] = 200

        return JsonResponse(message)


class TestAPI(View):
   def post(self, request):
       print(request.body)
       return JsonResponse({"message": "get it"})


