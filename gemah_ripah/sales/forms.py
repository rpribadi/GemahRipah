from django.forms import ModelForm

from models import Sales, SalesItem


class SalesForm(ModelForm):

    class Meta:
        model = Sales
        exclude = ()


class SalesItemForm(ModelForm):
    class Meta:
        model = SalesItem
        exclude = ()
