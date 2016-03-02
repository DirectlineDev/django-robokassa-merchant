# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from test_app import views


urlpatterns = patterns(
    '',
    # index view
    url(r'^$', views.IndexView.as_view(), name='index'),

    # robokassa result url
    url(r'^robo_result/$', views.ResultURLView.as_view(), name='robo_result'),

    # robokassa success url
    url(r'^robo_success/$', views.SuccessURLView.as_view(), name='robo_success'),

    # robokassa fail url
    url(r'^robo_fail/$', views.FailURLView.as_view(), name='robo_fail'),
)
