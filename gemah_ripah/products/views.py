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
    product_list = Product.objects.all().order_by('name').prefetch_related(
        models.Prefetch('purchaseitem_set', queryset=PurchaseItem.objects.filter(purchase__is_active=True).select_related('purchase').order_by('-purchase__date', '-id'), to_attr='purchase_items')
    )

    for product in product_list:
        if len(product.purchase_items):
            product.buy_price = product.purchase_items[0].price
            product.margin = product.price - product.buy_price

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
    product = get_object_or_404(Product, pk=id)
    product.buy_price = None
    product.margin = None

    purchase_list = product.purchaseitem_set.filter(purchase__is_active=True).select_related("purchase", "purchase__supplier").order_by('-purchase__date', '-id')

    if len(purchase_list):
        product.buy_price = purchase_list[0].price
        product.margin = product.price - product.buy_price


    if request.is_ajax():
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'stock': product.stock,
            'margin': product.margin,
            'buy_price': product.buy_price,
        })

    comparison_list = product.productcomparison_set.all().select_related('seller').order_by('-last_modified')
    sales_list = product.salesitem_set.all().select_related("sales").order_by('-sales__date')

    context = {
        'page_header': "Product Detail ID: %s" % product.id,
        'product': product,
        'comparison_list': comparison_list,
        'purchase_list': purchase_list,
        'sales_list': sales_list
    }

    return render(
        request,
        'products/detail.html',
        context
    )
