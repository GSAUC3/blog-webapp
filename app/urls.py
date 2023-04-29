from django.urls import path,include
from . import views



urlpatterns = [
    path('', views.PostListView.as_view(),name='home'),
    path('user/str:<username>', views.UserPostListView.as_view(),name='user-post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(),name='post-detail'),
    path('post/new', views.PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(),name='post-delete'),
    path('about/', views.about,name='about'),
    path('register/', views.register,name='register'),
    path('profile/', views.profile,name='profile'),
]