"""Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Shop.settings import MEDIA_ROOT
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from goods.views_base import GoodsListView

from rest_framework.documentation import include_docs_urls
from goods.views import GoodsListViewSet,CategoryViewSet,HotSearchsViewset,BannerViewset,IndexCategoryViewset
from rest_framework.routers import DefaultRouter
from user.views import SmsCodeViewSet,UserViewset
from rest_framework.authtoken import views

from rest_framework_jwt.views import obtain_jwt_token

from user_operation.views import UserFavViewset,LeavingMessageViewset,AddressViewset
from trade.views import ShoppingCartViewset,OrderViewset

good_list = GoodsListViewSet.as_view(
    {
        'get':'list',

    }
)

#配置goods的url
router = DefaultRouter()
#配置categoru的url
router.register(r'goods',GoodsListViewSet,basename='goods')

router.register(r'categorys',CategoryViewSet,basename='categorys')

router.register(r'codes',SmsCodeViewSet,basename='codes')

router.register(r'users',UserViewset,basename='users')

#收藏
router.register(r'userfavs',UserFavViewset,basename='userfavs')

#热搜词
router.register(r'hotsearchs',HotSearchsViewset,basename='hotsearchs')


#用户留言
router.register(r'messages',LeavingMessageViewset,basename='messages')

#收货地址
router.register(r'address',AddressViewset,basename='address')

#购物车
router.register(r'shopcarts',ShoppingCartViewset,basename='shopcarts')

#订单相关
router.register(r'orders',OrderViewset,basename='orders')

#轮播商品
router.register(r'banners',BannerViewset,basename='banners')

#首页商品分类系列数据
router.register(r'indexgoods',IndexCategoryViewset,basename='indexgoods')



from trade.views import AliPayView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    #商品列表页
    # path(r'goods/',good_list,name='goods-list'),
    path(r'api-auth/', include('rest_framework.urls',namespace='rest_framwork')),
    path(r'docs/',include_docs_urls(title='生鲜商场')),
    path(r'',include(router.urls)),
    path(r'api-token-auth/', views.obtain_auth_token),
    #drf自带的认证接口
    path(r'login/', obtain_jwt_token),
    path(r'alipay/return/',AliPayView.as_view(),name='alipay'),
    path(r'index/',TemplateView.as_view(template_name='index.html'),name='index'),

    #第三方登录url

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)