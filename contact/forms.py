from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from . import models


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Primeiro Nome",
            }
        ),
        label="Primeiro Nome",
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Segundo Nome",
            }
        ),
        label="Segundo Nome",
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Telefone",
            }
        ),
        label="Telefone",
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "E-mail",
            }
        ),
        label="E-mail",
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Digite uma descrição do contato",
            }
        ),
        label="Descrição",
    )
    category = forms.ModelChoiceField(
        queryset=models.CategoryModel.objects.all(),
        label="Categoria",
        empty_label="Selecione uma categoria",
    )

    picture = forms.ImageField(
        widget=forms.FileInput(attrs={"accept": "image/*"}), label="Foto"
    )

    class Meta:
        model = models.ContactModel
        fields = (
            "first_name",
            "last_name",
            "phone",
            "email",
            "description",
            "category",
            "picture",
        )


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            self.add_error(
                "email", ValidationError("E-mail ja cadastrado", code="invalid")
            )

        return email


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text="Required.",
        error_messages={"min_length": "Please, add more than 2 letters."},
    )
    last_name = forms.CharField(
        min_length=2, max_length=30, required=True, help_text="Required."
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Confirmar Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Use the same password as before.",
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)

        password = cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error("password2", ValidationError("Senhas devem ser iguais"))
        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        current_email = self.instance.email
        if email != current_email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    "email", ValidationError("E-mail ja cadastrado", code="invalid")
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error("password1", errors)
        return password1
