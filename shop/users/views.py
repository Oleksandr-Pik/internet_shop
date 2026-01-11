from django.views.generic import TemplateView, View
from django.http import HttpRequest
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from typing import Literal
from main.base_views import BaseView
from users.forms import RegisterForm, LoginForm, ProfileForm
from users.models import ConfirmationCode, Profile
from users.utils import merge_cart_to_user


class AuthTemplateView(TemplateView):
    required_user_type: Literal["logged_in", "any", "anonymous"] = "any"

    def _get_page_name(self, **kwargs):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_name"] = self._get_page_name(**kwargs)

        return context

    def _get_user_type(self, request: HttpRequest) -> Literal["logged_in", "anonymous"]:
        if request.user.is_authenticated:
            return "logged_in"
        return "anonymous"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        user_type = self._get_user_type(request)
        if self.required_user_type == "logged_in" and user_type == "anonymous":
            return redirect("login")
        if self.required_user_type == "anonymous" and user_type == "logged_in":
            return redirect("profile")  # or "users""
        return super().dispatch(request, *args, **kwargs)


class HomeView(AuthTemplateView):
    template_name = "users/home.html"
    required_user_type = "any"


class LoginView(AuthTemplateView, BaseView):
    template_name = "users/login.html"
    required_user_type = "anonymous"

    def _get_page_name(self, **kwargs):
        return "Авторизація користувача"

    def _get_user(self, cleaned_data):
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        user = authenticate(username=email, password=password)
        return user

    def post(self, request: HttpRequest, *args, **kwargs): 
        form = LoginForm(request.POST)
        if form.is_valid():
            user = self._get_user(form.cleaned_data)
            if user is not None:
                login(request, user)
                merge_cart_to_user(request)
                return redirect("catalog")
            else:
                form.add_error(None, "Невірний email або пароль.")
        return self.render_to_response(self.get_context_data(form=form))


class RegisterView(AuthTemplateView, BaseView):
    template_name = "users/register.html"
    required_user_type = "anonymous"

    def _get_page_name(self, **kwargs):
        return "Реєстрація користувача"

    def post(self, request: HttpRequest, *args, **kwargs): 
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return self.render_to_response(self.get_context_data(form=form))


class ProfileView(AuthTemplateView, BaseView):
    template_name = "users/profile.html"
    required_user_type = "logged_in"

    def _get_page_name(self, **kwargs):
        return "Профіль користувача"

    def get_profile(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context["profile"] = profile
        context["form"] = ProfileForm(instance=profile)
        return context

    def post(self, request, *args, **kwargs):
        profile = self.get_profile()
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class ProfileEditView(AuthTemplateView, BaseView):
    template_name = "users/edit-profile.html"
    required_user_type = "logged_in"

    def _get_page_name(self, **kwargs):
        return "Редагування профілю"

    def get_profile(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context["profile"] = profile
        context["form"] = ProfileForm(instance=profile)
        context["page_name"] = self._get_page_name()
        return context

    def post(self, request, *args, **kwargs):
        profile = self.get_profile()
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class LogoutView(AuthTemplateView):
    template_name = "users/logout.html"
    required_user_type = "logged_in"

    def get(self, request: HttpRequest, *args, **kwargs): 
        logout(request)
        return redirect("login")


class EmailActivationView(View):    
    def get(self, request: HttpRequest, code: str, *args, **kwargs):
        user = ConfirmationCode.process_code(code)
        if user:
            login(request, user)
            merge_cart_to_user(request)
            return redirect("home")
        return redirect("login")


class PasswordResetView(AuthTemplateView):
    template_name = "users/password_reset.html"
    required_user_type = "anonymous"


class PasswordChangeView(AuthTemplateView):
    template_name = "users/password_change.html"
    required_user_type = "logged_in"


class PasswordResetDoneView(AuthTemplateView):
    template_name = "users/password_reset_done.html"
    required_user_type = "anonymous"
