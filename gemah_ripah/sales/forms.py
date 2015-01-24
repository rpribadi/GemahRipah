from django.forms import ModelForm

from products.models import Product

from models import Sales, SalesItem


class SalesForm(ModelForm):

    class Meta:
        model = Sales
        exclude = ()


class SalesItemForm(ModelForm):
    class Meta:
        model = SalesItem
        exclude = ()


    def __init__(self, *args, **kwargs):
        super(SalesItemForm, self).__init__(*args, **kwargs)

        # get different list of choices here
        choices = [(None, "----------")]
        for product in Product.objects.values_list('id', 'name', 'is_active'):
            name = product[1] if product[2] else "(inactive) - %s" % product[1]
            choices.append((product[0], name))
        self.fields["product"].choices = choices