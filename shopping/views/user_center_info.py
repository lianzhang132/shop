from django.shortcuts import render,HttpResponse,redirect
from shopping.models import Member,Goods,Order,OrderDetail,Cart,Category
import json
from shopping.my_forms import *
from django.contrib.auth.hashers import make_password,check_password
from django.core.paginator import  Paginator,EmptyPage,PageNotAnInteger

def user_center_info(request):
    ## 获取session
    member_id = request.session.get('member_id')
    # 提取到个人信息 显示到前端
    member_obj = Member.objects.filter(member_id=member_id).first()

    cart_obj = Cart.objects.filter(member_id=member_id).count()
    #遍历最近浏览
    info_obj = Goods.objects.all().order_by('-goods_addtime')

    # info_obj = OrderDetail.objects.filter(order__member_id=member_id).order_by('order__order_addtime').values('goods__goods_name','goods__goods_img','goods__goods_id','goods__goods_price','goods__goods_unit')
    res = {'status': None, 'info': None}
    if request.method == 'POST':
        goods_id=request.POST.get('goods_id')
        # print(type(goods_id))
        a = Cart.objects.filter(goods_id=int(goods_id), member_id=member_id).first()
        if a:
            res['status'] = 0
            res['info'] = '您已经添加过该物品'
            return HttpResponse(json.dumps(res))
        else:
            obj=Cart.objects.create(cart_num=1,goods_id=goods_id,member_id=member_id)
            if obj:
                res['status'] = 1
                res['info'] = '添加成功'
                return HttpResponse(json.dumps(res))
            else:
                res['status'] = 0
                res['info'] = '添加失败'
                return HttpResponse(json.dumps(res))

    # 分页
    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    paginator = Paginator(info_obj, 5)  # 告诉分页器我10条分页

    #  如果页数十分多时，换另外一种显示方式
    # print(paginator.num_pages)#一共21页
    if paginator.num_pages > 11:
        # 如果在第1-6页，显示1-10页
        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        # 当前在18,19,20,21页          显示当前页-5 -  21页
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages + 1)
        else:
            # 当前在第6，7，页 7-5=2 7+5=12
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        # 如果总页数小于等于11，pageRange 1-10
        pageRange = paginator.page_range

    try:
        # print(currentPage)
        info_obj = paginator.page(currentPage)  # 获取当前页的10条记录
    except PageNotAnInteger:
        info_obj = paginator.page(1)  # 如果page参数为负值，获取第1页的10条记录
    except EmptyPage:
        info_obj = paginator.page(1)  # 如果page参数为负值，获取第1页的10条记录

    return render(request, 'user_center_info.html', locals())



#修改个人信息
def xiugai(request,id):
    xiugai_obj = Member.objects.filter(member_id=id).first()
    # print(xiugai_obj)
    res = {'status': None, 'info': None}
    if request.method == 'POST':

        member_name = request.POST.get("member_name")
        member_nickname = request.POST.get("member_nickname")
        member_pwd = request.POST.get("member_pwd")

        r_pwd = request.POST.get("r_pwd")
        member_paypwd = request.POST.get("member_paypwd")
        # member_paypwd = make_password(request.POST.get("member_pwd"))

        member_email = request.POST.get("member_email")

        if member_name and member_nickname and member_pwd and r_pwd and member_paypwd and member_email:
            if member_pwd == r_pwd:
                #判断支付密码六位而且是整数
                if len(member_paypwd)==6 and member_paypwd.isdigit():
                    obj = Member.objects.filter(member_id=id).update(member_name=member_name, member_nickname=member_nickname,member_pwd=make_password(member_pwd), member_paypwd=member_paypwd,member_email=member_email,)
                    if obj:
                        res['status'] = 1
                        res['info'] = '修改成功'
                        return HttpResponse(json.dumps(res))
                else:
                    res['status'] = 0
                    res['info'] = '支付密码必须为六位整数'
                    return HttpResponse(json.dumps(res))

            else:
                res['status'] = 0
                res['info'] = '两次密码不一致'
                return HttpResponse(json.dumps(res))
        else:
            res['status'] = 0
            res['info'] = '信息不全,修改信息失败'
            return HttpResponse(json.dumps(res))
    return render(request, 'xiugai.html',locals())



