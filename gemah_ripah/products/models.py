from django.db import models


class CharUpperCaseField(models.CharField):
    def get_prep_value(self, value):
        if not value:
            return value
        return value.upper()


class Brand(models.Model):
    name = CharUpperCaseField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey("Brand")
    name = CharUpperCaseField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    stock = models.IntegerField(default=0)

    class Meta:
        ordering = ("brand", "name")

    def __str__(self):
        return self.name

    def is_out_of_stock(self):
        if self.stock <= 0:
            return True
        return False


# class Transaction:
#     pass
#
# class BuyTransaction:
#     pass
#
# class SellTransaction:
#     pass
#
