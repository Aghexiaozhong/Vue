from django.shortcuts import render

# Create your views here.

from .serializer import GoodsSerializer,CategorySerializer,GoodsCategorySerializer,HotWordsSerializer,BannerSerializer,IndexCategorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Goods,GoodsCategory,HotSearchWords,Banner
from rest_framework import status
from rest_framework import filters
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

#从filters.py导入
from .filters import GoodsFilter

from rest_framework_extensions.cache.mixins import CacheResponseMixin

from rest_framework.authentication import TokenAuthentication

from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

#分页
class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100






#直接继承generics.ListAPIView　里面有个list方法
#RetrieveModelMixin 详情页
#ListModelMixin　列表页  CacheResponseMixin放在最前面
class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    """
    List all snippets, or create a new snippet　　商品列表页.分页，过滤，排序
    """
    throttle_classes = (UserRateThrottle,AnonRateThrottle)
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name','goos_brief')
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    """
    list:
       商品分类列表页
    """

    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer

class IndexCategoryViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    首页商品分类数据
    '''
    queryset = GoodsCategory.objects.filter(is_tab=True,name__in=['生鲜食品','酒水饮料'])
    serializer_class = IndexCategorySerializer




