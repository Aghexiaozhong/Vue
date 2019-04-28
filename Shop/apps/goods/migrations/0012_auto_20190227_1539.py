# Generated by Django 2.1.5 on 2019-02-27 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0011_hotsearchwords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='is_hot',
            field=models.BooleanField(default=False, help_text='是否热销', verbose_name='是否热销'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='is_new',
            field=models.BooleanField(default=False, help_text='是否新品', verbose_name='是否新品'),
        ),
    ]
