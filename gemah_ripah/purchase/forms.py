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
        choices = []
        group_member = [(None, "----------")]
        group_name = ""
        for product in Product.objects.values_list('id', 'name', 'is_active'):
            name = product[1] if product[2] else "(inactive) - %s" % product[1]
            if group_name != product[1].split()[0]:
                choices.append((group_name, group_member))
                group_member = []
                group_name = product[1].split()[0]
            group_member.append((product[0], name))
        self.fields["product"].choices = choices