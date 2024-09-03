from django.shortcuts import redirect
from rest_framework.exceptions import NotAuthenticated


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, NotAuthenticated):
            return redirect("/login/")  # Redirect to your login URL
        return response
