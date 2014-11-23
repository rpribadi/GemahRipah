from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

from purchase.models import Purchase, PurchaseItem
from forms import ProductForm
from models import Product


@login_required
def index(request):
    product_list = Product.objects.all().prefetch_related(
        models.Prefetch('purchaseitem_set', queryset=PurchaseItem.objects.select_related('purchase').order_by('-purchase__date', '-id'))
    )

    for product in product_list:
        if product.purchaseitem_set.all().count():
            product.buy_price = product.purchaseitem_set.all()[0].price

    context = {
        'page_header': "Products",
        'product_list': product_list
    }

    return render(
        request,
        'products/index.html',
        context
    )


@login_required
def add_edit(request, id=None):
    obj = None
    if id:
        obj = get_object_or_404(Product, pk=id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been saved successfully.')
            if id:
                return HttpResponseRedirect(reverse("products:index"))
            return HttpResponseRedirect(".")
        else:
            messages.error(request, 'Failed to save record. Please correct the errors below.', extra_tags='danger')
    else:
        form = ProductForm(instance=obj)

    context = {
        'page_header': ("Edit Product ID: %s" % id) if id else "Add New Product",
        'form': form
    }

    return render(
        request,
        'products/add_edit.html',
        context
    )


@login_required
def detail(request, id):
    obj = get_object_or_404(Product, pk=id)

    if request.is_ajax():
        return JsonResponse({
            'id': obj.id,
            'name': obj.name,
            'price': obj.price,
            'stock': obj.stock,
        })
