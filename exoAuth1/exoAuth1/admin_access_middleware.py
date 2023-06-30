from django.shortcuts import redirect
from django.urls import reverse

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.path.startswith(reverse('admin:index')):
                return redirect(reverse('connexion'))
        else:
            if request.path.startswith(reverse('admin:index')):
                if not request.user.is_superuser:
                    return redirect(reverse('home'))

        response = self.get_response(request)
        return response
