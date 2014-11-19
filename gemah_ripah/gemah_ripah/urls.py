from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(pattern_name='products:index')),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),

    url(r'^products/', include('products.urls', namespace="products")),
    url(r'^sales/', include('sales.urls', namespace="sales")),
    url(r'^purchase/', include('purchase.urls', namespace="purchase")),

    url(r'^secured/', include(admin.site.urls)),
)
