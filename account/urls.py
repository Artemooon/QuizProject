from django.contrib.auth import views as v
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views



urlpatterns = [
    path('login/', views.LoginView.as_view(redirect_authenticated_user = True), name='login'),
    path('logout/', v.LogoutView.as_view(), name='logout'),
    path('settings/',views.AccountData.as_view(), name = "account_data"),
    path('profile/<slug:name>/', views.PublicProfile.as_view(), name = "user_profile"),
    path('profile/<slug:name>/stats/',views.ProfileStats.as_view(),name = "profile_stats"),
    path('login-warning/',views.LoginWarning.as_view(), name = "login_warning"),
    path('feedback/',views.Feedback.as_view(), name = "feedback"),
    path('register-success/<registerlink>/',views.SuccessfullyRegistered.as_view(), name = "successfully_registered")
]
