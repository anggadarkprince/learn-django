from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def login(request):
    return render(request, 'account/login.html', {})


@require_http_methods(["GET"])
def register(request):
    return render(request, 'account/register.html', {})


@require_http_methods(["GET"])
def profile(request, username):
    return render(request, 'account/profile.html', {'username': username})
