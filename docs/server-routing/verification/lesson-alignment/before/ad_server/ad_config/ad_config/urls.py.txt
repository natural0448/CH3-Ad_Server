from django.contrib import admin
from django.contrib.auth import views as django_auth_views
from django.urls import include, path
from django.views.generic import RedirectView
from ads import auth_views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="login", permanent=False), name="home"),
    path("admin/", admin.site.urls),
    path("api/auth/csrf/", auth_views.csrf_token, name="csrf"),
    path("api/auth/login/", auth_views.login_view, name="api-login"),
    path("api/auth/logout/", auth_views.logout_view, name="api-logout"),
    path("accounts/login/", django_auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", django_auth_views.LogoutView.as_view(), name="logout"),
    path("", include("ads.urls")),
]
