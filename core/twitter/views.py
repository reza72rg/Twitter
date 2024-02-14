from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from twitter.models import Post, Like, DisLike
from accounts.models import User, Profile, Follow
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.


class PostListView(LoginRequiredMixin, ListView):
    template_name = 'twitter/home.html'
    ordering = ['-created_date']
    context_object_name = 'posts'
    paginate_by = 3
    def dispatch(self, request, *args, **kwargs):
        self.user_follow = Follow.objects.filter(user=self.request.user).values_list('follow_user', flat=True)
        self.follow_user = Follow.objects.filter(follow_user=self.request.user).values_list('user', flat=True)
        self.posts = Post.objects.filter(author__in=self.user_follow) | Post.objects.filter(author__in=self.follow_user) | Post.objects.filter(author=self.request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.posts

    def post(self, request, *args, **kwargs):
        q = request.POST.get('search')
        posts = self.posts.filter(content__icontains=q)
        context = {'posts': posts}
        return render(request, self.template_name, context)
    
    
    
    
    
        

class Aboutpage(View):
    template_name = 'twitter/about.html'
    def get(self, request, *args, **kwargs):
        return render (request , self.template_name)






class UserFollowListView(LoginRequiredMixin, ListView):
    template_name = 'twitter/home_follow.html'
    ordering = ['-created_date']
    context_object_name = 'posts'
    paginate_by = 3
    
    def dispatch(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['user_id'])
        self.relation = Follow.objects.filter(user=request.user, follow_user=self.user)
        self.posts = []
        self.can_follow = True
        if self.relation.exists() or self.user == self.request.user:
            self.can_follow = False
            self.posts = Post.objects.filter(author= self.user).order_by('-created_date')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.relation.exists():
            self.relation.delete()
        else:
            Follow(user=request.user, follow_user=self.user).save()
        return redirect('twitter:user-follows', self.user.id)
    def get_queryset(self):
        return self.posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['user'] = self.user
        context ["can_follow"] = self.can_follow
        return context
   
   
   
   
   
   
   
   

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
    
    


       
class FollowUserView(View):
    template_name = 'twitter/followuser.html'
    def post(self, request, *args, **kwargs):
        q =  request.POST.get('search')
        results = User.objects.filter(username__icontains=q)
        context = {
            'results':results
        }
        return render (request , self.template_name, context)


class LikePostView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.pk =kwargs['pk']
        self.like = Like.objects.filter(user = request.user, post_id = self.pk)
        self.can_like = True
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        if self.like.exists():
            can_like = False
        else:
            Like(user= request.user , post_id= self.pk).save()
        return redirect('/')
    
class DisLikePostView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.pk =kwargs['pk']
        self.dislike = DisLike.objects.filter(user = request.user, post_id = self.pk)
        self.can_dislike = True
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        if self.dislike.exists():
            can_dislike = False
        else:
            DisLike(user= request.user , post_id= self.pk).save()
        return redirect('/')