from django.urls import path,re_path
from backshopping.views import main
urlpatterns = [

    re_path('backindex/',main.backindex,name='backindex'),
    re_path('backfooter/',main.backfooter,name='backfooter'),
    re_path('backleft/',main.backleft,name='backleft'),
    re_path('backmain/',main.backmain,name='backmain'),
    re_path('backtop/',main.backtop,name='backtop'),




]