from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from shopping.models import *


# def user_center_order(request):
#
#     menmberID = request.session.get('member_id')
#     request.session.get('order_detail_name')

#     #未付款
#     orderNO_dict = {}
#     orderNOs = Order.objects.filter(order_status=1, member_id=menmberID)  # 找到这个用户没有付款的订单
#     for x in orderNOs:  # 循环这个订单
#         orderNO_dict[x] = OrderDetail.objects.filter(order_id=x.order_id)  # 拿到这个订单里的商品ID

#     #已付款
#     orderYES_dict = {}
#     dingdanhao = {}
#     orderYESs = Order.objects.filter(order_status=2,member_id=menmberID)
#     for x in orderYESs:
#         orderYES_dict[x] = OrderDetail.objects.filter(order_id=x.order_id)




def user_center_order(request):

    get_member_id = request.session.get('member_id')  # 获取会员id
    if get_member_id:
        get_member_name = Member.objects.filter(member_id=get_member_id).values('member_name').first()['member_name']

    # num = []
    orderNO_dict = {}      #先定义一个空字典
    orderNOs = Order.objects.filter(member_id=get_member_id)  # 找到这个用户的全部订单
    for x in orderNOs:  # 循环订单
        orderNO_dict[x] = OrderDetail.objects.filter(order_id=x.order_id)  # 拿到订单里的商品ID
    # num.append(orderNO_dict)



    # currentpage = int(request.GET.get('page', 1))  # 当前第几页
    # paginator = Paginator(num,2)
    # if paginator.num_pages > 11:  # 如果总页数大于11
    #     if currentpage - 5 < 1:
    #         pageRange = range(1, 11)
    #     elif currentpage + 5 > paginator.num_pages:
    #         pageRange = range(currentpage - 5, paginator.num_pages + 1)
    #     else:
    #         pageRange = range(currentpage - 5, currentpage + 5)
    # else:
    #     pageRange = paginator.page_range
    # try:
    #     num = paginator.page(currentpage)
    # except PageNotAnInteger:
    #     num = article_list = paginator.page(1)
    # except EmptyPage:
    #     num = article_list = paginator.page(1)

    return render(request, 'user_center_order.html', locals())