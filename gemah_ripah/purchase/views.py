from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
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
        'page_title': "Purchase",
        'purchase_list': Purchase.objects.select_related('supplier').prefetch_related(
            models.Prefetch('purchaseitem_set', queryset=PurchaseItem.objects.select_related('product').order_by('product__name'))
        ),
        'max_per_page': 50
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
            for item in items:
                item.purchase = purchase
                item.save()
            messages.success(request, 'Record has been saved successfully.')
            return HttpResponseRedirect(".")
        else:
            messages.error(request, 'Failed to save record. Please correct the errors below.', extra_tags='danger')
    else:
        form = PurchaseForm()
        formset = PurchaseItemFormSet(
            minimum_forms=1
        )

    context = {
        'page_header': "Add New Purchase",
        'page_title': "Add New Purchase",
        'form': form,
        'formset': formset
    }

    return render(
        request,
        'purchase/add.html',
        context
    )


@login_required
def edit(request, id):
    sales = get_object_or_404(Purchase, pk=id)
    PurchaseItemFormSet = inlineformset_factory(
        Purchase,
        PurchaseItem,
        formset=MinimumRequiredFormSet,
        form=PurchaseItemForm
    )
    if request.method == "POST":
        form = PurchaseForm(request.POST, instance=sales)
        formset = PurchaseItemFormSet(
            request.POST,
            instance=sales,
            minimum_forms=1,
            minimum_forms_message="At least 1 purchase item is required."
        )
        if form.is_valid() and formset.is_valid():
            purchase = form.save()
            items = formset.save()
            for item in items:
                item.purchase = purchase
                item.save()
            messages.success(request, 'Record has been saved successfully.')
            return HttpResponseRedirect(".")
        else:
            messages.error(request, 'Failed to save record. Please correct the errors below.', extra_tags='danger')
    else:
        form = PurchaseForm(instance=sales)
        formset = PurchaseItemFormSet(
            instance=sales,
            minimum_forms=1
        )

    context = {
        'page_header': "Edit Purchase ID: %s" % id,
        'page_title': "Edit Purchase ID: %s" % id,
        'form': form,
        'formset': formset
    }

    return render(
        request,
        'purchase/edit.html',
        context
    )


@login_required
def detail(request, id):
    purchase = get_object_or_404(Purchase.objects.prefetch_related(
        models.Prefetch('purchaseitem_set', queryset=PurchaseItem.objects.select_related('product'))
    ), pk=id)

    for item in purchase.purchaseitem_set.all():
        item.estimated_margin = item.product.price - item.price
        item.estimated_profit = item.estimated_margin * item.quantity

    context = {
        'page_header': "Purchase Detail ID: %s" % id,
        'page_title': "Purchase Detail ID: %s" % id,
        'purchase': purchase
    }

    return render(
        request,
        'purchase/detail.html',
        context
    )


@login_required
def delete(request, id):
    obj = get_object_or_404(Purchase, pk=id)
    try:
        obj.delete()
        messages.success(request, 'Record has been deleted successfully.')
    except Exception, e:
        messages.error(request, 'Failed to delete record. Reason: %s' % e, extra_tags='danger')
    return HttpResponseRedirect(reverse("internal:purchase:index"))
