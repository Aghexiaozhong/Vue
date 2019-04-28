# Generated by Django 2.1.5 on 2019-03-11 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0012_auto_20190227_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodscategorybrand',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='goods.GoodsCategory', verbose_name='商品类目'),
        ),
    ]