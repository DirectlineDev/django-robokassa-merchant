# -*- coding: utf-8 -*-

from django.test import TestCase
from robokassa_merchant.models import Invoice

from test_app.models import *


class CounterTestCase(TestCase):
    def setUp(self):
        # человек хочет заказать 5 единиц товара из 10 имеющихся
        item = Item.objects.create(
            pk=1,
            title='Электровеник',
            price=500,
            amount_in_stock=10
        )
        order = Order.objects.create(pk=1, full_name='Жирмунский Пофистал Владленович')
        item_in_order = ItemInOrder.objects.create(item=item, order=order, amount=5)
        order.iteminorder_set.add(item_in_order)

    def test_Order_get_total_price(self):
        order = Order.objects.first()
        total_price = order.get_total_price()
        self.assertEqual(total_price, 2500)

    def test_invoice_creation(self):
        order = Order.objects.first()
        invoice = Invoice.objects.create(
            content_object=order,
            total_price=order.get_total_price()
        )

        # todo ???