from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from models import Purchase, PurchaseItem
from forms import PurchaseForm, PurchaseItemForm


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


@login_required
def add(request):
    PurchaseItemFormSet = inlineformset_factory(Purchase, PurchaseItem)
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        formset = PurchaseItemFormSet(request.POST)
        if form.is_valid and formset.is_valid():
            purchase = form.save()
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(".")
    else:
        form = PurchaseForm()
        formset = PurchaseItemFormSet()


    context = {
        'page_header': "Add New Purchase",
        'form': form,
        'formset': formset,
    }

    return render(
        request,
        'purchase/add.html',
        context
    )
