from django import forms
from django.contrib.auth import get_user_model
from users.utils import send_activation_email
from users.models import ConfirmationCode, Profile
from django.conf import settings

User = get_user_model()


class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=150)
    password = forms.CharField()
    confirm_password = forms.CharField()

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get("email")).exists():
            raise forms.ValidationError("Користувач з таким email вже існує.")
        return self.cleaned_data.get("email")

    def clean_password(self):
        if len(self.cleaned_data.get("password")) < 8:
            raise forms.ValidationError("Пароль повинен містити щонайменше 8 символів.")
        return self.cleaned_data.get("password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Паролі не збігаються.")

    def save(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = User.objects.create_user(
            username=email, email=email, password=password, is_active=False
        )
        confirmation_code = ConfirmationCode.objects.create(user=user)
        
        send_activation_email(email, f'{settings.EMAIL_CONFIRMATION_LINK}{confirmation_code.code}/')
        
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150)
    password = forms.CharField()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "phone",
            "city",
            "address",
            # "avatar",
        )
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }
