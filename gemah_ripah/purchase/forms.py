from django.forms import ModelForm

from products.models import Product

from models import Purchase, PurchaseItem


class PurchaseForm(ModelForm):

    class Meta:
        model = Purchase
        exclude = ()


class PurchaseItemForm(ModelForm):
    class Meta:
        model = PurchaseItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(PurchaseItemForm, self).__init__(*args, **kwargs)

        # get different list of choices here
        choices = [(None, "----------")]
        for product in Product.objects.values_list('id', 'name', 'is_active'):
            name = product[1] if product[2] else "(inactive) - %s" % product[1]
            choices.append((product[0], name))
        self.fields["product"].choices = choices