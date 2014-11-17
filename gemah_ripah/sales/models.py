from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Sales(models.Model):
    date = models.DateField()
    discount = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ("-date", )

    def __str__(self):
        return "%s" % (self.date, )


class SalesItem(models.Model):
    sales = models.ForeignKey(Sales)
    product = models.ForeignKey(Product)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    quantity = models.IntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ('product__name', )

    def __str__(self):
        return "%s: %d @ %f" % (self.product, self.quantity, self.price)

