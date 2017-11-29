from django import forms
from django.contrib.auth.hashers import check_password

from .models import User


class SettingsForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', max_length=50, required=True)
    last_name = forms.CharField(label='Last name', max_length=50)
    username = forms.CharField(label='Username', max_length=30, required=True)
    email = forms.EmailField(label='Email address', max_length=50, required=True)
    avatar = forms.ImageField(label='Avatar', required=False)
    about = forms.CharField(label='About', max_length=300, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, label='New password', max_length=50, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm password', max_length=50, required=False)
    hashed_password = ''
    id = 0

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'about', 'password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.id).count() > 0:
            raise forms.ValidationError(
                "This username was taken, try another"
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.id).count() > 0:
            raise forms.ValidationError(
                "This email was taken, try another"
            )
        return email

    def clean_password(self):
        current_password = self.cleaned_data.get('password')
        if not check_password(current_password, self.hashed_password):
            raise forms.ValidationError(
                "Your current password is wrong"
            )
        return current_password

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get("confirm_password")

        if new_password is not None:
            if new_password != confirm_password:
                raise forms.ValidationError(
                    "Your confirm password does not match"
                )

        return confirm_password


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=30, required=True)
    email = forms.EmailField(label='Email address', max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', min_length=5, max_length=50, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm password', max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        # additional cleaning here
        return cleaned_data

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Your confirm password does not match"
            )
        return confirm_password


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=50)
