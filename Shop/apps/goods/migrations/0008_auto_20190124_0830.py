# Generated by Django 2.1.5 on 2019-01-24 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0007_remove_goods_goods_front_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='goos_front_image',
            field=models.ImageField(blank=True, null=True, upload_to='goods/images/', verbose_name='封面图'),
        ),
    ]
