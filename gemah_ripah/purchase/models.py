from django.contrib.auth.models import User
from django.db import models

from products.models import Merchant, Product


class Purchase(models.Model):
    supplier = models.ForeignKey(Merchant)
    date = models.DateField()
    discount = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ("-date", )

    def __str__(self):
        return "%s: %s" % (self.date, self.supplier)


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ('product__name', )

    def __str__(self):
        return "%s: %d @ %f" % (self.product, self.quantity, self.price)
