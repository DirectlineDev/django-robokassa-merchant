# -*- coding: utf-8 -*-

# Статусы заказов
STATUS_CREATED = 0
STATUS_SUCCESS = 1
STATUS_FAIL = 2
STATUS = (
    (STATUS_CREATED, 'Created'),
    (STATUS_SUCCESS, 'Success'),
    (STATUS_FAIL, 'Fail'),
)

# Статусы заказа в Robokassa todo проверять через XML-интерфейс
ROBOKASSA_STATUS = (
    (5, 'Initialized'),
    (10, 'Cancelled'),
    (50, 'Received payment, sending to store account'),
    (60, 'Returned to customer account'),
    (80, 'Stopped or restricted'),
    (100, 'Successfully paid'),
)
