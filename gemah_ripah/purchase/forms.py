from django.forms import ModelForm

from models import Purchase, PurchaseItem


class PurchaseForm(ModelForm):

    class Meta:
        model = Purchase
        exclude = ()


class PurchaseItemForm(ModelForm):
    class Meta:
        model = PurchaseItem
        exclude = ()
