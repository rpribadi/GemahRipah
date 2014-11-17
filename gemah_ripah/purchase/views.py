from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from models import Purchase


@login_required
def index(request):
    context = {
        'page_header': "Purchase",
        'purchase_list': Purchase.objects.all()
    }

    return render(
        request,
        'purchase/index.html',
        context
    )
