from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import (
    AuthenticationForm,
    UsernameField,
    UserCreationForm
)
from django.utils.timezone import make_aware

from manager.models import Worker, Position, Task, TaskType, Tag, Project


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
                "class": "transparent-input"
                ,"placeholder": "Username"
            }
        ),
    )
    password1 = forms.CharField(
        label="",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "transparent-text",
                "placeholder": "Password"
            }
        )
    )
    password2 = forms.CharField(
        label="",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "transparent-text",
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
                "class": "transparent-text",
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
                "class": "transparent-text",
            }
        )
    )
    email = forms.EmailField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "example@example.com",
                "class": "transparent-text",
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
                "class": "transparent-text",
                "value": "+",
            }
        )
    )
    location = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Location",
                "class": "transparent-text",
            }
        )
    )
    description = forms.CharField(
        required=False,
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Enter profile description",
                "class": "transparent-textarea",
            }
        )
    )
    profile_picture = forms.ImageField(
        required=False,
        label="",
        widget=forms.FileInput(
            attrs={
                "class": "transparent-input",
            }
        )
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        label="",
        widget=forms.Select(
            attrs={
                "class": "transparent-input",
            }
        )
    )
    instagram = forms.URLField(
        required=False,
        label="",
        widget=forms.URLInput(
            attrs={
                "class": "transparent-text",
                "placeholder": "https://www.instagram.com",
            }
        )
    )
    facebook = forms.URLField(
        required=False,
        label="",
        widget=forms.URLInput(
            attrs={
                "class": "transparent-text",
                "placeholder": "https://www.facebook.com",
            }
        )
    )
    twitter = forms.URLField(
        required=False,
        label="",
        widget=forms.URLInput(
            attrs={
                "class": "transparent-text",
                "placeholder": "https://www.twitter.com",
            }
        )
    )
    is_superuser = forms.BooleanField(
        required=False,
        label="Admin?",
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input border",
        })
    )
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
            "description",
            "location",
            "profile_picture",
            "phone_number",
            "twitter",
            "facebook",
            "instagram",
            "is_superuser",
        )

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        if password1 and len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters")
        if password1 and password1.isnumeric():
            raise forms.ValidationError("Password cannot contain only numbers")
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


class TaskForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control",
            }
        )
    )
    description = forms.CharField(
        required=False,
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Description",
                "class": "form-control",
            }
        )
    )
    deadline = forms.DateTimeField(
        required=False,
        label="",
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "type": "datetime-local",
            }
        )
    )
    priority = forms.IntegerField(
        required=False,
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Priority 1-5",
                "max": 5,
                "min": 1,
                "step": 1,
                "value": 3,
            }
        )
    )
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        required=False,
        label="",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
    )
    assigners = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        required=True,
        label="",
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select",
            }
        )
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label="",
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input",
            }
        )
    )
    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "assigners",
            "priority",
            "task_type",
            "tags"
        )

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')

        if deadline and deadline.tzinfo is None:
            deadline = make_aware(deadline)

        return deadline


class TaskProjectForm(TaskForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        label="",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "project",
            "tags"
        )
