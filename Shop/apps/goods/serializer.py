from rest_framework import serializers
from .models import Goods,GoodsCategory,GoodsImage,HotSearchWords,Banner,GoodsCategoryBrand,IndexAd
from django.db.models import Q

class CategorySerializer3(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = ('__all__')


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = ('__all__')



class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'



class GoodsImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = '__all__'



class GoodsCategorySerializer(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    category = CategorySerializer()
    class Meta:
        model = Goods
        fields = ('__all__')


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"
#首页商品
class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)

    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self,obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_ins = ad_goods[0].goods
            #当serializer中嵌套有serializer的时候，images的路径是相对路径，不会解析为绝对路径，所以需要设置context
            goods_json = GoodsSerializer(good_ins,many=False,context={'request':self.context['request']}).data
        return goods_json

    def get_goods(self,obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        goods_serialzer = GoodsSerializer(all_goods,many=True)
        #返回序列化的数据
        return goods_serialzer.data
    class Meta:
        model = GoodsCategory
        fields = "__all__"














