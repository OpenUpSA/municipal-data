from django import forms
from .models import FinancialPositionFactsV2
from municipal_finance.models.updates import ItemCodeSchema


class FinPosForm(forms.ModelForm):
    version = forms.CharField(
        disabled=True,
        label="Schema version",
    )

    class Meta:
        model = FinancialPositionFactsV2
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(FinPosForm, self).__init__(*args, **kwargs)
        try:
            most_recent_version = ItemCodeSchema.objects.latest("id")
        except ItemCodeSchema.DoesNotExist:
            most_recent_version = ""
        self.fields["version"].initial = (
            most_recent_version.version if most_recent_version else ""
        )
