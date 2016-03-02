# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from robokassa_merchant.utils import now


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(default=now, verbose_name='Время события')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Created'), (1, 'Success'), (2, 'Fail')], verbose_name='Тип события')),
                ('message', models.CharField(null=True, max_length=255, verbose_name='Сообщение')),
            ],
            options={
                'verbose_name_plural': 'события',
                'ordering': ('-create_date',),
                'verbose_name': 'событие',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='ID объекта приложения')),
                ('create_date', models.DateTimeField(default=now, verbose_name='Дата создания')),
                ('payment_date', models.DateTimeField(null=True, blank=True, verbose_name='Дата оплаты')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=12, default=0, verbose_name='Итоговая сумма')),
                ('current_status', models.PositiveSmallIntegerField(default=0, choices=[(0, 'Created'), (1, 'Success'), (2, 'Fail')], verbose_name='Текущий статус')),
                ('description', models.CharField(null=True, max_length=250, blank=True, verbose_name='Описание')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', verbose_name='Приложение', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь', null=True)),
            ],
            options={
                'verbose_name_plural': 'Счёта к оплате',
                'ordering': ('-create_date',),
                'verbose_name': 'Счёт к оплате',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='invoice',
            field=models.ForeignKey(to='robokassa_merchant.Invoice', related_name='events', verbose_name='Счёт к оплате'),
        ),
    ]
