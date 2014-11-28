from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count, Min, Sum, Avg, F, FloatField
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

from other_expenses.models import OtherExpenses
from products.models import Product
from purchase.models import Purchase, PurchaseItem
from sales.models import Sales, SalesItem


@login_required
def index(request):
    purchase = Purchase.objects.aggregate(Sum('discount'), Sum('other_expenses'))
    purchase_items = PurchaseItem.objects.aggregate(
        total=Sum('price', field="price*quantity")
    )

    sales = Sales.objects.aggregate(Sum('discount'))
    sales_items = SalesItem.objects.aggregate(
        total=Sum('price', field="price*quantity")
    )

    purchase_other_expenses = purchase['other_expenses__sum'] if purchase['other_expenses__sum'] else 0
    purchase_discount = purchase['discount__sum'] if purchase['discount__sum'] else 0

    sales = sales['discount__sum'] if sales['discount__sum'] else 0
    purchase_items = purchase_items['total'] if purchase_items['total'] else 0
    sales_items = sales_items['total'] if sales_items['total'] else 0

    other_expenses = OtherExpenses.objects.aggregate(Sum('amount'))
    other_expenses = other_expenses['amount__sum'] if other_expenses['amount__sum'] else 0

    inventory = Product.objects.aggregate(Sum('total_purchased'), Sum('total_sold'))
    inventory['total_purchased__sum'] = inventory['total_purchased__sum'] if inventory['total_purchased__sum'] else 0
    inventory['total_sold__sum'] = inventory['total_sold__sum'] if inventory['total_sold__sum'] else 0

    total_product_expenses = (purchase_items + purchase_other_expenses - purchase_discount)
    total_income = (sales_items - sales)

    out_of_stock_list = Product.objects.extra(
        where=["total_sold >= total_purchased",]
    ).filter(
        is_active=True, total_purchased__gt=0
    ).order_by('name')

    context = {
        'page_header': "Summaries",
        'inventory': {
            'total_purchased': inventory['total_purchased__sum'],
            'total_sold': inventory['total_sold__sum'],
            'in_stock': inventory['total_purchased__sum'] - inventory['total_sold__sum']
        },
        'cash_flow': {
            'total_product_expenses': int(total_product_expenses),
            'total_other_expenses': int(other_expenses),
            'total_income': int(total_income),
            'profit': int(total_income - (total_product_expenses + other_expenses))
        },
        'latest_sold_items': SalesItem.objects.select_related('sales', 'product').order_by('-sales__date')[:20],
        'popular_products': Product.objects.filter(total_sold__gt=0).order_by('-total_sold', 'name')[:20],
        'out_of_stock_list': out_of_stock_list
    }

    return render(
        request,
        'dashboard/index.html',
        context
    )
