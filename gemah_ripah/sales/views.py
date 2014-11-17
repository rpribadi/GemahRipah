from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from models import Sales


@login_required
def index(request):
    context = {
        'page_header': "Sales",
        'sales_list': Sales.objects.all()
    }

    return render(
        request,
        'sales/index.html',
        context
    )
