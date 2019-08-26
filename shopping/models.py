from django.db import models

# Create your models here.

# (1) 用户表 开始
class Member(models.Model):
    member_id = models.AutoField(primary_key=True,verbose_name='用户id')
    member_name = models.CharField(max_length=100,verbose_name='用户登录名',default='')
    member_nickname = models.CharField(max_length=100,verbose_name='用户昵称',null=True,blank=True)
    member_pwd = models.CharField(max_length=100,verbose_name='用户密码',null=True,blank=True)
    member_money = models.DecimalField(verbose_name='账户余额',max_digits=10,decimal_places=2,null=True,blank=True)
    member_paypwd = models.CharField(max_length=6,verbose_name='支付密码',null=True,blank=True)
    member_email = models.EmailField(max_length=100,verbose_name='用户邮箱',null=True,blank=True)
    def __str__(self):
        return self.member_name
# (1) 用户表 结束


# (2) 商品分类表开始
class Category(models.Model):
    category_id = models.AutoField(primary_key=True,verbose_name='商品分类id')
    category_name = models.CharField(max_length=60,verbose_name='商品名称',null=True,blank=True)

    # pid子类
    category_pid = models.IntegerField(verbose_name='商品分类pid',null=True,blank=True)
    # category_img = models.CharField(max_length=255, verbose_name='列表商品主图', null=True, blank=True)
    def __str__(self):
        return self.category_name
# (2) 商品分类表结束

# (3) 商品表 开始
class Goods(models.Model):
    goods_id = models.AutoField(primary_key=True,verbose_name='商品id')
    goods_name = models.CharField(max_length=60,verbose_name='商品名称',null=True,blank=True)
    goods_describe = models.CharField(max_length=255,verbose_name='商品描述',null=True,blank=True)
    goods_unit = models.CharField(max_length=60,verbose_name='单位',null=True,blank=True)
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价',null=True,blank=True)
    goods_content = models.TextField(verbose_name='商品内容',null=True,blank=True)
    goods_addtime = models.DateTimeField(auto_now_add=True,verbose_name='上架时间',null=True,blank=True)
    goods_img = models.CharField(max_length=255,verbose_name='商品主图',null=True,blank=True)

    # 一种商品有多种分类，
    category = models.ForeignKey(verbose_name='类别id', to='Category', null=True, blank=True, on_delete=models.CASCADE)



    def __str__(self):
        return self.goods_name
# (3) 商品表 结束

# (4) 商品的图片表 开始
class GoodsImg(models.Model):
    goodimg_id = models.AutoField(primary_key=True,verbose_name='商品图片表id')
    goodimg_path = models.CharField(max_length=255,verbose_name='商品图片表的路径',null=True,blank=True)
    # 一个商品有多张图片 创建与商品的一对多的关系 商品外键
    goods = models.ForeignKey(verbose_name='商品id',to='Goods',null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.goodimg_id
# (4) 商品的图片表 结束

# (5) 购物车表 开始
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True,verbose_name='购物车id')
    cart_num = models.IntegerField(verbose_name='加入购物车单个商品数量', null=True, blank=True)
    # 一个用户可以有多个购物车  用户与购物车的外键
    member = models.ForeignKey(verbose_name='用户id',to='Member',null=True,blank=True,on_delete=models.CASCADE)
    # 一个购物车有多件商品  商品与购物车的外键
    goods = models.ForeignKey(verbose_name='购物车id', to='Goods', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cart_id)


# (5) 购物车表 结束

# (6) 商品收货地址表 开始
class Address(models.Model):
    address_id = models.AutoField(primary_key=True,verbose_name='地址id')
    address_province = models.CharField(max_length=15,verbose_name='省份',null=True,blank=True)
    address_city = models.CharField(max_length=15,verbose_name='市',null=True,blank=True)
    address_area = models.CharField(max_length=15,verbose_name='区/县',null=True,blank=True)
    address_detail = models.CharField(max_length=100,verbose_name='详细地址',null=True,blank=True)
    address_tel = models.CharField(max_length=11,verbose_name='收件人手机号',null=True,blank=True)
    address_name = models.CharField(max_length=100,verbose_name='收件人名称',null=True,blank=True)
    address_post_num =models.IntegerField(verbose_name='邮编',null=True,blank=True)
    # 定义一个字段显示默认收件地址
    address_default = models.NullBooleanField(verbose_name='为true表示为默认的地址，为false表示为一般地址,默认为false',default=False)

    # 地址与用户是一对多的关系，一个用户可以有多个地址 地址与用户的外键
    member = models.ForeignKey(verbose_name='用户id',to='Member',null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.address_name
# (6) 商品收货地址表 结束

# (7) 订单表 开始
class Order(models.Model):
    order_id = models.AutoField(primary_key=True,verbose_name='下单表id')
    order_addtime = models.DateTimeField(auto_now_add=True,verbose_name='下单时间')
    order_pay_method = models.IntegerField(verbose_name='支付方式： 1:余额支付,2:微信支付,3:支付宝支付',default=1)
    order_number = models.CharField(max_length=100,verbose_name='订单号')
    order_status = models.IntegerField(verbose_name='订单状态： 1:未支付,2:已支付代发货,3:已发货待收货,4:已收货,5:已完成',default=1)

    # 订单发货地址
    order_province = models.CharField(max_length=15, verbose_name='订单省份', null=True, blank=True)
    order_city = models.CharField(max_length=15, verbose_name='订单市', null=True, blank=True)
    order_area = models.CharField(max_length=15, verbose_name='订单区/县', null=True, blank=True)
    order_detail = models.CharField(max_length=100, verbose_name='订单详细地址', null=True, blank=True)
    order_tel = models.CharField(max_length=11, verbose_name='订单收件人手机号', null=True, blank=True)
    order_addressee = models.CharField(max_length=100, verbose_name='订单收件人名称', null=True, blank=True)


    # 用户与订单是一对多的关系  用户与订单的外键
    member = models.ForeignKey(verbose_name='用户id',to='Member',null=True,blank=True,on_delete=models.CASCADE)

    # 一个地址可以收多个订单，一个订单只能有一个地址 一对多关系  订单与收货地址的外键
    address = models.ForeignKey(verbose_name='地址id',to='Address',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id
# (7) 订单表 结束

# (8) 订单详情表 开始
class OrderDetail(models.Model):
    order_detail_id = models.AutoField(primary_key=True,verbose_name='订单详情id')
    order_detail_name = models.CharField(max_length=100,verbose_name='订单详情商品的名称',null=True,blank=True)
    order_detail_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='订单详情商品的价格',null=True,blank=True)
    order_detail_num = models.IntegerField(verbose_name='订单详情商品的数量',null=True,blank=True)
    order_detail_img = models.CharField(verbose_name='订单详情商品的主图',max_length=255,null=True,blank=True)

    # 一个订单详情中有多个商品  订单详情与商品的外键
    goods = models.ForeignKey(verbose_name='商品id', to='Goods', null=True, blank=True,on_delete=models.CASCADE)

    # 一个订单详情中可能有多个订单  订单详情与订单的外键
    order = models.ForeignKey(verbose_name='订单id', to='Order', null=True, blank=True, on_delete=models.CASCADE)

# (8) 订单详情表 结束