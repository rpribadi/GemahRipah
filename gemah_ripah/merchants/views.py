from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from forms import MerchantForm
from products.models import Merchant


@login_required
def index(request):
    context = {
        'page_header': "Merchants",
        'merchant_list': Merchant.objects.all()
    }

    return render(
        request,
        'merchants/index.html',
        context
    )


@login_required
def add_edit(request, id=None):
    obj = None
    if id:
        obj = get_object_or_404(Merchant, pk=id)

    if request.method == "POST":
        form = MerchantForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been saved successfully.')
            if id:
                return HttpResponseRedirect(reverse("merchants:index"))
            return HttpResponseRedirect(".")
        else:
            messages.error(request, 'Failed to save record. Please correct the errors below.', extra_tags='danger')
    else:
        form = MerchantForm(instance=obj)

    context = {
        'page_header': ("Edit Other Expenses ID: %s" % id) if id else "Add New Merchant",
        'form': form
    }

    return render(
        request,
        'merchants/add_edit.html',
        context
    )
