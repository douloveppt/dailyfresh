from django import forms
from django.contrib.auth.hashers import check_password

from user.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(
        required=True, max_length=20, min_length=5, error_messages={
            'required': '请填写用户名',
            'max_length': '用户名最大长度为20个字符',
            'min_length': '用户名最小长度为5个字符'
        })
    pwd1 = forms.CharField(
        required=True, max_length=20, min_length=8, error_messages={
            'required': '请填写密码',
            'max_length': '密码最大长度为20个字符',
            'min_length': '密码最小长度为8个字符'
        })
    pwd2 = forms.CharField(
        required=True, max_length=20, min_length=8, error_messages={
            'required': '请填写密码',
            'max_length': '密码最大长度为20个字符',
            'min_length': '密码最小长度为8个字符'
        })
    email = forms.EmailField(
        required=True, max_length=50, min_length=5, error_messages={
            'required': '请填写邮箱',
            'max_length': '邮箱最大长度为50个字符',
            'min_length': '邮箱最小长度为5个字符'
        })

    def clean(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': '该账号已经注册过了'})
        pwd1 = self.cleaned_data.get('pwd1')
        pwd2 = self.cleaned_data.get('pwd2')
        if pwd1 != pwd2:
            raise forms.ValidationError({'pwd2': '两次密码不一致'})
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True, max_length=20, min_length=5, error_messages={
            'required': '请填写用户名',
            'max_length': '用户名最大长度为20个字符',
            'min_length': '用户名最小长度为5个字符'
        })
    password = forms.CharField(
        required=True, max_length=20, min_length=8, error_messages={
            'required': '请填写密码',
            'max_length': '密码最大长度为20个字符',
            'min_length': '密码最小长度为8个字符'
        })

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': '该账号不存在'})
        password2 = User.objects.filter(username=username).first().password
        if not check_password(password, password2):
            raise forms.ValidationError({'password': '密码不正确'})
        return self.cleaned_data
