from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),

    url(r'^products/', include('products.urls', namespace="products")),
    url(r'^sales/', include('sales.urls', namespace="sales")),
    url(r'^purchase/', include('purchase.urls', namespace="purchase")),

    url(r'^admin/', include(admin.site.urls)),
)
