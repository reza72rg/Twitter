from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from accounts.forms import UserRegisterForm
from accounts.models import Profile, User


# Custom Login View
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    # Redirect to success URL if user is already authenticated

    def get_success_url(self):
        return reverse_lazy("blog:home_page")
        # Redirect to the task list page after successful login


class RegisterPageView(CreateView):
    form_class = UserRegisterForm
    template_name = "accounts/register.html"

    def get_success_url(self):
        return reverse_lazy("accounts:login")
        # Redirect to the task list page after successful login

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("blog:home_page")
            # Redirect to the task list page if user is already authenticated
        return super(RegisterPageView, self).get(*args, **kwargs)


class CustomLogoutView(LoginRequiredMixin, View):
    login_url = "accounts/login.html"

    def get(self, request):
        logout(request)
        return redirect("accounts:logout_success")


class LogoutSuccessView(TemplateView):
    template_name = "accounts/logout.html"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = "accounts/profile.html"
    model = Profile
    fields = ["image", "descriptions", "active"]
    success_url = reverse_lazy("blog:home_page")

    def form_valid(self, form):
        value = self.request.POST["user"]
        user_email = self.request.POST["email"]
        username = get_object_or_404(User, username=self.request.user)
        username.username = value
        username.email = user_email
        username.save()
        return super(ProfileEditView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = User.objects.get(username=self.request.user.profile)
        return context
