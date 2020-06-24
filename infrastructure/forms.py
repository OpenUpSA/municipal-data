from django import forms
from .models import QuarterlySpendFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        models = QuarterlySpendFile
        fields = ("financial_year", "document")
