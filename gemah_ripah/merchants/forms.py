from django.forms import ModelForm

from models import Merchant


class MerchantForm(ModelForm):

    class Meta:
        model = Merchant
        exclude = ()
