from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^delete(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^(?P<id>\d+)/$', views.detail, name='detail'),
)