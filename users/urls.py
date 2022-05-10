from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_userdata, name='user-data'),
    path('register/', views.RegisterView.as_view(), name='user-register'),
    path('login/', views.LoginView.as_view(), name='user-login'),
    path('logout/', views.LogoutView.as_view(), name='user-logout'),
    path('is-verified/', views.is_verified_user, name='user-verification-status'),
    path('verify-email/', views.VerifyEmail.as_view(), name='user-verify'),
]
