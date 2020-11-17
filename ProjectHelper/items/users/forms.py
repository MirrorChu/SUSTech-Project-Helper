from django import forms


# 表单验证，即对用户提交数据的验证
class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=8)
    password = forms.CharField(required=True, min_length=6)
    # required = True 代表相应字段是必填的
    # 用户名的长度至少要为8，密码的长度至少要为6，否则没必要查询数据库

