# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from robokassa_merchant import options
from robokassa_merchant.utils import now

__all__ = ['Invoice', 'Event', ]


class InvoiceQuerySet(models.QuerySet):
    def for_object(self, obj):
        if not (getattr(obj, 'id', None) and obj.id):
            raise ValueError('Can not filter by object "{}", it has no "id" field or its value'.format(obj))
        return self.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id
        )


class Invoice(models.Model):
    # связь с объектом приложения
    content_type = models.ForeignKey(ContentType, verbose_name='Приложение', null=True)
    object_id = models.PositiveIntegerField(verbose_name='ID объекта приложения', null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # основная информация
    create_date = models.DateTimeField(verbose_name="Дата создания", default=now)
    payment_date = models.DateTimeField(verbose_name="Дата оплаты", blank=True, null=True)
    total_price = models.DecimalField(verbose_name="Итоговая сумма", max_digits=12, decimal_places=2, default=0)
    current_status = models.PositiveSmallIntegerField(verbose_name="Текущий статус", default=0,
                                                      choices=options.STATUS)

    # дополнительная информация
    description = models.CharField(max_length=250, verbose_name='Описание', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь", blank=True, null=True)

    objects = InvoiceQuerySet.as_manager()

    class Meta:
        verbose_name = 'Счёт к оплате'
        verbose_name_plural = 'Счёта к оплате'
        ordering = ('-create_date', )

    def __str__(self):
        return '{}: on {} for {}rub'.format(
            self.create_date,
            self.content_object,
            self.total_price,
            self.get_current_status_display(),
        )

    def status_changed(self, status, message=''):
        """ Логирует событие счёта оплаты
        """
        self.events.add(
            Event(status=status, message=message)
        )
        if self.current_status != status:
            self.current_status = status
        self.save()


class Event(models.Model):
    invoice = models.ForeignKey(Invoice, verbose_name='Счёт к оплате', related_name='events')
    create_date = models.DateTimeField('Время события', default=now)

    status = models.PositiveSmallIntegerField(verbose_name="Тип события", choices=options.STATUS)
    message = models.CharField('Сообщение', max_length=255, null=True)

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'события'
        ordering = ('-create_date', )

    def __str__(self):
        return 'for inv "{}": [{}] {}'.format(
            self.invoice,
            self.get_status_display(),
            self.message
        )
