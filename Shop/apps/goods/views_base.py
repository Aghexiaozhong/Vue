from django.views.generic.base import View
from .models import Goods

class GoodsListView(View):
    def get(self,request):
        #通过django的views实现商品列表页
        jsonList = []
        goods = Goods.objects.all()[:10]
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name
        #     json_dict['market_price'] = good.market_price
        #     jsonList.append(json_dict)

        #导入django的模块
        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     jsonList.append(json_dict)

        import json
        from django.core import serializers
        json_data = serializers.serialize('json',goods)
        json_data = json.loads(json_data)

        from django.http import HttpResponse,JsonResponse

        return HttpResponse(json.dumps(json_data),content_type='application/json')
























