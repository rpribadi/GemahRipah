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
    purchase = Purchase.objects.aggregate(Sum('discount'))
    purchase_items = PurchaseItem.objects.aggregate(
        total=Sum('price', field="price*quantity")
    )

    sales = Sales.objects.aggregate(Sum('discount'))
    sales_items = SalesItem.objects.aggregate(
        total=Sum('price', field="price*quantity")
    )

    purchase = purchase['discount__sum'] if purchase['discount__sum'] else 0
    sales = sales['discount__sum'] if sales['discount__sum'] else 0
    purchase_items = purchase_items['total'] if purchase_items['total'] else 0
    sales_items = sales_items['total'] if sales_items['total'] else 0

    other_expenses = OtherExpenses.objects.aggregate(Sum('amount'))
    inventory = Product.objects.aggregate(Sum('total_purchased'), Sum('total_sold'))

    total_product_expenses = (purchase_items - purchase)
    total_income = (sales_items - sales)

    context = {
        'page_header': "Summaries",
        'inventory': {
            'total_purchased': inventory['total_purchased__sum'],
            'total_sold': inventory['total_sold__sum'],
            'in_stock': inventory['total_purchased__sum'] - inventory['total_sold__sum']
        },
        'cash_flow': {
            'total_product_expenses': int(total_product_expenses),
            'total_other_expenses': int(other_expenses['amount__sum']),
            'total_income': int(total_income),
            'profit': int(total_income - (total_product_expenses + other_expenses['amount__sum']))
        },
        'latest_sold_items': SalesItem.objects.all().order_by('-sales__date')[:10],
        'latest_purchased_items': PurchaseItem.objects.all().order_by('-purchase__date')[:10]
    }

    return render(
        request,
        'dashboard/index.html',
        context
    )
