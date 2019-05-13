from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from cart.models import ShoppingCart
from goods.models import Goods


def cart(request):
    if request.method == 'GET':
        goods = Goods.objects.all()
        user_id = request.session.get('user_id')
        # 未登录时，从session取数据
        if not user_id:
            goods_sessions = request.session.get('goods')
            response = {'goods_sessions': goods_sessions, 'goods': goods}
            return render(request, 'cart.html', response)
        # 登录时从数据库取数据
        cart_goods = ShoppingCart.objects.all()
        cgood_list = []
        for good in cart_goods:
            goods_id = good.goods_id
            num = good.nums
            is_select = good.is_select
            cgood = [goods_id, num, is_select, user_id]
            cgood_list.append(cgood)
        response = {'goods_sessions': cgood_list, 'goods': goods}
        return render(request, 'cart.html', response)


def add_cart(request, id):
    res = HttpResponseRedirect(reverse('goods:detail', args=(id,)))
    if request.method == 'GET':
        return res
    if request.method == 'POST':
        goods_id = id
        num = request.POST.get('num', '1')
        is_select = '0'
        goods = [goods_id, num, is_select]
        user_id = request.session.get('user_id')
        goods_init = request.session.get('goods')
        # 没有登陆时
        if not user_id:
            # 购物车有东西时
            if goods_init:
                for good in goods_init:
                    # 购物车中存在此商品时
                    if id == good[0]:
                        good[1] = str(int(good[1]) + int(goods[1]))
                        request.session['goods'] = goods_init
                        return res
                # 购物车中不存在此商品时
                goods_init.append(goods)
                request.session['goods'] = goods_init
                return res
            # 购物车没东西时
            request.session['goods'] = [goods]
            return res
        # 登录时
        cgoods = ShoppingCart.objects.all()
        goods_list = []
        for cgood in cgoods:
            goods_id = cgood.goods_id
            num = cgood.nums
            is_select = cgood.is_select
            allgoods = [goods_id, num, is_select, user_id]
            goods_list.append(allgoods)
        for good in goods_list:
            # 购物车中存在此商品时
            if goods[0] == good[0]:
                good[1] = str(int(good[1]) + int(goods[1]))
                ShoppingCart.objects.filter(goods_id=good[0]).update(nums=good[1])
                return res
        # 购物车中不存在此商品时
        sgood = ShoppingCart()
        sgood.goods_id = goods[0]
        sgood.nums = goods[1]
        sgood.is_select = goods[2]
        sgood.user_id = user_id
        sgood.save()
        return res


def add_goods(request, id):
    if request.is_ajax():
        user_id = request.session.get('user_id')
        goods = request.session.get('goods')
        if not user_id:
            for good in goods:
                if id == good[0]:
                    good[1] = str(int(good[1]) + 1)
                    request.session['goods'] = goods
                    return JsonResponse({'data': good[1]})
        cart_goods = ShoppingCart.objects.all()
        for cgood in cart_goods:
            if id == cgood.goods_id:
                num = ShoppingCart.objects.filter(goods_id=id).first().nums + 1
                ShoppingCart.objects.filter(goods_id=id).update(nums=num)
                return JsonResponse({'data': str(num)})


def minus_goods(request, id):
    if request.is_ajax():
        user_id = request.session.get('user_id')
        goods = request.session.get('goods')
        if not user_id:
            for good in goods:
                if id == good[0]:
                    if int(good[1]) == 1:
                        goods.remove(good)
                        request.session['goods'] = goods
                        return JsonResponse({'data': ''})
                    good[1] = str(int(good[1]) - 1)
                    request.session['goods'] = goods
                    return JsonResponse({'data': good[1]})
        cart_goods = ShoppingCart.objects.all()
        for cgood in cart_goods:
            if id == cgood.goods_id:
                if cgood.nums == 1:
                    cgood.delete()
                    return JsonResponse({'data': ''})
                num = ShoppingCart.objects.filter(goods_id=id).first().nums - 1
                ShoppingCart.objects.filter(goods_id=id).update(nums=num)
                return JsonResponse({'data': str(num)})


def del_goods(request, id):
    if request.is_ajax():
        user_id = request.session.get('user_id')
        goods = request.session.get('goods')
        if not user_id:
            for good in goods:
                if id == good[0]:
                    goods.remove(good)
                    request.session['goods'] = goods
                    return JsonResponse({'data': ''})
        cart_goods = ShoppingCart.objects.all()
        for cgood in cart_goods:
            if id == cgood.goods_id:
                cgood.delete()
                return JsonResponse({'data': ''})
