from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your username"
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )
    nickname = forms.CharField(
        min_length=3,
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your nickname"
        })
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password"
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Repeat your password"
        })
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control",
            "accept": "image/*"
        })
    )

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("confirm_password"):
            self.add_error("confirm_password", "Passwords do not match.")
        return data


# TODO: implement email login (take into account the uniqueness when updating the field)
class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your username"
        })
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password"
        })
    )


class ProfileEditForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter new username"
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter new email"
        })
    )
    nickname = forms.CharField(
        min_length=3,
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter new nickname"
        })
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control",
            "accept": "image/*"
        })
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            self.add_error('username', "This username is already occupied.")
        return username


class AskForm(forms.Form):
    title = forms.CharField(
        min_length=10,
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your question title"
        })
    )
    text = forms.CharField(
        required=False,
        max_length=3000,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Describe your question in detail...",
            "rows": 8,
            "style": "resize: none;"
        })
    )
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the tags separated by commas'
        })
    )


class AnswerForm(forms.Form):
    text = forms.CharField(
        max_length=3000,
        widget=forms.Textarea(attrs={
            "class": "form-control flex-grow-1",
            "placeholder": "Write your answer here...",
            "rows": 3,
            "style": "resize: none; overflow-y: auto;"
        })
    )
