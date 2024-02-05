from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth import REDIRECT_FIELD_NAME, logout as auth_logout
from django.views.generic import RedirectView
# Custom Login View
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
        # Redirect to success URL if user is already authenticated
    def get_success_url(self):
        return reverse_lazy('twitter:home_page')
        # Redirect to the task list page after successful login

class RegisterPageView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/register.html"
    def get_success_url(self):
        return reverse_lazy('accounts:login')
        # Redirect to the task list page after successful login
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("twitter:home_page")
            # Redirect to the task list page if user is already authenticated
        return super(RegisterPageView, self).get(*args, **kwargs)
    

class CustomLogoutView(RedirectView):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(CustomLogoutView, self).get(request, *args, **kwargs)
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('accounts:logout_success')
class LogoutSuccessView(TemplateView):
    template_name = 'accounts/logout.html'
