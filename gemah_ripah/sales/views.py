from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from gemah_ripah.forms import MinimumRequiredFormSet
from forms import SalesForm, SalesItemForm
from models import Sales, SalesItem


@login_required
def index(request):
    context = {
        'page_header': "Sales",
        'page_title': "Sales",
        'sales_list': Sales.objects.all().prefetch_related(
            models.Prefetch("salesitem_set", queryset=SalesItem.objects.select_related("product").order_by('product__name'))
        ),
        'max_per_page': 50
    }

    return render(
        request,
        'sales/index.html',
        context
    )

@login_required
def add(request):
    SalesItemFormSet = inlineformset_factory(
        Sales,
        SalesItem,
        formset=MinimumRequiredFormSet,
        form=SalesItemForm,
        extra=2
    )
    if request.method == "POST":
        form = SalesForm(request.POST)
        formset = SalesItemFormSet(
            request.POST,
            minimum_forms=1,
            minimum_forms_message="At least 1 sales item is required."
        )
        if form.is_valid() and formset.is_valid():
            sales = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.sales = sales
                item.save()
            messages.success(request, 'Record has been saved successfully.')
            return HttpResponseRedirect(".")
        else:
            messages.error(request, 'Failed to save record. Please correct the errors below.', extra_tags='danger')
    else:
        form = SalesForm()
        formset = SalesItemFormSet(
            minimum_forms=1
        )

    context = {
        'page_header': "Add New Sales",
        'page_title': "Add New Sales",
        'form': form,
        'formset': formset
    }

    return render(
        request,
        'sales/add.html',
        context
    )


@login_required
def edit(request, id):
    sales = get_object_or_404(Sales, pk=id)
    SalesItemFormSet = inlineformset_factory(
        Sales,
        SalesItem,
        formset=MinimumRequiredFormSet,
        form=SalesItemForm,
        extra=1
    )
    if request.method == "POST":
        form = SalesForm(request.POST, instance=sales)
        formset = SalesItemFormSet(
            request.POST,
            instance=sales,
            minimum_forms=1,
            minimum_forms_message="At least 1 Sales item is required."
        )
        if form.is_valid() and formset.is_valid():
            sales = form.save()
            items = formset.save()
            for item in items:
                item.sales = sales
                item.save()
            messages.success(request, 'Record has been saved successfully.')
            return HttpResponseRedirect(".")
        else:
            messages.error(request, 'Failed to save record. Please correct the errors below.', extra_tags='danger')
    else:
        form = SalesForm(instance=sales)
        formset = SalesItemFormSet(
            instance=sales,
            minimum_forms=1
        )

    context = {
        'page_header': "Edit Sales ID: %s" % id,
        'page_title': "Edit Sales ID: %s" % id,
        'form': form,
        'formset': formset
    }

    return render(
        request,
        'sales/edit.html',
        context
    )


@login_required
def detail(request, id):
    sales = get_object_or_404(Sales.objects.prefetch_related(
        models.Prefetch('salesitem_set', queryset=SalesItem.objects.select_related('product'))
    ), pk=id)

    context = {
        'page_header': "Sales Detail ID: %s" % id,
        'page_title': "Sales Detail ID: %s" % id,
        'sales': sales
    }

    return render(
        request,
        'sales/detail.html',
        context
    )


@login_required
def delete(request, id):
    obj = get_object_or_404(Sales, pk=id)
    try:
        obj.delete()
        messages.success(request, 'Record has been deleted successfully.')
    except Exception, e:
        messages.error(request, 'Failed to delete record. Reason: %s' % e, extra_tags='danger')
    return HttpResponseRedirect(reverse("internal:sales:index"))
