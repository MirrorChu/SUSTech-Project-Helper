from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from items.users.forms import LoginForm


class LoginView(View):
    @method_decorator(ensure_csrf_cookie)
    # 当网址login/被访问时，返回登录页面
    def get(self, request, *args, **kwargs):
        return render(request, "login.html")

    # 当用户按下登录按键时
    def post(self, request):
        # 表单验证，即对用户提交数据的验证
        print(type(request))
        print(request)
        print(type(request.body))
        print(request.body)

        student_id = eval(request.body.decode()).get("sid")
        password = eval(request.body.decode()).get("pswd")

        # 通过用户名和密码确认数据库中是否有和user对应的记录
        user = authenticate(student_id=student_id, password=password)
        # password是未加密的，而数据库中存储的是加密后的密码。因此要先将password加密再查询。
        # 如果能查询到相应记录
        if user is not None:
            return JsonResponse({"message": "Login success!"})
        # 如果未能查询到用户
        else:
            return JsonResponse({"message": "Login failed!"})
        # 若数据库检验的结果是登录失败，则停留在登录页面



