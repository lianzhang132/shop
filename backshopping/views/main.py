from django.shortcuts import render,HttpResponse,redirect
def backindex(request):

    return render(request,'main/backindex.html',locals())

def backfooter(request):

    return render(request,'main/backfooter.html',locals())

def backleft(request):

    return render(request,'main/backleft.html',locals())

def backmain(request):

    return render(request,'main/backmain.html',locals())

def backtop(request):

    return render(request,'main/backtop.html',locals())