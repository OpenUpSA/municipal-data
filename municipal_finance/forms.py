from django import forms
from .models import FinancialPositionFactsV2
from municipal_finance.models.updates import ItemCodeSchema


class FinPosForm(forms.ModelForm):
    try:
        most_recent_version = ItemCodeSchema.objects.latest("id")
    except ItemCodeSchema.DoesNotExist:
        most_recent_version = ""

    version = forms.CharField(
        initial=most_recent_version.version if most_recent_version else "",
        disabled=True,
        label="Schema version",
    )

    class Meta:
        model = FinancialPositionFactsV2
        fields = "__all__"
