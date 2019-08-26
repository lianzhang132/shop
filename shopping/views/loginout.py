from django.shortcuts import render,HttpResponse,redirect

def loginout(request):
        # del request.session["member_id"]  # 删除session
        # del request.session["member_nickname"]  # 删除session
        request.session.flush()#删除所有session
        return redirect("/shopping/login/")

