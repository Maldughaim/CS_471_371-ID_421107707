from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="users.register"),
    path('login/', views.login_user, name="users.login_user"),
    path('logout/', views.logout_user, name="users.logout_user"),
]