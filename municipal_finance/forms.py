from django import forms
from .models import FinancialPositionFactsV2
from municipal_finance.models.updates import ItemCodeSchema

class FinPosForm(forms.ModelForm):
    version = forms.ModelChoiceField(
        queryset=ItemCodeSchema.objects.all().values_list('version', flat=True),
        required=True,
        empty_label='Select a version'
    )
    class Meta:
        model = FinancialPositionFactsV2
        fields = '__all__'