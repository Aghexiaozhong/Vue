# Generated by Django 2.1.5 on 2019-02-28 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0004_auto_20190228_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[('sucess', '支付成功'), ('cancel', '取消'), ('paying', '待支付')], default='paying', max_length=10, verbose_name='订单状态'),
        ),
    ]