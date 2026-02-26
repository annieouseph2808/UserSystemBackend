from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UsersView.as_view(), name="users"),
    path('users/<str:username>/', views.UserDetailView.as_view(), name="user_detail"),
]