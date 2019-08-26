from django.shortcuts import render,HttpResponse,redirect
from shopping.models import Goods,Cart,Address,Member,Order,OrderDetail
import json
from django.utils import timezone

def spgm(request,id):
    res = {'status': None, 'info': None}
    member_id = request.session.get('member_id')
    member_obj = Member.objects.filter(member_id=member_id).first()
    address=Address.objects.filter(member_id=member_id)
    danjia=Goods.objects.filter(goods_id=id).values('goods_price')[0]['goods_price']
    shangpin=Goods.objects.filter(goods_id=id).first()
    if request.POST.get('shuliang'):
        shuliang=request.POST.get('shuliang')
        xiaoji = danjia *int(shuliang)
    return render(request,'spgm_order.html',locals())

def spgmpd(request):
    res = {'status': None, 'info': None}
    member_id = request.session.get('member_id')
    if request.method == 'POST':
        if member_id:
            # 产生随机数 作为订单号
            import datetime
            import random
            for i in range(0, 10):
                nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
            randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
            if randomNum <= 10:
                randomNum = str(0) + str(randomNum)
            uniqueNum = str(nowTime) + str(randomNum)
            # print(uniqueNum)
            request.session['order_num'] = uniqueNum

            res = {'status': None, 'info': None}

            member_id = request.session.get("member_id")
            member_obj = Member.objects.filter(member_id=member_id).first()
            address_list = Address.objects.filter(member_id=member_id).all()
            d1 = timezone.now()
            d2 = d1.strftime("%Y-%m-%d %H:%M:%S")
            # print(d2)
            dic1 = dict()
            # 得到每个商品的数量
            goodsnum = request.POST.get("goods_num")
            # 得到每个商品的id
            goods_id = request.POST.get("goods_id")
            order_add = request.POST.get("order_address")
            adr_obj = Address.objects.filter(address_id=order_add).first()
            pay_style = request.POST.get("pay_style")
            ord_obj = Order.objects.create(order_addtime=d2, order_pay_method=pay_style, order_number=uniqueNum,
                                           order_status=1,
                                           order_province=adr_obj.address_province, order_city=adr_obj.address_city,
                                           order_area=adr_obj.address_area, order_detail=adr_obj.address_detail,
                                           order_tel=adr_obj.address_tel, order_addressee=adr_obj.address_name,
                                           member=member_obj, address=adr_obj)

            god_obj = Goods.objects.filter(goods_id=goods_id).first()

            ord_det_obj = OrderDetail.objects.create(order_detail_name=god_obj.goods_name,
                                                         order_detail_price=god_obj.goods_price,
                                                         order_detail_num=goodsnum, order_detail_img=god_obj.goods_img,
                                                         goods=god_obj, order=ord_obj)

            if ord_obj and ord_det_obj:
                res['status'] = 1
                res['info'] = '提交订单成功'
            return HttpResponse(json.dumps(res))
        else:
            res['status'] = 0
            res['info'] = '请登录后再进行操作'
        return HttpResponse(json.dumps(res))