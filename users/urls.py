from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomResetPasswordForm, CustomNewPassword, CustomPasswordResetView

urlpatterns = [
    path('register/', views.create_user, name='register'),
    path('login/', views.login_user, name='login'),
    # path('forgot-password', views.forgot_password, name='forgot_password'),
    path('reset_password/', CustomPasswordResetView.as_view(template_name="reset_password.html", form_class=CustomResetPasswordForm), name='reset_password'),
    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html", form_class=CustomResetPasswordForm), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html", form_class=CustomNewPassword), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name='password_reset_complete'),
]
