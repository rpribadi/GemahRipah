from django.contrib.auth.models import User
from django.db import models

from gemah_ripah.models import CharUpperCaseField


class Merchant(models.Model):
    code = CharUpperCaseField(max_length=2, unique=True)
    name = CharUpperCaseField(max_length=50, unique=True)

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = CharUpperCaseField(max_length=100)
    name = CharUpperCaseField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    stock = models.IntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, null=True)

    class Meta:
        ordering = ("brand", "name")
        unique_together = ("brand", "name")

    def __str__(self):
        return self.name

    def is_out_of_stock(self):
        if self.stock <= 0:
            return True
        return False


class ProductComparison(models.Model):
    product = models.ForeignKey(Product, null=True)
    seller = models.ForeignKey(Merchant)
    name = CharUpperCaseField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    promotion_price = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, null=True)

    class Meta:
        unique_together = ("seller", "name")

    def __str__(self):
        return "%s: %s: %s" % (self.seller, self.product, self.current_price)

    @property
    def current_price(self):
        if self.is_on_promotion():
            return self.promotion_price
        return self.price

    def is_on_promotion(self):
        if self.promotion_price and self.promotion_price > 0:
            return True
        return False


