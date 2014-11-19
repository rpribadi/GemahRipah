from django.forms import ModelForm

from models import OtherExpenses


class OtherExpensesForm(ModelForm):

    class Meta:
        model = OtherExpenses
        exclude = ()
