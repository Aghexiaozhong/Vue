from django.shortcuts import render

# Create your views here.
import time
from rest_framework import viewsets
from .models import Cart,OrderInfo,OrderGoods
from .serializers import ShopCartSerializer,ShopCartDetailSerializer,OrderSerializer,OrderDetailSerializer

from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .models import Cart
from rest_framework import mixins

from Shop.settings import ali_pub_key_path,private_key_path

class ShoppingCartViewset(viewsets.ModelViewSet):
    '''
    购物车功能

    list:
        获取购物车详情
    create:
        加入购物车
    delete:
        删除购物车
    update:
        更新购物车
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    lookup_field = "goods_id"

    #动态获取serializer
    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer



    #获取列表页
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class OrderViewset(mixins.DestroyModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    '''
    订单管理
    list:
        获取个人订单列表
    create:
        新增订单
    detele:
        删除订单
    retrieve:
        获取订单详情页
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer
    # lookup_field = "goods_id"

    #获取当前用户的订单
    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        #获取订单详情
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        #在保存之前生成订单号


        order = serializer.save()
        #查询出购物车所有的商品信息
        shop_carts = Cart.objects.filter(user=self.request.user)
        #保存购物车中的所有商品,生成订单(order_goods表)后清空购物车
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()

        return order

#这是和支付宝相关的　和model没相关
from rest_framework.views import APIView
from utils.alipay import AliPay
from datetime import datetime
from rest_framework.response import Response

from django.shortcuts import redirect

class AliPayView(APIView):
    #支持get(对应return_url的同步访问，就是支付完返回页面),post（notify_url,异步的访问，
    # 就是只要你扫码后就会创建订单，就算不付款，也可以在支付宝订单中继续支付完成交易）两种方式
    def get(self,request):
        '''
        处理支付宝的return_url返回
        :param request:
        :return:
        '''

        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        # 对以上信息进行验证,验证支付是否有效
        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()

                existed_order.save()

            # 一旦我们返回了success,支付宝则不会再重复发送success

            response =  redirect('index')
            response.set_cookie('nextPath','pay',max_age=2)
            return response
        else:
            response = redirect('index')

            return response



    def post(self,request):
        '''
        处理支付宝的notify_url
        :param request:
        :return:
        '''
        processed_dict = {}
        for key,value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        #对以上信息进行验证,验证支付是否有效
        verify_re = alipay.verify(processed_dict,sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no',None)
            trade_no = processed_dict.get('trade_no',None)
            trade_status = processed_dict.get('trade_status',None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()

                existed_order.save()

            #一旦我们返回了success,支付宝则不会再重复发送success
            return Response('success')