from django import forms
from .models import QuarterlySpendFile, AnnualSpendFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        models = QuarterlySpendFile
        fields = ("financial_year", "document")

class UploadAnnualFileForm(forms.ModelForm):
    class Meta:
        models = AnnualSpendFile
        fields = ("financial_year", "document")
