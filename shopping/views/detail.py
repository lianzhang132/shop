from django.shortcuts import render,HttpResponse,redirect
from shopping.models import Goods,Cart,Member
import json
def detail(request,id):
    res = {'status': None, 'info': None}
    xiangqing = Goods.objects.filter(goods_id=id).first()
    xinpin = Goods.objects.all().order_by("-goods_id")[0:2]
    member_id=request.session.get('member_id')
    member_obj=Member.objects.filter(member_id=member_id).first()
    gwc = Cart.objects.filter(member_id=member_id).count()
    if request.method =='POST':
        if member_id:
            gwc_obj=Cart.objects.filter(member_id=member_id,goods_id=id)
            print(gwc_obj)
            if gwc_obj:
                res['status'] = 0
                res['info'] = '您已添加过此类商品'
            else:
                shuliang = request.POST.get("shuliang")
                obj = Cart.objects.create(cart_num=shuliang, goods_id=id, member_id=member_id)
                if obj:
                    res['status'] = 1
                    res['info'] = '添加成功'
                else:
                    res['status'] = 0
                    res['info'] = '添加失败'
                return HttpResponse(json.dumps(res))
            return HttpResponse(json.dumps(res))
        else:
            res['status'] = 0
            res['info'] = '请登录后再进行购买'
            return HttpResponse(json.dumps(res))
    return render(request, 'detail.html', locals())