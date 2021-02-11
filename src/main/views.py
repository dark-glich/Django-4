from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView


class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'main/home.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 5

"""
class UserPostListView(ListView):
    model = Post
    template_name = 'main/user_post.html'
    context_object_name = 'posts'
    paginate_by = 50

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')
"""
def UserPostListView(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    if request.user == user:
        username = None
    else:
        username = user
    context = {'posts':posts, 'username':username}
    return render(request, 'main/user_post.html', context)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'main/update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'main/delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def HomeView(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request, 'main/home.html', context)

def AboutView(request):
    return render(request, 'main/about.html')
