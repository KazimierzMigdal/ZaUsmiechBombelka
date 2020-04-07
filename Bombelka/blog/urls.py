from django.urls import path
from .views import (PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    CommentCreateView)
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='add_comment_to_post'),
    path('about/', views.about, name='blog-about'),
    path('likepost/', views.likePost, name='likepost'),
    path('post/<username>/', views.user_posts, name='user-posts'),
]
