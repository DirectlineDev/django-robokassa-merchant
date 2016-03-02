# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='Название', max_length=250)),
                ('price', models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=10, default=0)),
                ('amount_in_stock', models.IntegerField(verbose_name='Кол-во на складе', default=0)),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='ItemInOrder',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('amount', models.IntegerField(verbose_name='Кол-во товара в заказе')),
                ('item', models.ForeignKey(verbose_name='Товар', to='test_app.Item')),
            ],
            options={
                'verbose_name': 'товар в заказе',
                'verbose_name_plural': 'товар в заказах',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('full_name', models.CharField(verbose_name='ФИО покупателя', max_length=100)),
                ('create_date', models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)),
                ('payment_date', models.DateTimeField(verbose_name='Дата оплаты', null=True, blank=True)),
                ('is_cancelled', models.BooleanField(verbose_name='Отменён', default=False)),
            ],
            options={
                'verbose_name': 'заказе',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.AddField(
            model_name='iteminorder',
            name='order',
            field=models.ForeignKey(verbose_name='Заказ', to='test_app.Order'),
        ),
    ]
