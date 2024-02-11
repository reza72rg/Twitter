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
from django.urls import reverse_lazy
# Create your views here.



class PostListView(LoginRequiredMixin,ListView):
    template_name = 'twitter/home.html'
    model = Post
    context_object_name = "posts"
    ordering = ['-created_date']
    def get_queryset(self):
        queryset = super().get_queryset()
        user_follow = Follow.objects.filter(user=self.request.user).values_list('follow_user', flat=True)
        follow_user = Follow.objects.filter(follow_user=self.request.user).values_list('user', flat=True)
        posts = queryset.filter(author__in=user_follow) | queryset.filter(author__in=follow_user) | queryset.filter(author=self.request.user)
        return posts
    
class Aboutpage(View):
    template_name = 'twitter/about.html'
    def get(self, request, *args, **kwargs):
        return render (request , self.template_name)

class UserFollowListView(LoginRequiredMixin, View):
    template_name = 'twitter/home_follow.html'
    ordering = ['-created_date']
    def dispatch(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['user_id'])
        self.relation = Follow.objects.filter(user=request.user, follow_user=self.user)
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
        posts = Post.objects.filter(author= self.user).order_by('-created_date')
        content = {'user': self.user, "can_follow": can_follow, 'posts':posts}
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



class UserCreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'twitter/post_new.html'
    fields = ["content"]
    success_url = reverse_lazy("twitter:home_page")

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(UserCreatePostView, self).form_valid(form)


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'twitter/post_delete.html'
    context_object_name = "post"
    success_url = reverse_lazy("twitter:home_page")


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["content"]
    success_url = reverse_lazy("twitter:home_page")
    def form_valid(self, form):
        return super(UpdatePostView, self).form_valid(form)


class DetailsPostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'twitter/post_detail.html'