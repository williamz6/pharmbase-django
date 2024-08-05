from django import forms
from django.core.exceptions import ValidationError

def valid_quantity(quantity):
    if quantity <= 0:
        raise forms.ValidationError("Quantity must be a positive value")
    return quantity