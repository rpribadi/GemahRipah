from django import forms

from merchants.models import Merchant


class ComparisonForm(forms.Form):
    seller = forms.ModelChoiceField(label="Seller", queryset=Merchant.objects.filter(is_active=True))
    json = forms.CharField(label="JSON Data", widget=forms.Textarea)