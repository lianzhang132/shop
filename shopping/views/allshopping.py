from django.shortcuts import render,HttpResponse,redirect
from shopping.models import Category
from shopping.models import Goods
from shopping.models import  Cart
def allshopping(request):
    get_member_id = request.session.get('member_id')  # 获取会员id
    from django.db.models import Count
    cart_num = Cart.objects.filter(member_id=get_member_id).all().aggregate(count=Count('cart_num'))['count']
    category_1 = Category.objects.filter(category_id=1).first()
    category_2 = Category.objects.filter(category_id=2).first()
    category_3 = Category.objects.filter(category_id=3).first()
    category_4 = Category.objects.filter(category_id=4).first()
    category_5 = Category.objects.filter(category_id=5).first()
    category_6 = Category.objects.filter(category_id=6).first()
    goods_1 = Goods.objects.filter(category_id=1)[0:4]
    goods_2 = Goods.objects.filter(category_id=2)[0:4]
    goods_3 = Goods.objects.filter(category_id=3)[0:4]
    goods_4 = Goods.objects.filter(category_id=4)[0:4]
    goods_5 = Goods.objects.filter(category_id=5)[0:4]
    goods_6 = Goods.objects.filter(category_id=6)[0:4]

    category_goods = {category_1: goods_1, category_2: goods_2, category_3: goods_3, category_4: goods_4,
                      category_5: goods_5, category_6: goods_6}
    categorys = Category.objects.all()
    # print(category_goods)

    return render(request, 'index.html', locals())