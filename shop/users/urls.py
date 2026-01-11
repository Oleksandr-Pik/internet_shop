from django.urls import path
from users.views import (
    HomeView,
    LoginView,
    RegisterView,
    ProfileView,
    ProfileEditView,
    LogoutView,
    EmailActivationView
)


urlpatterns = [
    path("", HomeView.as_view(), name="users"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "email/activate/<str:code>/",
        EmailActivationView.as_view(),
        name="email_activate",
    ),
]
