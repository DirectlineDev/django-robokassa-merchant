# -*- coding: utf-8 -*-

from django.conf import settings
from django.test import TestCase

from robokassa_merchant.models import Invoice
from robokassa_merchant.forms import *
from robokassa_merchant.conf import Conf

from test_app.models import *


class ConfTest(TestCase):
    """ Тестирование класса Conf
    """
    def setUp(self):
        self.conf = Conf('default')

    def testConf(self):
        default = settings.ROBOKASSA_CONF['default']
        self.assertEqual(self.conf.LOGIN, default['ROBOKASSA_LOGIN'])
        self.assertEqual(self.conf.PASSWORD1, default['ROBOKASSA_PASSWORD1'])
        self.assertEqual(self.conf.PASSWORD2, default['ROBOKASSA_PASSWORD2'])
        self.assertEqual(self.conf.USE_POST, default['ROBOKASSA_USE_POST'])
        self.assertEqual(self.conf.STRICT_CHECK, default['ROBOKASSA_STRICT_CHECK'])
        self.assertEqual(self.conf.TEST_MODE, default['ROBOKASSA_USE_POST'])


class ModelsTestCase(TestCase):
    """ Тестирование моделей
    """
    def setUp(self):
        # человек хочет заказать 5 единиц товара из 10 имеющихся
        item = Item.objects.create(
            pk=1,
            title='iPhone',
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

    def test_invoice(self):
        order = Order.objects.first()
        invoice = Invoice.objects.create(
            content_object=order,
            total_price=order.get_total_price()
        )
        self.assertEqual(1, Invoice.objects.for_object(order).count())
        self.assertEqual(invoice, Invoice.objects.for_object(order).first())

        # invoice.status_changed()  # todo


class RobokassaFormTest(TestCase):
    """ Тестирование формы RobokassaForm
    """
    def setUp(self):
        self.conf = Conf('default')
        self.form = RobokassaForm(conf=self.conf, initial={
            'OutSum': 500.00,
            'InvId': 124,
            'Desc': 'iPhone',
            'Email': 'test@example.com'
        })

    def testSignature(self):
        self.assertEqual(self.form._get_signature_string(),
                         "{}:500.0:124:{}".format(self.conf.LOGIN, self.conf.PASSWORD1).encode('utf-8'))
        self.assertEqual(len(self.form.fields['SignatureValue'].initial), 32)

    def testRedirectUrl(self):
        url = "https://merchant.roboxchange.com/Index.aspx?MrchLogin=test&OutSum=500.0&InvId=124&Desc=iPhone&SignatureValue=3B0F0CE2A42AE0CAB9121D9D9ECF0026&Email=test%40example.com&IsTest=1"
        self.assertEqual(str(self.form.get_redirect_url()), str(url))
