from django.shortcuts import render

from cart.models import ShoppingCart
from goods.models import Goods
from user.models import UserAddress


def order(request):
    if request.method == 'GET':
        # 获取地址列表
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
        # 获取购物车
        user_id = request.session.get('user_id')
        cart_goods = ShoppingCart.objects.all()
        goods_list = []
        for cgood in cart_goods:
            good_id = cgood.goods_id
            num = str(cgood.nums)
            is_select = cgood.is_select
            good = [good_id, num, is_select, user_id]
            goods_list.append(good)
        goods = Goods.objects.all()
        response = {'goods_sessions': goods_list, 'goods': goods, 'add_list': add_list}
        return render(request, 'place_order.html', response)
