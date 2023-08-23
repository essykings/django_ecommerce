from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields =  ['phone','street_address','city',
                'house_number','other']
        labels = {
            'other': 'Any other Instructions', 
        }