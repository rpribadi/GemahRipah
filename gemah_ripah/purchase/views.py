from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from gemah_ripah.forms import MinimumRequiredFormSet
from forms import PurchaseForm, PurchaseItemForm
from models import Purchase, PurchaseItem


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
    PurchaseItemFormSet = inlineformset_factory(
        Purchase,
        PurchaseItem,
        formset=MinimumRequiredFormSet,
        form=PurchaseItemForm
    )
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        formset = PurchaseItemFormSet(
            request.POST,
            minimum_forms=1,
            minimum_forms_message="At least 1 purchase item is required."
        )
        if form.is_valid() and formset.is_valid():
            purchase = form.save()
            items = formset.save(commit=False)
            form_status = "valid"
            for item in items:
                item.purchase = purchase
                item.save()
            return HttpResponseRedirect(".")
        else:
            form_status = "error"
            print "FORM INVALID"
            print form.errors
            print formset.errors
            print formset.non_form_errors()
    else:
        form_status = "new"
        form = PurchaseForm()
        formset = PurchaseItemFormSet(
            minimum_forms=1
        )


    context = {
        'page_header': "Add New Purchase",
        'form': form,
        'formset': formset,
        'form_status': form_status
    }

    return render(
        request,
        'purchase/add.html',
        context
    )


@login_required
def detail(request, id):
    purchase = get_object_or_404(Purchase, pk=id)

    context = {
        'page_header': "Purchase Detail",
        'purchase': purchase
    }

    return render(
        request,
        'purchase/detail.html',
        context
    )