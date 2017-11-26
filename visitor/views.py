from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from .forms import ContactForm
from .models import Contact


@require_http_methods(["GET", "POST"])
def about(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipients = ['anggadarkprince@gmail.com']

            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save()
            if contact.pk is not None:
                try:
                    send_mail(subject, message, email, recipients)
                    messages.add_message(request, messages.SUCCESS, 'Your message successfully submitted.')
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            else:
                messages.add_message(request, messages.ERROR, 'Something went wrong.')

            # redirect to a new URL:
            return HttpResponseRedirect('/about')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, 'contact/about.html', {'form': form})
