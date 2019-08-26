from django.contrib import admin
from django.urls import path,re_path
from shopping.views import detail
from shopping.views import cart
from shopping.views import list
from shopping.views import login
from shopping.views import place_order
from shopping.views import register
from shopping.views import user_center_info
from shopping.views import user_center_order
from shopping.views import user_center_site
from shopping.views import index
from shopping.views import user_pay

from shopping.views import loginout

from shopping.views import spgm


urlpatterns = [

    re_path('index/',index.index,name='index'),
    re_path('detail/(\d+)/',detail.detail,name='detail'),
    re_path('cart/',cart.cart,name='cart'),
    re_path('cart_update/',cart.cart_update,name='cart_update'),
    re_path('list/(\d+)/',list.list,name='list'),
    #登陆
    re_path('login/',login.login,name='login'),
    re_path('findpwd/',login.findpwd,name='findpwd'),

    #注册
    re_path('register/',register.register,name='register'),


    re_path('place_order/',place_order.place_order,name='place_order'),

    re_path('user_center_info/',user_center_info.user_center_info,name='user_center_info'),
    re_path('user_center_order/',user_center_order.user_center_order,name='user_center_order'),
    re_path('user_center_site/',user_center_site.user_center_site,name='user_center_site'),
    re_path('user_pay/',user_pay.user_pay,name='user_pay'),
    re_path('pay_password/',user_pay.pay_password,name='pay_password'),
    re_path('pwd_confirm/',user_pay.pwd_confirm,name='pwd_confirm'),
    re_path('loginout/',loginout.loginout,name='loginout'),
    re_path('spgm/(\d+)/',spgm.spgm,name='spgm'),
    re_path('spgmpd/',spgm.spgmpd,name='spgmpd'),


    # 修改
    re_path('xiugai/(\d+)/',user_center_info.xiugai,name='xiugai'),
    #删除
    re_path('delete/',cart.delete, name='delete'),


    re_path('get_valid_code_img/',register.get_valid_code_img, name='get_valid_code_img/'),

]