from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from gemah_ripah.forms import MinimumRequiredFormSet
from forms import SalesForm, SalesItemForm
from models import Sales, SalesItem


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

@login_required
def add(request):
    SalesItemFormSet = inlineformset_factory(
        Sales,
        SalesItem,
        formset=MinimumRequiredFormSet,
        form=SalesItemForm
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
            messages.success(request, 'Record has been save successfully.')
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
        'form': form,
        'formset': formset
    }

    return render(
        request,
        'sales/add.html',
        context
    )


@login_required
def detail(request, id):
    sales = get_object_or_404(Sales, pk=id)

    context = {
        'page_header': "Sales Detail ID: %s" % id,
        'sales': sales
    }

    return render(
        request,
        'sales/detail.html',
        context
    )