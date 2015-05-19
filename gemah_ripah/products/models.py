from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from gemah_ripah.models import CharUpperCaseField
from merchants.models import Merchant


class ProductManager(models.Manager):
    def active(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Product(models.Model):
    brand = CharUpperCaseField(max_length=100)
    name = CharUpperCaseField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=1, validators=[MinValueValidator(0)])
    total_purchased = models.IntegerField(default=0, editable=False)
    total_incoming = models.IntegerField(default=0, editable=False)
    total_sold = models.IntegerField(default=0, editable=False)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, blank=True, null=True, editable=False)

    objects = ProductManager()

    class Meta:
        ordering = ("name",)
        unique_together = ("brand", "name")

    def __str__(self):
        return self.name

    @property
    def stock(self):
        return self.total_purchased - self.total_sold

    def is_out_of_stock(self):
        if self.stock <= 0:
            return True
        return False


class ProductComparison(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True)
    seller = models.ForeignKey(Merchant)
    name = CharUpperCaseField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=1, validators=[MinValueValidator(0)])
    promotion_price = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True, validators=[MinValueValidator(0)])
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, blank=True, null=True, editable=False)

    class Meta:
        unique_together = ("seller", "name")

    def __str__(self):
        return "%s: %s: %s" % (self.seller, self.name, self.current_price)

    @property
    def current_price(self):
        if self.is_on_promotion():
            return self.promotion_price
        return self.price

    def is_on_promotion(self):
        if self.promotion_price and self.promotion_price > 0:
            return True
        return False


