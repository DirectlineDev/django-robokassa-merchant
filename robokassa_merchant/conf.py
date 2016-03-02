# -*- coding: utf-8 -*-

from django.conf import settings


class Conf:
    """ Класс конфигурации для робокассы, берёт настройки из settings.ROBOKASSA_CONF
    """
    # todo: в большинстве случаев 1 магазин на 1 сайт - сделать необязательным параметр token

    # обязательные параметры - реквизиты магазина
    LOGIN = ''
    PASSWORD1 = ''
    PASSWORD2 = ''

    # url, по которому будет идти отправка форм
    FORM_TARGET = 'https://merchant.roboxchange.com/Index.aspx'
    # использовать ли метод POST при приеме результатов
    USE_POST = True
    # требовать предварительного уведомления на ResultURL
    STRICT_CHECK = True

    # тестовый режим
    TEST_MODE = False
    # список пользовательских параметров ("shp" к ним приписывать не нужно)
    EXTRA_PARAMS = []

    def __init__(self, token):
        if token not in settings.ROBOKASSA_CONF:
            raise ValueError('Can not find "{}" in settings.ROBOKASSA_CONF'.format(token))
        config = settings.ROBOKASSA_CONF[token]

        self.LOGIN = config['ROBOKASSA_LOGIN']
        self.PASSWORD1 = config['ROBOKASSA_PASSWORD1']
        self.PASSWORD2 = config.get('ROBOKASSA_PASSWORD2', None)

        self.USE_POST = config.get('ROBOKASSA_USE_POST', True)
        self.STRICT_CHECK = config.get('ROBOKASSA_STRICT_CHECK', True)
        self.TEST_MODE = config.get('ROBOKASSA_TEST_MODE', False)
        self.EXTRA_PARAMS = sorted(config.get('ROBOKASSA_EXTRA_PARAMS', []))
