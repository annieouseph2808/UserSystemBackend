from django.urls import path
from . import views
urlpatterns = [
    path('users/add',views.add_user,name="add_user"),
    path('users/delete',views.delete_user,name="remove_user"),
    path('users/reactivate',views.reactivate_user,name="reactivate_user"),
    path('users/view',views.view_users,name="view_users"),
]
