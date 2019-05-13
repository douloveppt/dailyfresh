from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from user.form import RegisterForm, LoginForm
from user.models import User, Token, UserAddress
from utils.functions import get_token


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('pwd2')
            password2 = make_password(password)
            User.objects.create(username=username, password=password2)
            return HttpResponseRedirect(reverse('user:login'))
        errors = form.errors
        return render(request, 'register.html', {'errors': errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            res = HttpResponseRedirect(reverse('goods:index'))
            request.session['user_id'] = user.id
            request.session.set_expiry(86400)
            return res
        errors = form.errors
        return render(request, 'login.html', {'errors': errors})


def logout(request):
    if request.method == 'GET':
        request.session.flush()
        return HttpResponseRedirect(reverse('goods:index'))


def is_login(request):
    if request.is_ajax():
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'username': ''})
        username = User.objects.filter(id=user_id).first().username
        response = JsonResponse({'username': username})
        return response


def user_center_info(request):
    if request.method == 'GET':
        return render(request, 'user_center_info.html')


def user_center_order(request):
    if request.method == 'GET':
        return render(request, 'user_center_order.html')


def user_center_site(request):
    if request.method == 'GET':
        uaddress = UserAddress.objects.all()
        add_list = []
        for add in uaddress:
            receiver = add.signer_name
            province = add.province
            city = add.city
            district = add.district
            address = add.address
            postcode = add.signer_postcode
            phone = add.signer_mobile
            a_list = [province, city, district, address, receiver, phone]
            add_list.append(a_list)
        return render(request, 'user_center_site.html', {'add_lsit': add_list})


def add_site(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        uaddress = UserAddress()
        # 获取表单数据
        receiver = request.POST.get('receiver')
        province = request.POST.get('province')
        city = request.POST.get('city')
        district = request.POST.get('district')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        # 存到数据库
        uaddress.user_id = user_id
        uaddress.signer_name = receiver
        uaddress.province = province
        uaddress.city = city
        uaddress.district = district
        uaddress.address = address
        uaddress.signer_postcode = postcode
        uaddress.signer_mobile = phone
        uaddress.save()
        return HttpResponseRedirect(reverse('user:user_center_site'))
