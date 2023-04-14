from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"
urlpatterns = [
    path('login/', views.login_form_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('otp/', views.otp_message_view, name="otp"),
    path("resend/", views.resend_message, name="resend"),
    path('logout/', views.logout_view, name="logout"),
    path('reset-password/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
