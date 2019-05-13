import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from goods.models import Goods
from user.models import User


# 校验登录状态
class UserLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path
        no_need_check_path_list = ['/user/register/', '/user/login/', '/goods/index/', '/media/(.*)/', '/static/(.*)/',
                                   '/goods/detail/(\d+)/', '/goods/goods_list/(\d+)/', '/cart/cart/',
                                   '/cart/add_cart/(\d+)/', '/cart/add_goods/(\d+)/', '/cart/minus_goods/(\d+)/',
                                   '/cart/del_goods/(\d+)/', '/goods/search/', '/user/is_login/',
                                   ]
        for no_path in no_need_check_path_list:
            if re.match(no_path, path):
                return None
        user_id = request.session.get('user_id')
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))
        user = User.objects.get(id=user_id)
        request.user = user


# 未登录到登录时购物车的数据同步
class SessionSyncDatabase(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        session_goods = request.session.get('goods')
        database_goods = ShoppingCart.objects.all()
        # 没登录时
        if not user_id:
            return None
        # 登录时
        # session有东西
        if session_goods:
            # 数据库没东西时
            if not database_goods:
                for sgood in session_goods:
                    scart = ShoppingCart()
                    good = sgood[0]
                    num = sgood[1]
                    is_select = sgood[2]
                    scart.user = User.objects.filter(pk=user_id).first()
                    scart.goods = Goods.objects.filter(pk=good).first()
                    scart.nums = num
                    scart.is_select = is_select
                    scart.save()
                del request.session['goods']
                return None
            # 数据库有东西时
            for sgood in session_goods:
                break_flag = False
                for dgood in database_goods:
                    good = dgood.goods_id
                    # 有重复商品时
                    if sgood[0] == good:
                        num = str(dgood.nums + int(sgood[1]))
                        ShoppingCart.objects.filter(goods_id=good).update(nums=num)
                        break_flag = True
                        break
                # 不重复时
                if break_flag == False:
                    scart = ShoppingCart()
                    good = sgood[0]
                    num = sgood[1]
                    is_select = sgood[2]
                    scart.user = User.objects.filter(pk=user_id).first()
                    scart.goods = Goods.objects.filter(pk=good).first()
                    scart.nums = num
                    scart.is_select = is_select
                    scart.save()

            del request.session['goods']
            return None

        # session没东西时
        return None
