from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from twitter.models import Post
from accounts.models import User, Profile, Follow
from django.contrib import messages
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

class UserPostListView(LoginRequiredMixin, View):
    template_name = 'twitter/home_follow.html'

    def dispatch(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['user_id'])
        self.relation = Follow.objects.filter(user=request.user, follow_user=self.user)
        if self.user == request.user:
            messages.error(request, 'You can\'t follow/unfollow your own account', 'danger')
            return redirect('twitter:home_page')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.relation.exists():
            self.relation.delete()
        else:
            Follow(user=request.user, follow_user=self.user).save()
        return redirect('twitter:user-follows', self.user.id)

    def get(self, request, *args, **kwargs):
        if self.relation.exists():
            can_follow = False
        else:
            can_follow = True
        content = {'user': self.user, "can_follow": can_follow}
        return render(request, self.template_name, content)


class FollowersView(LoginRequiredMixin, View):
    template_name = 'twitter/follow.html'
    def dispatch(self, request, *args, **kwargs):
        self.follow =kwargs['letter']
        self.user = User.objects.get(pk=kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        if self.follow =='following':
            follows = Follow.objects.filter(user = self.user)
        elif self.follow =='followers':
            follows = Follow.objects.filter(follow_user = self.user)
        content = {'follows': follows, 'follow': self.follow}
        return render(request, self.template_name,content)
