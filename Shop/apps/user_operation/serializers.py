from rest_framework import serializers
from .models import UserFav
from rest_framework.validators import UniqueTogetherValidator
from goods.serializer import GoodsSerializer
from .models import UserLeavinMessage,UserAddress
from Shop.settings import REGEX_MOBILE
class UserFavDetailSerializer(serializers.ModelSerializer):
	goods = GoodsSerializer()

	class Meta:
		model = UserFav
		fields = ('goods','id')


#收藏，fields = ('user','goods')逻辑不对，不应该是我们来选择用户，而是选择收藏商品的时候顺便把当前用户的user写进去
class UserFavSerializer(serializers.ModelSerializer):
	#获取当前用户
	user = serializers.HiddenField(
		default=serializers.CurrentUserDefault()
	)
	class Meta:
		model = UserFav
		validators = [
			UniqueTogetherValidator(
				queryset= UserFav.objects.all(),
				fields= ('user','goods'),
				message='您已经收藏过'
			)
		]
		fields = ('user','goods','id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')


    class Meta:
        model = UserLeavinMessage
        fields = ('user','message_type','message','subject','file','id','add_time')



class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    province = serializers.CharField(max_length=10)
    #add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    def validated_province(self,province):
        province = UserAddress.objects.filter(province=self.initial_data['province'])
        print(province)
        if province:
            return province
        else:
            raise serializers.ValidationError('省份不能为空')



    class Meta:
        model = UserAddress
        fields = ('id','user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile')



