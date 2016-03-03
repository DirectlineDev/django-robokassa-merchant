# -*- coding: utf-8 -*-

SECRET_KEY = '_'

USE_TZ = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': ':memory:',
        'NAME': 'test.db'
    },
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'robokassa_merchant',
    'test_app',
)

ALLOWED_HOSTS = (
    'robokassa-merchant-test.src',
)

ROOT_URLCONF = 'urls'

MIDDLEWARE_CLASSES = ()

# Robokassa
ROBOKASSA_CONF = dict(
    default=dict(
        ROBOKASSA_HOST=ALLOWED_HOSTS[0],
        ROBOKASSA_LOGIN='test',
        ROBOKASSA_PASSWORD1='password1',
        ROBOKASSA_PASSWORD2='password2',
        ROBOKASSA_TEST_MODE=True,
        ROBOKASSA_USE_POST=True,
        ROBOKASSA_STRICT_CHECK=True,
    ),
)
