import copy
import difflib

from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

from products.models import Product
from purchase.models import Purchase, PurchaseItem
from sales.models import Sales, SalesItem


@login_required
def cash_flow(request):
    record_list = []

    context = {
        'page_title': 'Cash Flow Report',
        'page_header': "Cash Flow Report",
        'record_list': record_list,
    }

    return render(
        request,
        'reports/cash_flow.html',
        context
    )
