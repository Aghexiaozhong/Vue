
from rest_framework import serializers
from .models import Goods
from .models import Cart,OrderInfo,OrderGoods
from goods.serializer import GoodsSerializer
import time

class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = Cart
        fields = '__all__'








#继承serializers.Serializer 而不是　serializers.ModelSerializer,因为对购物车user ,goods需要使用联合唯一索引
#而之前用户收藏则是如果已经存在同一用户收藏同一物品则不需要再收藏，而购物车不同，如果使用serializers.ModelSerializer
#则会在validator的时候抛出异常，就不会执行后面的程序，所以得继承更底层的serializers.Serializer
class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True,label='数量',min_value=1,
                                    error_messages={
                                        "min_value":"商品数量不能小于１",
                                        "required":"请选择购买数量"
                                    })
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(),required=True)



    #对于serializers.Serializer  user是保存在context['request]中
    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = Cart.objects.filter(user=user,goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += 1
            existed.save()

        else:
            existed = Cart.objects.create(**validated_data)

        return existed
    def update(self, instance, validated_data):
        #修改商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance

from Shop.settings import ali_pub_key_path,private_key_path
from utils.alipay import AliPay

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    #不能自己提交订单状态,订单号,交易号,支付日期,得由后台处理，所以设置为read_only

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    alipay_url = serializers.SerializerMethodField(read_only=True)


    def get_alipay_url(self,obj):
        alipay = AliPay(
            appid="2016092700611765",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject= obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url


    def generate_order_sn(self):
        #当前时间＋userid+随机数
        from random import Random

        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),userid=self.context['request'].user.id,
                                                   ranstr=random_ins.randint(10,99) )
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016092700611765",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url
    class Meta:
        model = OrderInfo
        fields = '__all__'










