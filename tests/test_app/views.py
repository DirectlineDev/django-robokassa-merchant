# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import View
from robokassa_merchant.views import BaseFailURLView, BaseSuccessURLView, BaseResultURLView
from robokassa_merchant import Conf


class IndexView(View):
    def get(self, request):
        return HttpResponse('Main Page')


class ResultURLView(BaseResultURLView):
    """ Обработка result url """
    conf = Conf('default')


class SuccessURLView(BaseSuccessURLView):
    """ Обработка success url """
    conf = Conf('default')

    def process_request(self, request, data):
        super().process_request(request, data)

        messages.success(request, 'Вы успешно оплатили заказ!')

        return redirect(reverse('index'))


class FailURLView(BaseFailURLView):
    """ Обработка fail url """
    conf = Conf('default')

    def process_request(self, request, data):
        super().process_request(request, data)

        messages.error(request, 'Оплата заказа не прошла, товар из заказа разблокирован и доступен для покупки всем. '
                                'Вы можете снова попробовать сделать заказ, либо обратиться в техническую поддержку, '
                                'если у Вас списались денежные средства')
        return redirect(reverse('index'))
