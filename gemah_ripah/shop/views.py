from django.db import models
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from products.models import Product


def home(request):
    latest = Product.objects.latest('last_modified')
    context = {
        'page_title': ': Product List',
        'page_header': "Product List",
        'product_list': Product.objects.filter(is_active=True, total_purchased__gt=0),
        'latest_product': latest
    }

    return render(
        request,
        'shop/home.html',
        context
    )

def contact_us(request):
    context = {
        'page_header': ": Contact Us",
    }

    return render(
        request,
        'shop/contact_us.html',
        context
    )