from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^cash-flow/$', views.cash_flow, name='cash_flow'),
)