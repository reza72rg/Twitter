from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from twitter.models import Post
from accounts.models import User, Profile, Follow
# Create your views here.



class PostListView(LoginRequiredMixin,ListView):
    template_name = 'twitter/home.html'
    model = Post
    
'''    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Status.objects.all()
        return context
'''
    
    
class Aboutpage(View):
    template_name = 'twitter/about.html'
    def get(self, request, *args, **kwargs):
        return render (request , self.template_name)


class UserPostListView(LoginRequiredMixin,View):
    template_name = 'twitter/home folllow.html'
   
    def get(self, request, *args, **kwargs):
        username = self.kwargs['username']
        user = User.objects.get(username = username)
    
        profile = Profile.objects.get(user = user)
        content = {'user':user,'profile':profile}
        return render (request , self.template_name, content)