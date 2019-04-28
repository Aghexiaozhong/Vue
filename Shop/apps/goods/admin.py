from django.contrib import admin
from .models import *
# Register your models here.
from .models import GoodsCategory,Goods,GoodsImage,GoodsCategoryBrand

class GoodsCategoryAdmin(admin.ModelAdmin):
    search_fields = ('category_type','name')
    list_filter = ('category_type','parent_category')


class GoodsAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('category',)

class GoodsImageAdmin(admin.ModelAdmin):
    search_fields = ('goods',)
    list_filter = ('goods',)


class GoodsCategoryBrandAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)

class BannerAdmin(admin.ModelAdmin):
    search_fields = ('goods',)
    list_filter = ('index',)

class HotSearchWordsAdmin(admin.ModelAdmin):
    search_fields = ('keywords',)
    list_filter = ('index',)


class IndexGoodsAdmin(admin.ModelAdmin):
    search_fields = ('goods__name',)
    list_filter = ('category',)

admin.site.register(Goods,GoodsAdmin)
admin.site.register(GoodsCategory,GoodsCategoryAdmin)
admin.site.register(GoodsCategoryBrand,GoodsCategoryBrandAdmin)
admin.site.register(GoodsImage,GoodsImageAdmin)
admin.site.register(Banner,BannerAdmin)
admin.site.register(HotSearchWords,HotSearchWordsAdmin)
admin.site.register(IndexAd,IndexGoodsAdmin)







