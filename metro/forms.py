from django import forms
from .models import FinancialYear, UpdateFile
from scorecard.models import Geography


class FinancialYearForm(forms.ModelForm):
    QUARTERS = (("", "-----"), ("Q1", "Q1"), ("Q2", "Q2"), ("Q3", "Q3"), ("Q4", "Q4"))
    quarter = forms.ChoiceField(
        choices=QUARTERS, help_text="Current quarter of the financial year"
    )

    class Meta:
        model = FinancialYear
        fields = "__all__"


class UpdateFileForm(forms.ModelForm):
    QUARTERS = (("", "-----"), ("Q1", "Q1"), ("Q2", "Q2"), ("Q3", "Q3"), ("Q4", "Q4"))
    quarter = forms.ChoiceField(
        choices=QUARTERS, help_text="Current quarter of the financial year"
    )
    geography = forms.ModelChoiceField(
        queryset=Geography.objects.filter(
            parent_level="province", geo_level="municipality"
        )
    )

    class Meta:
        model = UpdateFile
        fields = ("financial_year", "quarter", "geography", "document")
