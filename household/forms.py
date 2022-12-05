from django import forms
from .models import DataSetFile

class UploadForm(forms.ModelForm):
    file_type = forms.ChoiceField(choices=(
        ('Service', 'Service Totals'),
        ('Bill', 'Bill Totals')
    ))

    class Meta:
        model = DataSetFile
        fields = ('csv_file', 'file_type')
