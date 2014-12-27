from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from forms import MemberForm
from models import Member
from sales.models import Sales, SalesItem


@login_required
def index(request):
    context = {
        'page_header': "Members",
        'page_title': "Members",
        'member_list': Member.objects.all()
    }

    return render(
        request,
        'members/index.html',
        context
    )


@login_required
def add(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, 'Record has been saved successfully.')
            return HttpResponseRedirect(reverse("internal:members:detail", kwargs={'id':obj.id}))
        else:
            messages.error(request, 'Failed to save record. Please correct the errors below.', extra_tags='danger')
    else:
        form = MemberForm()

    context = {
        'page_header': "Add New Member",
        'page_title': "Add New Member",
        'form': form
    }

    return render(
        request,
        'members/add.html',
        context
    )


@login_required
def detail(request, id):
    member = get_object_or_404(Member.objects.prefetch_related(
        models.Prefetch(
            'sales_set',
            queryset=Sales.objects.prefetch_related(
                models.Prefetch(
                    'salesitem_set',
                    queryset=SalesItem.objects.select_related('product')
                )
            )
        )
    ), pk=id)

    context = {
        'page_header': "Member Detail ID: %s" % id,
        'page_title': "Member Detail ID: %s" % id,
        'member': member
    }

    return render(
        request,
        'sales/detail.html',
        context
    )

