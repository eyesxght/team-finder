from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

from .models import User
from .validators import normalize_phone, validate_github_url


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError('Неверный имейл или пароль')
            self.user = user

        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise ValidationError('Телефон обязателен')

        normalized = normalize_phone(phone)
        qs = User.objects.filter(phone=normalized)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Этот номер телефона уже используется')
        return normalized

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        validate_github_url(url)
        return url


class ChangePasswordForm(PasswordChangeForm):
    pass
