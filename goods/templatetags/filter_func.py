from django import template

register = template.Library()


@register.filter()
def filter_get(goods, param):
    filter_goods = goods.filter(category=param).all()
    return filter_goods


register.filter('filter_get', filter_get)
