# forecasting/forms.py
from django import forms
from .models import FinancialData

class FinancialDataForm(forms.ModelForm):
    class Meta:
        model = FinancialData
        fields = ['date', 'revenue', 'expenses', 'category', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }