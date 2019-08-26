from django.shortcuts import render,HttpResponse,redirect
from shopping.models import *

def user_center_site(request):

    get_member_id = request.session.get('member_id')  # 获取会员id
    if get_member_id:
        get_member_name = Member.objects.filter(member_id=get_member_id).values('member_name').first()['member_name']

    res = {'status': None, 'info': None}    #设置一个标杆
    #接收前台传过来的数据
    shoujianren = request.POST.get('shoujianren')
    dizhi = request.POST.get('dizhi')
    youbian = request.POST.get('youbian')
    shouji = request.POST.get('shouji')
    province = request.POST.get('province') #省
    city = request.POST.get('city') #市
    area = request.POST.get('area') #区

    address = Address.objects.filter(address_default=1,member_id=get_member_id).first()
    if request.method == 'POST':
        if shoujianren and shouji:
            res['status'] = 3  # 成功的话把标杆赋值成3
            res['info'] = '添加成功'
            book_obj = Address.objects.create(address_name=shoujianren,address_detail=dizhi,address_post_num=youbian,address_tel=shouji,address_province=province,address_city=city,address_area=area,member_id=get_member_id)
        else:
            res['status'] = 2  # 失败的话把标杆赋值成2
            res['info'] = '请填写完整信息'

        import json
        return HttpResponse(json.dumps(res))#通过json方式把数据结果在传给前台

    return render(request, 'user_center_site.html', locals())