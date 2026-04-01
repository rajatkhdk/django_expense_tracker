from django import forms
from .models import Expense, Category

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'description']

        # We add Bootstrap classes to make the form look like AdminLTE
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What did you buy?'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'catrgory' : forms.Select(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }