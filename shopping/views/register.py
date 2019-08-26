from django.shortcuts import render,HttpResponse,redirect
from shopping.models import Member
import json
from shopping.my_forms import *
from django.contrib.auth.hashers import make_password, check_password
from shopping.utils import validCode,function,sendMsg

def register(request):
    res = {'status': None, 'info': None}

    if request.method == 'POST':
        valid_code = request.POST.get("valid_code")
        valid_code_str = request.session.get("valid_code_str")
        import json
        if valid_code.upper() == valid_code_str.upper():
            # 判断验证
            form = UserForm(request.POST)
            if not form.is_valid():
                import json
                res['status'] = 0
                res['info'] = form.errors
                return HttpResponse(json.dumps(res))
            member_name = request.POST.get("member_name")
            # member_pwd = request.POST.make_password("member_pwd")
            member_pwd = make_password(request.POST.get("member_pwd"))
            member_nickname = request.POST.get("member_nickname")
            member_email = request.POST.get("member_email")
            member_obj = Member.objects.create(member_name=member_name,
                                               member_pwd=member_pwd,
                                               member_email=member_email,
                                               member_nickname=member_nickname,)
            if member_obj:
                res['status'] = 1
                res['info'] = '注册并登录成功'
            else:
                res['status'] = 2
                res['info'] = '注册失败'

            import json
            response_new = HttpResponse(json.dumps(res))
            request.session['member_id'] = member_obj.member_id
            request.session['member_name'] = member_obj.member_name
            request.session['member_nickname'] = member_obj.member_nickname
            return response_new
        else:
            res['status'] = 3
            res['info'] = '验证码错误'
            return HttpResponse(json.dumps(res))

    return render(request, 'register.html', locals())


def get_valid_code_img(request):
    img_data = validCode.get_valid_code_img(request)
    return HttpResponse(img_data)