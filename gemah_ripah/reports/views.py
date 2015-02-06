import copy
import datetime

from dateutil import relativedelta

from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

from products.models import Product
from purchase.models import Purchase, PurchaseItem
from sales.models import Sales, SalesItem
from other_expenses.models import OtherExpenses


@login_required
def cash_flow(request):
    record_list = []
    total_revenues = 0
    total_expenses = 0

    temp = []
    temp.append(Sales.objects.aggregate(models.Min('date'), models.Max('date')))
    temp.append(Purchase.objects.all().aggregate(models.Min('date'), models.Max('date')))
    temp.append(OtherExpenses.objects.aggregate(models.Min('date'), models.Max('date')))
    min_max = [temp[0]['date__min'], temp[0]['date__max']]

    for i in temp:
        min_max[0] = min(min_max[0], i['date__min'])
        min_max[1] = max(min_max[1], i['date__max'])

    range_list = []
    range_start = datetime.date(min_max[0].year, min_max[0].month, 1)
    range_end = datetime.date(min_max[1].year, min_max[1].month, 1)
    curr = range_start
    while curr <= range_end:
        range_list.append({
            'text': curr.strftime("%b %Y"),
            'value': curr.strftime("%Y-%m-%d"),
        })
        curr += relativedelta.relativedelta(months=1)

    current_date = datetime.date.today()
    if request.GET.get('period'):
        current_date = datetime.datetime.strptime(request.GET['period'], "%Y-%m-%d")
    current_date = current_date.replace(day=1)

    start_date = current_date
    end_date = start_date + relativedelta.relativedelta(months=1)

    curr = start_date
    while curr < end_date:
        record_list.append({
            'date': curr,
            'revenues': 0,
            'expenses': 0,
            'draft_included': False,
            'total_draft_expenses': 0,
            'total_sold_items': 0
        })
        curr += datetime.timedelta(days=1)

    total_sold_items = 0
    for sales in Sales.objects.filter(date__gte=start_date, date__lt=end_date).prefetch_related('salesitem_set'):
        record_list[sales.date.day-1]['revenues'] += sales.net_income
        record_list[sales.date.day-1]['total_sold_items'] += sales.total_items
        total_revenues += sales.net_income
        total_sold_items += sales.total_items

    for purchase in Purchase.objects.filter(date__range=[start_date, end_date]).prefetch_related('purchaseitem_set'):
        record_list[purchase.date.day-1]['expenses'] += purchase.net_expenses
        total_expenses += purchase.net_expenses
        if not purchase.is_active:
            record_list[purchase.date.day-1]['total_draft_expenses'] += purchase.net_expenses
            record_list[purchase.date.day-1]['draft_included'] = True


    for item in OtherExpenses.objects.filter(date__range=[start_date, end_date]):
        record_list[item.date.day-1]['expenses'] += item.amount
        total_expenses += item.amount

    context = {
        'page_title': "Cash Flow Report: %s" % current_date.strftime("%b %Y"),
        'page_header': "Cash Flow Report",
        'record_list': record_list,
        'range_list': range_list,
        'total_sold_items': total_sold_items,
        'total_expenses': total_expenses,
        'total_revenues': total_revenues,
        'current_date': current_date.strftime("%Y-%m-%d")
    }

    return render(
        request,
        'reports/cash_flow.html',
        context
    )
