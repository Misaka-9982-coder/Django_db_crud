from django.contrib import admin
from django.urls import path, include  # add this


urlpatterns = [
    path('admin/', admin.site.urls),                # Django admin后台
    path("", include("apps.authentication.urls")),  # 用户登录注册管理
    path("", include("apps.home.urls")),            # 应用程序
]
