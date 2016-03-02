# -*- coding: utf-8 -*-

from django.dispatch import Signal


signal_args = ['sender', 'invoice', 'inv_id', 'out_sum']
robokassa_result_received = Signal(providing_args=signal_args)
robokassa_success_page_visited = Signal(providing_args=signal_args)
robokassa_fail_page_visited = Signal(providing_args=signal_args)
