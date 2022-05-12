from .models import *
from django import forms
from django.forms import Form
from django.forms import fields

class BookInfoForm(forms.ModelForm):
    class Meta:
        model = Book_info
        fields=['ISBN','name','author','publisher','price','amount','is_active']

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock_bill
        fields=['book','price','amount']

class StockStatusForm(Form):
    pay = fields.BooleanField()
    send_back = fields.BooleanField()
    arrival = fields.BooleanField()
    
class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest_bill
        fields=['amount']