# -*- coding: utf-8 -*-

from hashlib import md5
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from django import forms


__all__ = ['BaseRobokassaForm', 'RobokassaForm', 'ResultURLForm', 'SuccessRedirectForm', 'FailRedirectForm']


class BaseRobokassaForm(forms.Form):

    def __init__(self, conf, *args, **kwargs):
        super(BaseRobokassaForm, self).__init__(*args, **kwargs)
        self.conf = conf
        # IsTest field
        self.fields['IsTest'] = forms.IntegerField(initial=1 if self.conf.TEST_MODE else 0)

        # создаем дополнительные поля
        for key in self.conf.EXTRA_PARAMS:
            self.fields['shp'+key] = forms.CharField(required=False)
            if 'initial' in kwargs:
                self.fields['shp'+key].initial = kwargs['initial'].get(key, 'None')

    def _cleaned_value(self, name):
        return str(self.cleaned_data[name])

    def _append_extra_part(self, standard_part, value_func):
        extra_part = ":".join(["%s=%s" % ('shp'+key, value_func('shp' + key)) for key in self.conf.EXTRA_PARAMS])
        if extra_part:
            return ':'.join([standard_part, extra_part])
        return standard_part

    def extra_params(self):
        extra = {}
        for param in self.conf.EXTRA_PARAMS:
            if ('shp'+param) in self.cleaned_data:
                extra[param] = self.cleaned_data['shp'+param]
        return extra

    def _get_signature(self):
        return md5(self._get_signature_string()).hexdigest().upper()

    def _get_signature_string(self):
        raise NotImplementedError


class RobokassaForm(BaseRobokassaForm):

    # login магазина в обменном пункте
    MrchLogin = forms.CharField(max_length=20)

    # требуемая к получению сумма
    OutSum = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2, required=False)

    # номер счета в магазине (должен быть уникальным для магазина)
    InvId = forms.IntegerField(min_value=0, required=False)

    # описание покупки
    Desc = forms.CharField(max_length=100, required=False)

    # контрольная сумма MD5
    SignatureValue = forms.CharField(max_length=32)

    # предлагаемая валюта платежа
    IncCurrLabel = forms.CharField(max_length=10, required=False)

    # e-mail пользователя
    Email = forms.CharField(max_length=100, required=False)

    # язык общения с клиентом (en или ru)
    Culture = forms.CharField(max_length=10, required=False)

    # Параметр с URL'ом, на который форма должны быть отправлена.
    # Может пригодиться для использования в шаблоне.
    target = ''

    def __init__(self, conf, *args, **kwargs):
        super(RobokassaForm, self).__init__(conf, *args, **kwargs)

        # скрытый виджет по умолчанию
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        self.fields['MrchLogin'].initial = self.conf.LOGIN
        self.fields['SignatureValue'].initial = self._get_signature()
        self.target = self.conf.FORM_TARGET

    def get_redirect_url(self):
        """ Получить URL с GET-параметрами, соответствующими значениям полей в
        форме. Редирект на адрес, возвращаемый этим методом, эквивалентен
        ручной отправке формы методом GET.
        """
        def _initial(name, field):
            val = self.initial.get(name, field.initial)
            if not val:
                return val
            return val

        fields = [(name, _initial(name, field))
                  for name, field in self.fields.items()
                  if _initial(name, field)]
        params = urlencode(fields)
        return self.target+'?'+params

    def _get_signature_string(self):
        def _val(name):
            value = self.initial[name] if name in self.initial else self.fields[name].initial
            if value is None:
                return ''
            return value
        standard_part = ':'.join([_val('MrchLogin'), str(_val('OutSum')), str(_val('InvId')), self.conf.PASSWORD1])
        return self._append_extra_part(standard_part, _val).encode('utf-8')


class ResultURLForm(BaseRobokassaForm):
    """ Форма для приема результатов и проверки контрольной суммы
    """
    OutSum = forms.CharField(max_length=15)
    InvId = forms.IntegerField(min_value=0)
    SignatureValue = forms.CharField(max_length=32)

    def clean(self):
        try:
            signature = self.cleaned_data['SignatureValue'].upper()
            if signature != self._get_signature():
                raise forms.ValidationError('Ошибка в контрольной сумме')
        except KeyError:
            raise forms.ValidationError('Пришли не все необходимые параметры')

        return self.cleaned_data

    def _get_signature_string(self):
        standard_part = ':'.join([self._cleaned_value('OutSum'), self._cleaned_value('InvId'), self.conf.PASSWORD2])
        return self._append_extra_part(standard_part, self._cleaned_value).encode('utf-8')


class SuccessRedirectForm(ResultURLForm):
    """ Форма для обработки страницы Success с дополнительной защитой. Она
    проверяет, что ROBOKASSA предварительно уведомила систему о платеже,
    отправив запрос на ResultURL. """
    Culture = forms.CharField(max_length=10)

    def clean(self):
        data = super().clean()
        # if STRICT_CHECK:AdvertPromotionOrder.objects.get(id=id, total_price = sum)
        #     if not AdvertPromotionOrder.objects.filter(id=data['InvId'], status=2):
        #         raise forms.ValidationError('От ROBOKASSA не было предварительного уведомления')
        return data

    def _get_signature_string(self):
        standard_part = ':'.join([self._cleaned_value('OutSum'), self._cleaned_value('InvId'), self.conf.PASSWORD1])
        return self._append_extra_part(standard_part, self._cleaned_value).encode('utf-8')


class FailRedirectForm(BaseRobokassaForm):
    """ Форма приема результатов для перенаправления на страницу Fail
    """
    OutSum = forms.CharField(max_length=15)
    InvId = forms.IntegerField(min_value=0)
    Culture = forms.CharField(max_length=10)
