# Generated by Django 2.1.5 on 2019-02-27 11:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0010_auto_20190128_1353'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_operation', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfav',
            unique_together={('user', 'goods')},
        ),
    ]