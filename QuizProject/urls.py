from django.contrib import admin
from django.urls import path,include
from account import views as v
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',include('quiz.urls')),
    path('',include('account.urls')),
    path('register/', v.RegisterView.as_view(), name = "register"),
    path('admin/', admin.site.urls),

    path('password_reset/',auth_views.PasswordResetView.as_view(template_name = 'registration/password_reset_form_my.html'), name = "password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'registration/password_reset_done_my.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'registration/password_reset_confirm_my.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = 'registration/password_reset_complete_my.html'), name='password_reset_complete'),
    path('',include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
]
