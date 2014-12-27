from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from forms import OtherExpensesForm
from models import OtherExpenses


@login_required
def index(request):
    context = {
        'page_header': "Other Expenses",
        'page_title': "Other Expenses",
        'other_expenses_list': OtherExpenses.objects.all()
    }

    return render(
        request,
        'other_expenses/index.html',
        context
    )


@login_required
def add_edit(request, id=None):
    obj = None
    if id:
        obj = get_object_or_404(OtherExpenses, pk=id)

    if request.method == "POST":
        form = OtherExpensesForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been saved successfully.')
            if id:
                return HttpResponseRedirect(reverse("internal:other_expenses:index"))
            return HttpResponseRedirect(".")
        else:
            messages.error(request, 'Failed to save record. Please correct the errors below.', extra_tags='danger')
    else:
        form = OtherExpensesForm(instance=obj)

    context = {
        'page_header': ("Edit Other Expenses ID: %s" % id) if id else "Add New Other Expenses",
        'page_title': ("Edit Other Expenses ID: %s" % id) if id else "Add New Other Expenses",
        'form': form
    }

    return render(
        request,
        'other_expenses/add_edit.html',
        context
    )


@login_required
def delete(request, id):
    obj = get_object_or_404(OtherExpenses, pk=id)
    try:
        obj.delete()
        messages.success(request, 'Record has been deleted successfully.')
    except Exception, e:
        messages.error(request, 'Failed to delete record. Reason: %s' % e, extra_tags='danger')
    return HttpResponseRedirect(reverse("internal:other_expenses:index"))
