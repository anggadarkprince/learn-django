from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def about(request):
    return render(request, 'scene/about.html', {})
