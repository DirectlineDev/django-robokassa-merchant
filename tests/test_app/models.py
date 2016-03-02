# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Sum, F
from django.dispatch.dispatcher import receiver
from robokassa_merchant.signals import *
from robokassa_merchant.utils import now


__all__ = ['Item', 'Order', 'ItemInOrder', ]


class Item(models.Model):
    """ Товар
    """
    title = models.CharField(verbose_name='Название', max_length=250)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, default=0)
    amount_in_stock = models.IntegerField(verbose_name='Кол-во на складе', default=0)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    """ Заказ
    """
    full_name = models.CharField(verbose_name='ФИО покупателя', max_length=100)
    create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    payment_date = models.DateTimeField(verbose_name='Дата оплаты', blank=True, null=True)
    is_cancelled = models.BooleanField(verbose_name='Отменён', default=False)

    class Meta:
        verbose_name = 'заказе'
        verbose_name_plural = 'заказы'

    def get_total_price(self):
        return self.iteminorder_set.aggregate(total_price=Sum(F('item__price') * F('amount')))['total_price']


@receiver(robokassa_result_received, sender=Order)
def complete_order(invoice, **kwargs):
    """ Успешная оплата
    """
    order = invoice.content_object
    order.payment_date = now()
    order.save()


@receiver(robokassa_fail_page_visited, sender=Order)
def order_fail_page_visited(invoice, **kwargs):
    """ Посещение Fail URL
    """
    # todo: по сути, то не является гарантом отмены оплаты, в доке пишут, что пользователь может завершить платёж, поэтому требуется доработка robokassa_merchant
    order = invoice.content_object
    order.is_cancelled = True
    order.save()


class ItemInOrder(models.Model):
    """ Товар в заказе
    """
    order = models.ForeignKey('test_app.Order', verbose_name='Заказ')
    item = models.ForeignKey('test_app.Item', verbose_name='Товар')
    amount = models.IntegerField(verbose_name='Кол-во товара в заказе')

    class Meta:
        verbose_name = 'товар в заказе'
        verbose_name_plural = 'товар в заказах'
