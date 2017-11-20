from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def index(request):
    return render(request, 'scene/index.html', {})


@require_http_methods(["GET"])
def agreement(request):
    return render(request, 'scene/agreement.html', {})


@require_http_methods(["GET"])
def privacy(request):
    return render(request, 'scene/privacy.html', {})


@require_http_methods(["GET", "POST"])
def about(request):
    return render(request, 'scene/about.html', {})
