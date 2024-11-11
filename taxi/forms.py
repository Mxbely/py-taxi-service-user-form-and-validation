from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car

from django.contrib.auth.forms import UserCreationForm


def update_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number must be 8 characters long")
    if (
        license_number[:3].isalpha() is False
        or license_number[:3].upper() != license_number[:3]
    ):
        raise ValidationError(
            "License number must start with 3 uppercase letters"
        )
    if license_number[3:].isdigit() is False:
        raise ValidationError("License number must end with 5 digits")
    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=255,
        validators=[
            update_license_number,
        ],
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
