from django.shortcuts import render,HttpResponse,redirect
from shopping.models import Member
from shopping.models import Goods
from shopping.models import Cart
from shopping.models import Address
def place_order(request):
    member_id= request.session.get("member_id")
    get_member_id= request.session.get("member_id")
    member_obj=Member.objects.filter(member_id=member_id).first()
    if get_member_id:
        get_member_name = Member.objects.filter(member_id=get_member_id).values('member_name').first()['member_name']
    address_list=Address.objects.filter(member_id=member_id).all()
    cart_obj=Cart.objects.filter(member_id=member_id).all()

    dic1=dict()
    if request.method == 'POST':
        # print(request.POST)
        # 得到每个商品的数量

        # goodsnum = request.POST.getlist("goodsnum1",[])
        # # 得到每个商品的id
        # goods_id = request.POST.getlist("goods_id",[])
        # print(goods_id)
        goods_ids=request.POST.getlist('goods_ids',[])#从carthtml中获取物品id值
        # print(goods_ids)
        # goodsnums = request.POST.getlist('goodsnums', [])
        # print(goodsnums)

        # goodsnum = request.POST.getlist("goodsnum")
        # # 得到每个商品的id
        # goods_id = request.POST.getlist("goods_id")

        # order_add = request.POST.get("order_address")
        # print(goodsnum)
        # print(goods_id)
        goodsnums_1 = []#定义各物品数量的空列表
        goodsnums_11=Cart.objects.filter(member_id=member_id,goods_id__in=goods_ids).all().values('cart_num')#从数据库拿去各物品的件数
        import json
        goodsnums_11_json = json.dumps(list(goodsnums_11))#将数据序列化json格式(物品的件数)

        goodsnums_11_json_reverse=json.loads(goodsnums_11_json)#将序列化数据反序列化成list格式(物品的件数)

        for v2 in goodsnums_11_json_reverse:
            goodsnums_1_1=v2['cart_num']
            goodsnums_1.append(goodsnums_1_1)#将物品件数进行增加个列表格式


        n=0
        for m in goodsnums_1:
            # 因为键值不能重复 会覆盖 前面的数据 所以使用商品对象为键 对应商品数量为值
            dic1[Goods.objects.filter(goods_id=goods_ids[n]).first()]=m
            Cart.objects.filter(member_id=member_id,goods_id=goods_ids[n]).update(cart_num=m)
            n+=1

    return render(request, 'place_order.html', locals())