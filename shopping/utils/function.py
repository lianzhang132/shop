import random
import datetime
def range_num(num):
    # 定义一个种子，从这里面随机拿出一个值，可以是字母
    seeds = "1234567890"
    # 定义一个空列表，每次循环，将拿到的值，加入列表
    random_num = []
    # choice函数：每次从seeds拿一个值，加入列表
    for i in range(num):
        random_num.append(random.choice(seeds))
    # 将列表里的值，变成四位字符串
    return "" . join(random_num)

def recent_seven_day():
    lists = []
    d = datetime.datetime.now()
    for i in range(1,8):
        oneday = datetime.timedelta(days=i)
        day = d-oneday
        date_to = datetime.datetime(day.year,day.month,day.day)
        lists.append(str(date_to)[0:10])
    return lists

def getWhere(request):
    where = dict()
    article_title=request.POST.get('article_title','')
    article_is_recommend = request.POST.get('article_is_recommend', '')
    member_id = request.POST.get('member_id', '')
    if article_title:
        where['article_title__icontains']=article_title
    if article_is_recommend!='':
        where['article_is_recommend'] = article_is_recommend
    if member_id:
        where['members'] = member_id
    #print(where)
    return where

def getWheres(request):
    where = dict()
    backg_name=request.POST.get('backg_name','')
    backg_tel = request.POST.get('backg_tel', '')
    backg_id = request.POST.get('backg_id', '')
   # print(backg_name)
    if backg_name:
        where['backg_name__icontains']=backg_name
    if backg_tel:
        where['backg_tel__icontains'] = backg_tel
    if backg_id:
        where['backg_id__icontains'] = backg_id

    #print(where)
    return where

def getWhereM(request):
    where = dict()
    member_nickname= request.POST.get('member_nickname','')
    member_tel = request.POST.get('member_tel', '')
    # member_id = request.POST.get('member_id', '')
   # print(backg_name)
    if member_nickname:
        where['member_nickname__icontains']=member_nickname
    if member_tel!='':
        where['member_tel'] = member_tel
    # if member_id:
    #     where['members'] = member_id
    #print(where)
    return where