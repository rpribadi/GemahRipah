from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.dispatch import receiver

from products.models import Product


class Sales(models.Model):
    date = models.DateField()
    discount = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    remarks = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ("-date", '-id')

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
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ('-sales__date', 'product__name', '-id')

    def __str__(self):
        return "%s: %d @ %f" % (self.product, self.quantity, self.price)


@receiver(models.signals.pre_save, sender=SalesItem)
def on_pre_save_callback(sender, **kwargs):
    update_pre_total_sold(kwargs['instance'])


@receiver(models.signals.post_save, sender=SalesItem)
def on_post_save_callback(sender, **kwargs):
    update_post_total_sold(kwargs['instance'])


@receiver(models.signals.post_delete, sender=SalesItem)
def on_post_delete_callback(sender, **kwargs):
    update_post_total_sold(kwargs['instance'])


def update_pre_total_sold(instance):
    if instance.id:
        old_instance = SalesItem.objects.get(pk=instance.id)
        if old_instance.product.id != instance.product.id:
            total = 0
            items = SalesItem.objects.filter(product=old_instance.product).exclude(pk=old_instance.id)
            for item in items:
                total += item.quantity
            old_instance.product.total_sold = total
            old_instance.product.save()


def update_post_total_sold(instance):
    total = 0
    items = SalesItem.objects.filter(product=instance.product)
    for item in items:
        total += item.quantity
    instance.product.total_sold = total

    instance.product.save()
