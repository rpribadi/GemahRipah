from django.forms import ModelForm

from products.models import Merchant


class MerchantForm(ModelForm):

    class Meta:
        model = Merchant
        exclude = ()
