from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from models import Product


@login_required
def index(request):
    context = {
        'page_header': "Products",
        'product_list': Product.objects.all()
    }

    return render(
        request,
        'products/index.html',
        context
    )
