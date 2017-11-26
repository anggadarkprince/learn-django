from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=30, required=True)
    email = forms.EmailField(label='Email address', max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', min_length=5, max_length=50, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', max_length=50, required=True)

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
