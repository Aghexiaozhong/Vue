# _*_ coding:utf-8 _*_

#独立使用django的model
import sys
import os

#获取当前文件路劲
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+'../')
#设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Shop.settings')

import django
django.setup()


from goods.models import *

from db_tools.data.product_data import row_data


for goods_data1 in row_data:
    goods = Goods()
    goods.name = goods_data1['name']
    goods.market_price = float(int(goods_data1['market_price'].replace('￥','').replace('元','')))
    goods.shop_price = float(int(goods_data1['sale_price'].replace('￥','').replace('元','')))
    goods.goos_brief = goods_data1['desc'] if goods_data1['goods_desc'] is not None else ""
    goods.goods_desc = goods_data1['goods_desc'] if goods_data1['desc'] is not None else ""
    goods.goos_front_image = goods_data1['images'][0] if goods_data1['images'] else ""

    category_name = goods_data1['categorys'][-1]
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

    for goods_image in goods_data1['images']:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()






