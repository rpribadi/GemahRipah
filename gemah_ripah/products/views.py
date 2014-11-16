from django.shortcuts import render

from models import Product

# Create your views here.
def index(request):
    context = {
        'product_list': Product.objects.all()
    }

    return render(
        request,
        'products/index.html',
        context
    )
