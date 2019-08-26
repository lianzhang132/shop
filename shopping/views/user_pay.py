from django.shortcuts import render,HttpResponse,redirect
from shopping.models import Member
from shopping.models import Goods
from shopping.models import Address
from shopping.models import Cart
from shopping.models import Order
from shopping.models import OrderDetail
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password




def user_pay(request):
    #产生随机数 作为订单号
    import datetime
    import random
    for i in range(0, 10):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
    randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    # print(uniqueNum)
    request.session['order_num'] = uniqueNum

    res = {'status': None, 'info': None}

    member_id= request.session.get("member_id")
    member_obj=Member.objects.filter(member_id=member_id).first()
    address_list=Address.objects.filter(member_id=member_id).all()
    d1 = timezone.now()
    d2=d1.strftime("%Y-%m-%d %H:%M:%S")
    # print(d2)


    dic1=dict()
    if request.method == 'POST':
        # print(request.POST)
        # 得到每个商品的数量
        goodsnum = request.POST.getlist("goods_num",[])
        # 得到每个商品的id
        goods_id = request.POST.getlist("goods_id",[])
        order_add = request.POST.get("order_address")
        adr_obj=Address.objects.filter(address_id=order_add).first()
        pay_style = request.POST.get("pay_style")
        # print(goodsnum,goods_id,order_add)
        ord_obj = Order.objects.create(order_addtime=d2, order_pay_method=pay_style, order_number=uniqueNum,
                                       order_status=1,
                                       order_province=adr_obj.address_province, order_city=adr_obj.address_city,
                                       order_area=adr_obj.address_area, order_detail=adr_obj.address_detail,
                                       order_tel=adr_obj.address_tel, order_addressee=adr_obj.address_name,
                                       member=member_obj,address=adr_obj)
        n=0
        for m in goodsnum:
            # 因为键值不能重复 会覆盖 前面的数据 所以使用商品对象为键 对应商品数量为值
            god_obj=Goods.objects.filter(goods_id=goods_id[n]).first()

            # print(god_obj,n)
            # 创建一次订单 多次订单详情
            ord_det_obj=OrderDetail.objects.create(order_detail_name=god_obj.goods_name,order_detail_price=god_obj.goods_price,
                                                   order_detail_num=m,order_detail_img=god_obj.goods_img,
                                 goods=god_obj,order=ord_obj)
            car_obj = Cart.objects.filter(goods_id=goods_id[n],member_id=member_id).delete()
            n += 1
            if ord_obj and ord_det_obj :
                res['status'] = 1
                res['info'] = '提交成功'
            else:
                res['status'] = 2
                res['info'] = '提交失败'
        import json
        return (HttpResponse(json.dumps(res)))

def pay_password(request):
    # 怎样准确获取订单号  考虑  从立即购买链接和购物车提交 过来的存session
    # 从订单中心 立即付款过来的用？传值过来get获取
    member_id = request.session.get("member_id")
    member_obj=Member.objects.filter(member_id=member_id).first()
    order_num = request.session.get("order_num")
    member_obj = Member.objects.filter(member_id=member_id).first()
    member_money_obj = member_obj.member_money

    # print(order_num)

    if order_num:
        good_price=OrderDetail.objects.filter(order__order_number=order_num).values('order_detail_price').all()
        good_num=OrderDetail.objects.filter(order__order_number=order_num).values('order_detail_num').all()
        total_price=0
        list1=[]
        list2=[]
        # 计算本次订单总金额
        for m in good_price:
            list1.append(m["order_detail_price"])
        for m in good_num:
            list2.append(m["order_detail_num"])
        # print(list1,list2)
        num=len(list2)

        # print(num)
        for i in range(0,num):
            total_price += list1[i] * list2[i]
    else:
        order_num = request.GET.get("order_num")
        # request.session['order_num'] = order_num

        good_price = OrderDetail.objects.filter(order__order_number=order_num).values('order_detail_price').all()
        good_num = OrderDetail.objects.filter(order__order_number=order_num).values('order_detail_num').all()
        total_price = 0
        list1 = []
        list2 = []
        # 计算本次订单总金额
        for m in good_price:
            list1.append(m["order_detail_price"])
        for m in good_num:
            list2.append(m["order_detail_num"])
        # print(list1, list2)
        num = len(list2)

        # print(num)
        for i in range(0, num):
            total_price += list1[i] * list2[i]

        return render(request, 'user_pay.html', locals())

    return render(request, 'user_pay.html', locals())

def pwd_confirm(request):
    member_id = request.session.get("member_id")
    inpwd = request.POST.getlist("inpwd",[])
    cash_money = request.POST.get("cash_money")
    inpwd = "".join(inpwd)
    member_obj = Member.objects.filter(member_id=member_id).first()
    member_money_obj = member_obj.member_money
    pwd = member_obj.member_paypwd
    # res2 = check_password(inpwd, pwd)
    res2 = (inpwd==pwd)
    print(inpwd,pwd,res2,member_money_obj,cash_money)
    order_num = request.session.get("order_num")
    res3=(float(member_money_obj) - float(cash_money))>0

    res = {'status': None, 'info': None}
    if res2 and res3:
        res['status'] = 1
        res['info'] = '提交成功'
        del request.session['order_num']
        member_money_obj=float(member_money_obj)-float(cash_money)
        Order.objects.filter(order_number=order_num).update(order_status=2)
        member_obj = Member.objects.filter(member_id=member_id).update(member_money=member_money_obj)
    else:
        res['status'] = 2
        res['info'] = '密码错误或者余额不足'
    import json
    return (HttpResponse(json.dumps(res)))