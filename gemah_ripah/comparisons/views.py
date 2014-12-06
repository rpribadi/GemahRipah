import copy
import difflib

from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

from forms import ComparisonForm
from comparisons import parsers
from merchants.models import Merchant
from products.models import Product, ProductComparison
from purchase.models import PurchaseItem

SIMILARITY_THRESHOLD = 0.7


@login_required
def index(request):
    merchant_list = Merchant.objects.filter(
        is_active=True,
        id__in=[item['seller'] for item in ProductComparison.objects.values('seller').distinct()]
    ).order_by('code')

    merchant_map = {}
    comparison_list_template = []
    for i, merchant in enumerate(merchant_list):
        merchant_map[merchant.code] = i
        comparison_list_template.append({
            'price': None,
            'is_on_promotion': False
        })

    product_list = Product.objects.all().order_by('name').prefetch_related(
        models.Prefetch('purchaseitem_set', queryset=PurchaseItem.objects.select_related('purchase').order_by('-purchase__date', '-id'))
    ).prefetch_related(
        models.Prefetch('productcomparison_set', queryset=ProductComparison.objects.select_related('seller'))
    )

    for product in product_list:
        if product.purchaseitem_set.all().count():
            product.buy_price = product.purchaseitem_set.all()[0].price
            product.margin = product.price - product.buy_price

        product.comparison_list = copy.deepcopy(comparison_list_template)

        if product.productcomparison_set.all().count():
            _index = -1
            _price = product.price
            for item in product.productcomparison_set.all():
                i = merchant_map[item.seller.code]
                product.comparison_list[i]['is_on_promotion'] = item.is_on_promotion()
                product.comparison_list[i]['price'] = item.current_price
                if item.current_price < _price:
                    _index = i
                    _price = item.current_price

            if _index < 0:
                product.is_cheapest = True
            else:
                product.comparison_list[_index]['is_cheapest'] = True

    context = {
        'page_title': 'Price Comparison',
        'page_header': "Price Comparison",
        'product_list': product_list,
        'merchant_list': merchant_list
    }

    return render(
        request,
        'comparisons/index.html',
        context
    )

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@login_required
def manage_comparison(request):
    product_list = Product.objects.filter(is_active=True)
    comparison_list = ProductComparison.objects.all().select_related('product', 'seller')
    merchant_list = Merchant.objects.filter(
        is_active=True,
        id__in=[item['seller'] for item in ProductComparison.objects.values('seller').distinct()]
    )

    paginator_inner = Paginator(product_list, 20)
    page = request.GET.get('page')
    try:
        product_list = paginator_inner.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        product_list = paginator_inner.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        product_list = paginator_inner.page(paginator_inner.num_pages)

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
        'page_title': 'Manage Comparison',
        'page_header': "Manage Comparison",
        'product_list': product_list,
        'product_list_pagination': Product.objects.all(),
        'merchant_list': merchant_list
    }

    return render(
        request,
        'comparisons/manage_comparison.html',
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


@login_required
def import_comparison(request):

    if request.method == "POST":
        form = ComparisonForm(request.POST)
        if form.is_valid():
            parser = getattr(parsers, "parse_%s" % form.cleaned_data['seller'].code)
            if parser:
                parser(form.cleaned_data['seller'], form.cleaned_data['json'])
                messages.success(request, 'Record has been saved successfully.')
            else:
                messages.error(request, 'Can not find proper parser for the seller.', extra_tags='danger')
            return HttpResponseRedirect(".")
        else:
            messages.error(request, 'Failed to save record. Please correct the errors below.', extra_tags='danger')
    else:
        form = ComparisonForm()

    context = {
        'page_header': "Import Comparison",
        'form': form
    }

    return render(
        request,
        'comparisons/import_comparison.html',
        context
    )
