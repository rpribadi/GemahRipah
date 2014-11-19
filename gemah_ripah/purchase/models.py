from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.dispatch import receiver

from products.models import Merchant, Product


class Purchase(models.Model):
    supplier = models.ForeignKey(Merchant)
    date = models.DateField()
    discount = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ("-date", )

    def __str__(self):
        return "%s: %s" % (self.date, self.supplier)

    @property
    def gross_expenses(self):
        total_expenses = 0
        for item in self.purchaseitem_set.all():
            total_expenses += (item.price * item.quantity)
        total_expenses -= self.discount

        return total_expenses

    @property
    def total_items(self):
        total_items = 0
        for item in self.purchaseitem_set.all():
            total_items += item.quantity

        return total_items

    @property
    def net_expenses(self):
        return self.gross_expenses - self.discount

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=1, validators=[MinValueValidator(0)])
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ('product__name', )

    def __str__(self):
        return "%s: %d @ %f" % (self.product, self.quantity, self.price)



@receiver(models.signals.post_save, sender=PurchaseItem)
def on_save_callback(sender, **kwargs):
    kwargs['instance'].product.total_purchased = get_total_purchased(kwargs['instance'].product)
    kwargs['instance'].product.save()

@receiver(models.signals.post_delete, sender=PurchaseItem)
def on_delete_callback(sender, **kwargs):
    kwargs['instance'].product.total_purchased = get_total_purchased(kwargs['instance'].product)
    kwargs['instance'].product.save()


def get_total_purchased(product):
    total = 0
    items = PurchaseItem.objects.filter(product=product)
    for item in items :
        total += item.quantity
    return total