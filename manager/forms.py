from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import (
    AuthenticationForm,
    UsernameField,
    UserCreationForm,
)

from manager.models import Worker, Position


class LoginForm(AuthenticationForm):
  username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  password = forms.CharField(
      label="Password",
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
  )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username",
                "class": "form-control search-input",
            }
        ),
    )


class WorkerForm(ModelForm):
    username = UsernameField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs=
            {
                "class": "form-control"
                ,"placeholder": "Username"
            }
        ),
    )
    password1 = forms.CharField(
        label="",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            }
        )
    )
    password2 = forms.CharField(
        label="",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password confirmation"
            }
        )
    )
    first_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "form-control",
            }
        )
    )
    last_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "class": "form-control",
            }
        )
    )
    email = forms.EmailField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
            }
        )
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "+",
                "class": "form-control",
                "value": "+",
            }
        )
    )
    description = forms.CharField(
        required=False,
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Enter profile description",
                "class": "form-control",
            }
        )
    )
    profile_picture = forms.ImageField(
        required=False,
        label="",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        label="",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
    )
    instagram = forms.URLField(
        required=False,
        label="",
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": "https://www.instagram.com",
            }
        )
    )
    facebook = forms.URLField(
        required=False,
        label="",
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": "https://www.facebook.com",
            }
        )
    )
    twitter = forms.URLField(
        required=False,
        label="",
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": "https://www.twitter.com",
            }
        )
    )
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
            "description",
            "profile_picture",
            "phone_number",
        )

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def clean_phone_number(self) -> str:
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number:
            phone_number = phone_number.strip("+ ")
        return phone_number

    def save(self, commit=True):
        user = super(WorkerForm, self).save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name",
                "class": "form-control",
            }
        ),
    )