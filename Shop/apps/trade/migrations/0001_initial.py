# Generated by Django 2.1.5 on 2019-01-23 13:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField(default=0)),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name_plural': '购物车',
                'verbose_name': '购物车',
            },
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField(default=0, verbose_name='商品数量')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name_plural': '订单商品',
                'verbose_name': '订单商品',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_sn', models.CharField(max_length=30, verbose_name='订单号')),
                ('trade_no', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='交易编号')),
                ('pay_status', models.CharField(choices=[('sucess', '支付成功'), ('cancel', '取消'), ('cancel', '待支付')], max_length=10, verbose_name='订单状态')),
                ('post_script', models.CharField(max_length=200, verbose_name='订单留言')),
                ('order_mount', models.FloatField(default=0, verbose_name='订单金额')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='支付时间')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('address', models.CharField(default='', max_length=100, verbose_name='收货地址')),
                ('signer_name', models.CharField(default='', max_length=20, verbose_name='签收人姓名')),
                ('signer_mobile', models.CharField(max_length=11, verbose_name='联系电话')),
            ],
            options={
                'verbose_name_plural': '订单',
                'verbose_name': '订单',
            },
        ),
    ]