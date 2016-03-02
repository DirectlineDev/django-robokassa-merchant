# -*- coding: utf-8 -*-

import datetime
from django.utils import timezone


def now():
    """ Текущее время с учетом текущей временной зоны """
    return datetime.datetime.now(timezone.get_current_timezone())
