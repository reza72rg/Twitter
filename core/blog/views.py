from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post, Like, DisLike, Comment
from accounts.models import User, Profile, Follow
from blog.forms import CommentForm, PostForm
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.


class PostListView(LoginRequiredMixin, ListView):
    template_name = 'blog/home.html'
    ordering = ['-created_date']
    context_object_name = 'posts'
    paginate_by = 3
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.user_follow = Follow.objects.filter(user=request.user.profile).values_list('follow_user', flat=True)
            self.posts = Post.objects.filter(author__in=self.user_follow, archive=True) | Post.objects.filter(author=request.user.profile, archive=True)
        else:
            self.posts = Post.objects.none()  # Empty queryset if user is not authenticated
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.posts

    def post(self, request, *args, **kwargs):
        q = request.POST.get('search')
        posts = self.posts.filter(content__icontains=q)
        context = {'posts': posts}
        return render(request, self.template_name, context)


class Aboutpage(LoginRequiredMixin, View):
    template_name = 'blog/about.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UserFollowListView(LoginRequiredMixin, ListView):
    template_name = 'blog/home_follow.html'
    ordering = ['-created_date']
    context_object_name = 'posts'
    paginate_by = 3
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.active:
            self.user = Profile.objects.get(user_id=kwargs['user_id'])
            self.relation = Follow.objects.filter(user=request.user.profile, follow_user=self.user)
            self.posts = []
            self.can_follow = True
            if self.relation.exists() or self.user == self.request.user.profile:
                self.can_follow = False
                self.posts = Post.objects.filter(author=self.user, archive=True).order_by('-created_date')
        else:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.relation.exists():
            self.relation.delete()
        else:
            Follow(user=request.user.profile, follow_user=self.user).save()
        return redirect('blog:user-follows', self.user.id)

    def get_queryset(self):
        return self.posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context["can_follow"]= self.can_follow
        return context
   

class FollowersView(LoginRequiredMixin, View):
    template_name = 'blog/follow.html'

    def dispatch(self, request, *args, **kwargs):
        self.follow = kwargs['letter']
        self.user = Profile.objects.get(user_id=kwargs['user_id'])
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
    form_class = PostForm
    template_name = 'blog/post_new.html'
    # fields = ["content", "image"]
    success_url = reverse_lazy("blog:home_page")

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(UserCreatePostView, self).form_valid(form)


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    context_object_name = "post"
    success_url = reverse_lazy("blog:home_page")


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_new.html'
    success_url = reverse_lazy("blog:home_page")

    def form_valid(self, form):
        return super().form_valid(form)


'''class DetailsPostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    form_class = CommentForm()
    def dispatch(self, request, *args, **kwargs):
        self.pk =kwargs['pk']
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post_id = self.pk,approach = True)
        return context
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(DetailsPostView, self).form_valid(form)

'''


class DetailsPostView(LoginRequiredMixin, View):
    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        self.posts = Post.objects.get(pk=self.pk, archive=True)
        self.comment = Comment.objects.filter(post_id=self.pk, approach=True)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'comments': self.comment, 'post': self.posts, "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) 
        if form.is_valid():
            endcomment = form.save(commit=False)
            endcomment.post = self.posts
            endcomment.author = request.user.profile
            endcomment.save()
        return redirect('blog:details_post', self.posts.pk)


class FollowUserView(View):
    template_name = 'blog/followuser.html'

    def post(self, request, *args, **kwargs):
        q = request.POST.get('search')
        results = Profile.objects.filter(user__username__icontains=q, active=True)
        print(results)
        context = {
            'results': results
        }
        return render(request, self.template_name, context)


class LikePostView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.pk =kwargs['pk']
        self.like = Like.objects.filter(user= request.user.profile, post_id=self.pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.like.exists():
            self.like.delete()
        else:
            Like(user=request.user.profile, post_id=self.pk).save()
        return redirect('/')


class DisLikePostView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.pk =kwargs['pk']
        self.dislike = DisLike.objects.filter(user=request.user.profile, post_id=self.pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.dislike.exists():
            self.dislike.delete()
        else:
            DisLike(user=request.user.profile, post_id=self.pk).save()
        return redirect('/')
