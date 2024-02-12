from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from accounts.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Custom Login View
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
        # Redirect to success URL if user is already authenticated
    def get_success_url(self):
        return reverse_lazy('twitter:home_page')
        # Redirect to the task list page after successful login

class RegisterPageView(CreateView):
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    def get_success_url(self):
        return reverse_lazy('accounts:login')
        # Redirect to the task list page after successful login
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("twitter:home_page")
            # Redirect to the task list page if user is already authenticated
        return super(RegisterPageView, self).get(*args, **kwargs)
    
class CustomLogoutView(LoginRequiredMixin, View):
    login_url = 'accounts/login.html'  
    def get(self,request):
        logout(request)
        return redirect('accounts:logout_success')

class LogoutSuccessView(TemplateView):
    template_name = 'accounts/logout.html'

class ProfileView(LoginRequiredMixin, View):
    form_class = UserUpdateForm
    template_name = 'accounts/profile.html'
    second_form_class = ProfileUpdateForm
    
    def get(self, request, *args, **kwargs):
        uform = self.form_class(instance=request.user)
        pform = self.second_form_class(instance=request.user.profile)
        content = {'uform':uform,'pform':pform}
        return render (request , self.template_name,content)
    def post(self, request, *args, **kwargs):
        uform = self.form_class(request.POST, instance=request.user) 
        pform = self.second_form_class(request.POST, request.FILES, instance=request.user.profile) 
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save() 
            return redirect('/')
        content = {'uform':uform,'pform':pform}
        return render (request , self.template_name,content)
       
