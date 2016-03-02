# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import transaction
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from robokassa_merchant import options
from robokassa_merchant.utils import now
from robokassa_merchant.models import *
from robokassa_merchant.forms import ResultURLForm, SuccessRedirectForm, FailRedirectForm
from robokassa_merchant.signals import robokassa_result_received, robokassa_success_page_visited, robokassa_fail_page_visited


class BaseRobokassaView(View):
    """ Базовый класс вьюхи для вьюх робокассы
    Дочерние классы должны присвоить объект конфигурации робокассы в conf
    Свой код вьюхи надо писать в переопределённом методе process_request,
    вызвав родительский метод и вернув в итоге Response
    """
    # todo: отрефакторить процесс обработки запроса, выделив для пользовательского кода отдельный метод
    # Объект конфигурации робокассы
    conf = None
    # Инвойс
    invoice = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if not self.conf:
            raise ImproperlyConfigured('No Conf object for robokassa view')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        if self.conf.USE_POST:
            return HttpResponseBadRequest('Need POST')
        return self.process_request(request, request.GET)

    def post(self, request):
        if not self.conf.USE_POST:
            return HttpResponseBadRequest('Need GET')
        return self.process_request(request, request.POST)

    def process_request(self, request, data):
        raise NotImplemented('BaseRobokassaView._process_request MUST be implemented in inherited CBVs')


class BaseResultURLView(BaseRobokassaView):
    """ Базовый класс вьюхи для Result URL
    """

    def process_request(self, request, data):
        form = ResultURLForm(self.conf, data)
        if form.is_valid():
            with transaction.atomic():
                inv_id, out_sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']
                self.invoice = Invoice.objects.get(id=inv_id)

                # посылаем сигнал
                robokassa_result_received.send(
                    sender=self.invoice.content_object.__class__,
                    invoice=self.invoice,
                    inv_id=inv_id,
                    out_sum=out_sum,
                    extra=form.extra_params()
                )

                # обновляем инвойс
                self.invoice.payment_date = now()
                self.invoice.status_changed(options.STATUS_SUCCESS, 'Оплата прошла по ResultURL')

            return HttpResponse('OK{}'.format(inv_id))  # Ответ для робокассы, что всё норм
        return HttpResponse('Error: bad signature')


class BaseSuccessURLView(BaseRobokassaView):
    """ Базовый класс вьюхи для Success URL
    """
    def process_request(self, request, data):
        form = SuccessRedirectForm(self.conf, data)
        if form.is_valid():
            with transaction.atomic():
                inv_id, out_sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']
                self.invoice = Invoice.objects.get(id=inv_id)

                # посылаем сигнал
                robokassa_success_page_visited.send(
                    sender=self.invoice.content_object.__class__,
                    invoice=self.invoice,
                    inv_id=inv_id,
                    out_sum=out_sum,
                    extra=form.extra_params()
                )

                # обновляем инвойс
                self.invoice.status_changed(options.STATUS_SUCCESS, 'Посещение по success url')
        else:
            raise ValidationError('Robokassa data not valid')
        return HttpResponse('Спасибо за оплату :)')


class BaseFailURLView(BaseRobokassaView):
    """ Базовый класс вьюхи для Fail URL
    """
    def process_request(self, request, data):
        form = FailRedirectForm(self.conf, data)
        if form.is_valid():
            with transaction.atomic():
                inv_id, out_sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']
                self.invoice = Invoice.objects.get(id=inv_id)

                # посылаем сигнал
                robokassa_fail_page_visited.send(
                    sender=self.invoice.content_object.__class__,
                    invoice=self.invoice,
                    inv_id=inv_id,
                    out_sum=out_sum,
                    extra=form.extra_params()
                )

                # обновляем инвойс
                self.invoice.status_changed(options.STATUS_FAIL, 'Посещение по fail url')
        else:
            raise ValidationError('Robokassa data not valid')
        return HttpResponse('Оплата отменена, товар разблокирован :(')
