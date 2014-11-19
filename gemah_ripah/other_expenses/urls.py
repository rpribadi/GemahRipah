from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add_edit, name='add'),
    url(r'^edit/(?P<id>\d+)/$', views.add_edit, name='edit'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
)