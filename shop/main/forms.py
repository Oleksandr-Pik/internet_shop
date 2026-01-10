from django import forms
from django.forms import ModelForm
from main.models import SiteReview, ProductReview


class SiteReviewForm(ModelForm):
    class Meta:
        model = SiteReview
        # fields = "__all__"
        fields = ["name", "rating", "text"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ваше ім'я"}
            ),
            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control rating",
                    "placeholder": "Ваша оцінка",
                    "min": "1",
                    "max": "5",
                }
            ),
            "text": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Ваш відгук"}
            ),
        }


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ["name", "text", "rating"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ваше ім'я"}
            ),
            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control rating",
                    "placeholder": "Ваша оцінка",
                    "min": "1",
                    "max": "5",
                }
            ),
            "text": forms.Textarea(
                attrs={"rows": 4, "class": "form-control", "placeholder": "Ваш відгук"}
            ),
        }
