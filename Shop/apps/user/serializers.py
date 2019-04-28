from rest_framework import serializers
from django.contrib.auth import get_user_model
from goods.models import Goods
import re
from Shop.settings import REGEX_MOBILE
from datetime import datetime,timedelta
from .models import VerifyCode

from rest_framework.validators import UniqueValidator

User = get_user_model()

class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param mobile:
        :return:
        '''
        #手机是否注册
        if User.objects.filter(mobile = mobile).count():
            raise serializers.ValidationError('用户已存在')
        #验证手机号码是否符合规范
        if not re.match(REGEX_MOBILE,mobile):
            raise serializers.ValidationError('手机号码非法')
        #验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gt= one_minutes_ago,mobile = mobile).count():
            raise serializers.ValidationError('距离上一次发送未超过６０秒')
        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    用户详情序列化
    '''
    class Meta:
        model = User
        fields = ('name','gender','birthday','email','mobile')



class UserRegisterSerializer(serializers.ModelSerializer):
    '''
    用户注册序列化
    '''

    #wrir_only  在序列化数据的时候不会吧code序列化
    code = serializers.CharField(write_only=True,max_length=4,min_length=4,help_text="验证码",label='验证码',
                                 error_messages={
                                     "blank":"请输入验证码",
                                     "required":"请输入验证码",
                                     "max_length":"验证码格式错误",
                                     "min_length":"验证码格式错误",
                                 })

    #验证username是否存在
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    #序列化数据时不会返回密码
    password = serializers.CharField(
        style= {'input_type':'password'},
        label='密码',write_only=True,
    )

    #重载create方法，使保存到数据库的密码不是明文的
    # def create(self, validated_data):
    #     user = super(UserRegisterSerializer,self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_code(self,code):
        #initial_data是前端放进去的数据
        verfy_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by('-add_time')
        if verfy_records:
            last_record = verfy_records[0]

            one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
            if one_minutes_ago > last_record.add_time:
                raise serializers.ValidationError('验证码过期')
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')

        #没有verfy_code
        else:
            raise serializers.ValidationError('验证码错误')
    #作用于全局之上
    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username','code','mobile','password')

















