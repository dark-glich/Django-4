from django.urls import path
from .views import (HomeView, AboutView,
                    PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView)

urlpatterns = [
    path('home/', PostListView.as_view(), name='home'),
    path('about/', AboutView, name='about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='delete'),
    path('user/<str:username>', UserPostListView, name='user-posts'),
    path('post/create/', PostCreateView.as_view(), name='create'),
]