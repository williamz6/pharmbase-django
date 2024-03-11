from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

    def clean_email(self):
        try:
            email = self.cleaned_data.get("email")
            qs = User.objects.filter(email=email)

            if qs.exists() :
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
