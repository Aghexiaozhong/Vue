# Generated by Django 2.1.5 on 2019-02-28 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20190123_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='goods_num',
        ),
        migrations.AddField(
            model_name='cart',
            name='nums',
            field=models.IntegerField(default=0),
        ),
    ]
