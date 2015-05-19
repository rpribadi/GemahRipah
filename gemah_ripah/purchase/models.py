from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.dispatch import receiver

from gemah_ripah.models import CharUpperCaseField
from merchants.models import Merchant
from products.models import Product


class Purchase(models.Model):
    supplier = models.ForeignKey(Merchant)
    date = models.DateField()
    other_expenses = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    remarks = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ("-date", "-id")

    def __str__(self):
        return "%s: %s" % (self.date, self.supplier)

    @property
    def product_expenses(self):
        if hasattr(self, '_product_expenses'):
            return self._product_expenses

        self._product_expenses = 0
        for item in self.purchaseitem_set.all():
            self._product_expenses += (item.price * item.quantity)

        return self._product_expenses

    @property
    def gross_expenses(self):
        return self.product_expenses + self.other_expenses

    @property
    def total_items(self):
        total_items = 0
        for item in self.purchaseitem_set.all():
            total_items += item.quantity

        return total_items

    @property
    def net_expenses(self):
        return self.gross_expenses - self.discount

    @property
    def estimated_revenues(self):
        if hasattr(self, '_estimated_revenues'):
            return self._estimated_revenues

        self._estimated_revenues = 0
        for item in self.purchaseitem_set.all().select_related('product'):
            self._estimated_revenues += (item.product.price * item.quantity)

        return self._estimated_revenues

    @property
    def estimated_profit(self):
        return self.estimated_revenues - self.net_expenses


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=1, validators=[MinValueValidator(0)])
    expiry_date = CharUpperCaseField(
        max_length=50,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]{3}[-]\d{4}$',
                message='Invalid format',
                code='invalid_expiry_date_format'
            ),
        ]
    )
    last_modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ('-purchase__date', 'product__name', '-id')

    def __str__(self):
        return "%s: %d @ %f" % (self.product, self.quantity, self.price)


@receiver(models.signals.post_save, sender=Purchase)
def on_post_save_purchase_callback(sender, **kwargs):
    for item in kwargs['instance'].purchaseitem_set.all():
        update_post_total_purchased(item.product)


@receiver(models.signals.pre_save, sender=PurchaseItem)
def on_pre_save_callback(sender, **kwargs):
    update_pre_total_purchased(kwargs['instance'])


@receiver(models.signals.post_save, sender=PurchaseItem)
def on_post_save_callback(sender, **kwargs):
    update_post_total_purchased(kwargs['instance'].product)


@receiver(models.signals.post_delete, sender=PurchaseItem)
def on_delete_callback(sender, **kwargs):
    update_post_total_purchased(kwargs['instance'].product)


def update_pre_total_purchased(instance):
    if instance.id:
        old_instance = PurchaseItem.objects.get(pk=instance.id)
        if old_instance.product.id != instance.product.id:
            total = 0
            items = PurchaseItem.objects.filter(product=old_instance.product, purchase__is_active=True).exclude(pk=old_instance.id)
            for item in items:
                total += item.quantity
            old_instance.product.total_purchased = total

            total = 0
            items = PurchaseItem.objects.filter(product=old_instance.product, purchase__is_active=False).exclude(pk=old_instance.id)
            for item in items:
                total += item.quantity
            old_instance.product.total_incoming = total

            old_instance.product.save()


def update_post_total_purchased(product):
    total = 0
    items = PurchaseItem.objects.filter(product=product, purchase__is_active=True)
    for item in items:
        total += item.quantity
    product.total_purchased = total

    total = 0
    items = PurchaseItem.objects.filter(product=product, purchase__is_active=False)
    for item in items:
        total += item.quantity
    product.total_incoming = total

    product.save()


