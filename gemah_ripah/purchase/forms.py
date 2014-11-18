from django.forms import ModelForm

from models import Purchase, PurchaseItem


class PurchaseForm(ModelForm):

    class Meta:
        model = Purchase


class PurchaseItemForm(ModelForm):
    class Meta:
        model = PurchaseItem
