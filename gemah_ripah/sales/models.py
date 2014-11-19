from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.dispatch import receiver

from products.models import Product


class Sales(models.Model):
    date = models.DateField()
    discount = models.DecimalField(max_digits=10, decimal_places=1, default=0, validators=[MinValueValidator(0)])
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ("-date", )

    def __str__(self):
        return "%s" % (self.date, )

    @property
    def gross_income(self):
        total_income = 0
        for item in self.salesitem_set.all():
            total_income += (item.price * item.quantity)

        return total_income

    @property
    def total_items(self):
        total_items = 0
        for item in self.salesitem_set.all():
            total_items += item.quantity

        return total_items

    @property
    def net_income(self):
        return self.gross_income - self.discount


class SalesItem(models.Model):
    sales = models.ForeignKey(Sales)
    product = models.ForeignKey(Product)
    price = models.DecimalField(max_digits=10, decimal_places=1, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ('product__name', )

    def __str__(self):
        return "%s: %d @ %f" % (self.product, self.quantity, self.price)


@receiver(models.signals.post_save, sender=SalesItem)
def on_save_callback(sender, **kwargs):
    update_total_sold(kwargs['instance'].product)


@receiver(models.signals.post_delete, sender=SalesItem)
def on_delete_callback(sender, **kwargs):
    update_total_sold(kwargs['instance'].product)


def update_total_sold(product):
    total = 0
    items = SalesItem.objects.filter(product=product)
    for item in items:
        total += item.quantity
    product.total_sold = total

    product.save()
