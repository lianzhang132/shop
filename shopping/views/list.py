from django.shortcuts import render,HttpResponse,redirect
from shopping.models import Category
from shopping.models import Goods
from shopping.models import Cart
from shopping.models import Member
from shopping.models import Order
from shopping.models import OrderDetail
from django.core.paginator import  Paginator,EmptyPage,PageNotAnInteger


def list(request,id):
    get_member_id=request.session.get('member_id')#获取会员id
    if  get_member_id:
        get_member_name=Member.objects.filter(member_id=get_member_id).values('member_nickname').first()['member_nickname']
    # print(get_member_id)
    category_list=Category.objects.all()
    category_list_part=Category.objects.filter(category_id=id)
    goods_list=Goods.objects.filter(category_id=id)
    goods_list_part =Goods.objects.filter(category_id=id).order_by('-goods_addtime')[0:2]
    # print(goods_list_part)
    from django.db.models import  Count
    cart_num=Cart.objects.filter(member_id=get_member_id).all().aggregate(count=Count('cart_num'))['count']
    # print(cart_num)
    import json
    res = {'status': None, 'info': None}
    if request.POST.get('dosubmit_praise') == '1':#ajax从前台获取信息进行会员id判断添加数据库
        get_id = request.POST.get('get_id')#从前台获取物品id
        if  get_member_id:
            # Cart.objects.filter(member_id=get_member_id)
            # print(Cart.objects.filter(member_id=get_member_id))
            a=Cart.objects.filter(goods_id=int(get_id),member_id=get_member_id).first()#从数据库拿出来用a表示
            # print(a)
            if a:
                Cart.objects.filter(goods_id=int(get_id), member_id=get_member_id).values('cart_num').first()
                get_cart_num=Cart.objects.filter(goods_id=int(get_id), member_id=get_member_id).values('cart_num').first()['cart_num']+1
                # Cart.objects.filter(goods_id=int(get_id), member_id=get_member_id).update(cart_num=get_cart_num)
                res['status']=1
                res['info']='您已经添加过该物品'
                return HttpResponse(json.dumps(res))
            if a == None:
                Cart.objects.create(cart_num=1,goods_id=int(get_id),member_id=get_member_id)
                res['status'] = 2
                res['info'] = '添加成功'
                return HttpResponse(json.dumps(res))
        else:
            res['status'] = 3
            res['info'] = '请先登录后在来添加'
            return HttpResponse(json.dumps(res))

    #搜索
    if request.method == 'POST':
        shousuo = request.POST.get('shousuo')  # 从前台获得搜索
        # print(shousuo)
        get_num = request.POST.get('get_num')
        # print(get_num)
        goods_search = Goods.objects.filter(goods_name__contains=shousuo)
        result_search=Goods.objects.filter(goods_name__contains=shousuo).first()
        if result_search:#判断有内容进行获取
            goods_search_categor=Goods.objects.filter(goods_name__contains=shousuo).values('category_id').first()['category_id']#从goods获取category的id
            category_id_name=Category.objects.filter(category_id=goods_search_categor).values('category_name').first()['category_name']#根据该物品的种类id获取category名称
        if get_num:#分页判断
            if result_search:
                currentpage = request.GET.get('page', 1)  # 获取当前页


                paginator = Paginator(goods_search.order_by('goods_id'), 5)  # 获取每页10条数据
                paginator.num_pages
                # print(paginator.num_pages)
                if paginator.num_pages > 11:
                    if currentpage - 5 < 1:  # 第五页符合，
                        pageRange = range(1, 11)
                    elif currentpage + 5 > paginator.num_pages:  # 第七页
                        pageRange = range(currentpage - 5, paginator.num_pages + 1)
                    else:
                        pageRange = range(currentpage - 5, currentpage + 5)  # 第十七页
                else:
                    pageRange = paginator.page_range
                    # 进一步优化处理，报错时兼容
                try:
                    goods_search = paginator.page(currentpage)
                except PageNotAnInteger:
                    goods_search = paginator.page(1)
                except EmptyPage:
                    goods_search = paginator.page(paginator.num_pages)

# 分页 这个是没有搜索的分页

    currentpage = request.GET.get('page', 1)  # 获取当前页


    paginator = Paginator(goods_list.order_by('goods_id'), 5)  # 获取每页10条数据
    paginator.num_pages
    # print(paginator.num_pages)
    if paginator.num_pages > 11:
        if currentpage - 5 < 1:  # 第五页符合，
            pageRange = range(1, 11)
        elif currentpage + 5 > paginator.num_pages:  # 第七页
            pageRange = range(currentpage - 5, paginator.num_pages + 1)
        else:
            pageRange = range(currentpage - 5, currentpage + 5)  # 第十七页
    else:
        pageRange = paginator.page_range
                    # 进一步优化处理，报错时兼容
    try:
        goods_list = paginator.page(currentpage)
    except PageNotAnInteger:
        goods_list = paginator.page(1)
    except EmptyPage:
        goods_list = paginator.page(paginator.num_pages)

    return render(request, 'list.html', locals())


