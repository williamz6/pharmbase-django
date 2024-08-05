from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from backend.models import Drug, Order, OrderItem
from django.forms.models import inlineformset_factory

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control my-2  "})
            field.label = mark_safe(f"<b>{field.label}</b>")

    def clean_email(self):
        try:
            email = self.cleaned_data.get("email")
            qs = User.objects.filter(email=email)

            if qs.exists():
                raise ValidationError("Email already registered")
        except:
            raise forms.ValidationError("Email already registered")
        return email


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["username", "email", "firstName", "lastName"]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = []

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['drug', 'quantity'] 

    def clean_quantity(self):
        quantity= self.cleaned_data.get('quantity')
        drug= self.cleaned_data.get('drug')

        if quantity <= 0:
            raise forms.ValidationError('Quantity must be a positive integer')
        
        if drug and quantity > drug.stock_quantity:
            raise forms.ValidationError(f'Only {drug.stock_quantity} items available in stock')
        
        return quantity
