from django import template
register = template.Library()
from decimal import Decimal

#两个数相乘
@register.simple_tag
def multi_filter(a,b)->str:
    return Decimal(str(a)) * Decimal(str(b))

#全部的总数
@register.simple_tag
def get_orderAll(a)->str:
    num = 0
    for i in a:
        num += Decimal(str(i.order_detail_price))*Decimal(str(i.order_detail_num))
    return num