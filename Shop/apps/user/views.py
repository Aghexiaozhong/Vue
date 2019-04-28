from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from .serializers import SmsSerializer,UserRegisterSerializer,UserDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from random import choice
from .models import VerifyCode
from utils.yunpian import YunPian
from Shop.settings import APIKEY
from rest_framework import mixins
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler

from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

User = get_user_model()

class CustomBackend(ModelBackend):
    '''
    自定义用户验证
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username = username) | Q(mobile = username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin,viewsets.GenericViewSet):
    '''
    发送短信验证码
    '''
    serializer_class = SmsSerializer

    def generate_code(self):
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return ''.join(random_str)



    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        #raise_exception设置为true,当出错的话直接抛出异常，后面的不执行
        serializer.is_valid(raise_exception = True)

        mobile = serializer.validated_data["mobile"]
        yun_pian = YunPian(APIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code,mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                "mobile":sms_status['msg']

            },status = status.HTTP_400_BAD_REQUEST)
        else:
            #当通过验证的时候才保存验证码
            code_record = VerifyCode(code=code,mobile=mobile)
            code_record.save()
            return Response({
                "mobile":mobile
            },status = status.HTTP_201_CREATED)

#UpdateModelMixin  更新操作

class UserViewset(CreateModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    '''
    用户
    '''
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (authentication.SessionAuthentication,JSONWebTokenAuthentication)

    #动态获取serializer,重载get_serializer_class函数
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegisterSerializer
        return UserDetailSerializer


    #修改，删除等操作必须在已登录的状态,而当注册的时候则不需要验证，所以需要动态的设置
    #permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        #实现token的定制化，生成token,payload
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)

        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user


    def perform_create(self, serializer):
        return serializer.save()
















