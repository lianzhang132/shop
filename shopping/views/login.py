from django.shortcuts import render,HttpResponse,redirect
from shopping.models import Member
import json,threading
from shopping.utils import function
from django.core.mail import send_mail
from shop import settings
from django.contrib.auth.hashers import make_password, check_password
def login(request):
    res = {'status': None, 'info': None}
    #print('第一个')
    if request.method == 'POST':
        #print('第二个')
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        # password = check_password(request.POST.get("pwd"),)
        #print(username,password)
        isLogin = Member.objects.filter(member_name=username).first()
        a = Member.objects.all().filter()
        # print(a)
        # print('第三个')
        shaixuan = isLogin.member_pwd
        # print(cc)
        print(password)
        jiemi = check_password(password,shaixuan)
        # print(ccc)
        if jiemi:
        #print(a)
        #print(isLogin)
            if isLogin:
                res['status'] = 1
                res['info'] = '登录成功'
                request.session['member_id'] = isLogin.member_id
                request.session['member_name'] = isLogin.member_name
                request.session['member_nickname'] = isLogin.member_nickname
                #print('登录成功')
                return HttpResponse(json.dumps(res))
            else:
                res['status'] = 0
                res['info'] = '登陆失败'
                #print('登陆失败')
                return HttpResponse(json.dumps(res))
        else:
            res['status'] = 2
            res['info'] = '密码错误'
            return HttpResponse(json.dumps(res))
    return render(request, 'login.html', locals())


def findpwd(request):
    res = {'status': None, 'info': None}
    if request.method == 'POST':
        member_name = request.POST.get("member_name")
        member_email = request.POST.get("member_email")
        member_obj = Member.objects.filter(member_email=member_email,
                                           member_name=member_name)
        npwd = function.range_num(6)
        pwd = make_password(npwd)
        if member_obj:
            find = member_obj.update(member_pwd=pwd)
            pwd1 = int(npwd)
            aaa = threading.Thread(target=send_mail, args=(
                '%s在找回密码' % member_obj.first().member_nickname,
                '您的密码已经被找回，新密码为%d' % pwd1,
                settings.EMAIL_HOST_USER,
                [member_email]
            ))
            aaa.start()

            if find:
                res['status'] = 1
                res['info'] = '密码修改成功，请重新登陆'
                return HttpResponse(json.dumps(res))
            else:
                res['status'] = 0
                res['info'] = '密码修改失败'
                return HttpResponse(json.dumps(res))
        else:
            res['status'] = 0
            res['info'] = '用户名邮箱错误，请重新输入'
            return HttpResponse(json.dumps(res))

    return render(request,'findpwd.html',locals())