from django import template

register = template.Library()


@register.filter()
def goods_filter(goods, param):
    filter_goods = goods.filter(pk=param).first()
    image = filter_goods.goods_front_image
    name = filter_goods.name
    price = filter_goods.shop_price
    res = [image, name, price]
    return res


register.filter('filter_get', goods_filter)
