from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

#ｃｒｅａｔｅd　如果是新建的，则创建

@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:

        instance.set_password(instance.password)
        instance.save()























