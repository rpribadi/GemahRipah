from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView


shop_urls = patterns('',
    url(r'^$', 'shop.views.home', name="home"),
    url(r'^contact-us/', 'shop.views.contact_us', name="contact_us"),

)

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(pattern_name='shop:home')),
    url(r'^shop/', include(shop_urls, namespace="shop")),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),

    url(r'^admin/$', RedirectView.as_view(pattern_name='dashboard')),
    url(r'^admin/dashboard/$', 'dashboard.views.index', name='dashboard'),
    url(r'^admin/products/', include('products.urls', namespace="products")),
    url(r'^admin/sales/', include('sales.urls', namespace="sales")),
    url(r'^admin/purchase/', include('purchase.urls', namespace="purchase")),
    url(r'^admin/other-expenses/', include('other_expenses.urls', namespace="other_expenses")),
    url(r'^admin/merchants/', include('merchants.urls', namespace="merchants")),

    url(r'^secured/', include(admin.site.urls)),
)
