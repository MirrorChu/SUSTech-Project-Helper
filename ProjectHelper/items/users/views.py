from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
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



        # login_form = LoginForm(request.POST)
        # if login_form.is_valid():
        #     # 分别获取表单中的用户名和密码
        #     username = login_form.cleaned_data["username"]
        #     password = login_form.cleaned_data["password"]
        #     # 通过用户名和密码确认数据库中是否有和user对应的记录
        #     user = authenticate(username=username, password=password)
        #     # password是未加密的，而数据库中存储的是加密后的密码。因此要先将password加密再查询。
        #
        #     # 如果能查询到相应记录
        #     if user is not None:
        #         # 用django自带的函数登录
        #         login(request, user)
        #         return HttpResponseRedirect(reverse("index"))
        #         # 若用render函数，则返回后的网址还是/login
        #         # 若用HttpResponseRedirect函数，则返回后的网址会自动变化
        #         # 登录成功后还是返回首页
        #     # 如果未能查询到用户
        #     else:
        #         return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
        #     # 若数据库检验的结果是登录失败，则停留在登录页面
        # else:
        #     return render(request, "login.html", {"login_form": login_form})
        #     # 若表单检验的结果是登录失败，则停留在登录页面



