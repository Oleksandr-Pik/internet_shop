from django import forms

def rating_validator(value):
    if value < 1 or value > 5:
        raise forms.ValidationError("Оцінка має бути від 1 до 5")