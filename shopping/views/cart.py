from django.shortcuts import render,HttpResponse,redirect
from shopping.models import Goods
from shopping.models import Cart,Member
import json


def cart(request):

    ## 获取session
    member_id = request.session.get('member_id')
    member_obj=Member.objects.filter(member_id=member_id).first()
    cart_list = Cart.objects.filter(member_id=member_id).all()

    return render(request, 'cart.html', locals())

def cart_update(request):
    res = {'status': None, 'info': None}
    member_id = request.session.get('member_id')
    if request.method == 'POST':
        shuliang=int(request.POST.get('shuliang'))
        goods_id=request.POST.get('goods_id')
        cart_obj=Cart.objects.filter(member_id=member_id,goods_id=goods_id).update(cart_num=shuliang)
        if cart_obj:
            res['status'] = 1
            res['info'] = '购物车数量改变'
        return HttpResponse(json.dumps(res))

#删除
def delete(request):
    id=request.POST.get('id')
    result=Cart.objects.filter(cart_id=id).delete()
    import json
    res = {'status': None, 'info': None}
    if result:
        res['status'] = 1
        res['info'] = '删除成功'
        return HttpResponse(json.dumps(res))
    else:
        res['status'] = 0
        res['info'] = '删除失败'
        return HttpResponse(json.dumps(res))