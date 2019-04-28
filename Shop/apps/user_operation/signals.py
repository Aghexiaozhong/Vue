from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from django.conf import settings
from .models import UserFav

User = get_user_model()

#ｃｒｅａｔｅd　如果是新建的，则创建  对于增加和删除需要自定义方法的时候都可以考虑信号量

@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()






