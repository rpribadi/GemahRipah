import difflib

from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

from products.models import Product, ProductComparison

SIMILARITY_THRESHOLD = 0.8


@login_required
def index(request):
    product_list = Product.objects.all()
    comparison_list = ProductComparison.objects.all().select_related('product', 'seller')

    for product in product_list:
        product.comparison_list = []
        product.selected_list = []
        for comparison in comparison_list:
            ratio = difflib.SequenceMatcher(None, product.name, comparison.name).ratio()
            temp = ProductComparison(
                id=comparison.id,
                name=comparison.name,
                seller=comparison.seller,
                price=comparison.price,
            )
            temp.ratio = ratio
            if comparison.product == product:
                product.selected_list.append(temp)
            if ratio > SIMILARITY_THRESHOLD:
                temp.is_selected = False
                for item in product.selected_list:
                    if item.id == comparison.id:
                        temp.is_selected = True
                        break
                if temp.is_selected == False:
                    product.comparison_list.append(temp)

        product.comparison_list.sort(key=lambda x: x.ratio, reverse=True)
        print product, " : ", len(product.comparison_list)

    context = {
        'page_title': ': Product List',
        'page_header': "Product List",
        'product_list': product_list
    }

    return render(
        request,
        'comparisons/index.html',
        context
    )


@login_required
def edit(request):
    product = get_object_or_404(Product, pk=request.GET.get('product'))
    comparison = get_object_or_404(ProductComparison, pk=request.GET.get('comparison'))
    action = request.GET.get('action')

    if request.is_ajax():
        status = "error"
        message = ""

        if action in ["select", "remove"]:
            if action == "select":
                comparison.product = product
            else:
                comparison.product = None

            try:
                comparison.save()
            except Exception, e:
                message = "%s" % e
            else:
                status = "success"

        return JsonResponse({
            'status': status,
            'message': message,
            'action': action
        })