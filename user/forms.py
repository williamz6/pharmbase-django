from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from backend.models import Drug, Order, OrderItem


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


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ["drug", "quantity"]
        drug = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))

    def __init__(self, *args, **kwargs):
        drug_name = kwargs.pop("drug_name",None)
        super(OrderItemForm, self).__init__(*args, **kwargs)
        if drug_name:
            self.fields['drug'].initial = drug_name
