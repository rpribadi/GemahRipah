from django.db import models


class CharUpperCaseField(models.CharField):
    def get_prep_value(self, value):
        if not value:
            return value
        return value.upper()


class Product(models.Model):
    brand = CharUpperCaseField(max_length=100)
    name = CharUpperCaseField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    stock = models.IntegerField(default=0)

    class Meta:
        ordering = ("brand", "name")
        unique_together = ("brand", "name")

    def __str__(self):
        return self.name

    def is_out_of_stock(self):
        if self.stock <= 0:
            return True
        return False


class Comparison(models.Model):
    seller = CharUpperCaseField(max_length=100)
    product = CharUpperCaseField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    promotion_price = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "seller")

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


# class Transaction:
#     pass
#
# class BuyTransaction:
#     pass
#
# class SellTransaction:
#     pass
#
