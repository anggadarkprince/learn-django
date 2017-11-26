from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    email = forms.EmailField(label='Email address', max_length=50)
    subject = forms.CharField(label='Subject', max_length=100)
    message = forms.CharField(widget=forms.Textarea, label='Message', max_length=2000)
