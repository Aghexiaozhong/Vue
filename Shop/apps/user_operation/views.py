from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import mixins
from .models import UserFav,UserLeavinMessage,UserAddress
from .serializers import UserFavSerializer,UserFavDetailSerializer,LeavingMessageSerializer,AddressSerializer
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


class UserFavViewset(mixins.CreateModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):

    """

        list:
            获取用户收藏列表
        retrieve:
            判断某个商品是否已经收藏
        create:
            收藏商品
    """
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    #不要在全局设置JSONWebTokenAuthentication，不然如果看商品列表页都得token验证，万一token过期则无法访问,所以就在需要验证的地方验证
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    #动态获取serializer,重载get_serializer_class函数
    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavSerializer
    #用信号量实现用户收藏＋１操作，写在signals.py　代码分离性跟高
    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     goods = instance.goods
    #     goods.fav_num += 1
    #     goods.save()

class LeavingMessageViewset(mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    '''
    list:
        获取用户留言列表
    create:
        添加留言
    delete:
        删除留言
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer
    def get_queryset(self):
        return UserLeavinMessage.objects.filter(user=self.request.user)


#viewsets.ModelViewSet　包含增删改查功能
class AddressViewset(viewsets.ModelViewSet):
    '''
        list:
            获取用户地址
        create:
            添加用户地址
        delete:
            删除用户地址
        update:
            更新用户地址
        '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)







