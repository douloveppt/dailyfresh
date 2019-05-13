from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from goods.models import GoodsCategory, Goods


def index(request):
    if request.method == 'GET':
        goods_category = GoodsCategory.objects.all()
        goods = Goods.objects
        res = {'goods_category': goods_category, 'goods': goods}
        return render(request, 'index.html', res)


def detail(request, id):
    if request.method == 'GET':
        good = Goods.objects.filter(pk=id).first()
        category = GoodsCategory.objects.filter(pk=good.category_id).first()
        res = {'category': category, 'good': good}
        return render(request, 'detail.html', res)


def goods_list(request, id):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        category = GoodsCategory.objects.filter(pk=id).first()
        goods = Goods.objects.filter(category=id).all()
        p = Paginator(goods, 2)
        goods = p.page(page)
        res = {'category': category, 'goods': goods}
        return render(request, 'list.html', res)


def search(request, keywords):
    print(keywords)
    if request.is_ajax():
        print(keywords)
        if not keywords:
            return JsonResponse({'url': 'http://127.0.0.1:8000/goods/indedx/'})
        good = Goods.objects.filter(name__contains=keywords).first()
        if not good:
            return JsonResponse({'url': ''})
        good_id = good.id
        return JsonResponse({'url': 'http://127.0.0.1:8000/goods/detail/%s/' % good_id})
