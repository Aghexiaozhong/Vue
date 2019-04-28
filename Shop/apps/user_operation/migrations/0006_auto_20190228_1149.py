# Generated by Django 2.1.5 on 2019-02-28 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0005_auto_20190228_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='district',
            field=models.CharField(default='', help_text='区域', max_length=100, verbose_name='区域'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='address',
            field=models.CharField(default='', help_text='详细地址', max_length=100, verbose_name='详细地址'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='signer_mobile',
            field=models.CharField(default='', help_text='签收电话', max_length=11, verbose_name='电话'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='signer_name',
            field=models.CharField(default='', help_text='签收人', max_length=100, verbose_name='签收人'),
        ),
    ]
