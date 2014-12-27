from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from sales.models import Sales


class Member(models.Model):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    pin = models.CharField(max_length=255, editable=False)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    join_date = models.DateTimeField(auto_now_add=True, editable=False)
    points = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return "%s: %s" % (self.name, self.id)


class MemberRedeem(models.Model):
    member = models.ForeignKey(Member)
    sales = models.ForeignKey(Sales)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return "%s: %s" % (self.member, self.amount)

    def transaction_date(self):
        return self.sales.date
    transaction_date.admin_order_field = 'sales__date'
    transaction_date.short_description = 'Date'
