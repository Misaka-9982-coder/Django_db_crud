
from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),               #登录
    path('register/', register_user, name="register"),      #注册
    path("logout/", LogoutView.as_view(), name="logout")    #登出
]
