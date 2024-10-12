from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django import forms

from users.models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    discord_username = forms.CharField(max_length=100, required=False, label="Discord Username")

    class Meta:
        model = User
        fields = ['username', 'discord_username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'email':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'id': 'floatingEmail',
                    'style': 'padding-left: 30px'
                })
            field.widget.attrs.update({'class': 'form-control'})

    def clean_discord_username(self):
        discord_username = self.cleaned_data.get('discord_username')
        if discord_username:
            discord_username = discord_username.lower()
            if UserProfile.objects.filter(discord_username=discord_username).exists():
                raise ValidationError("This Discord username is already in use.")
        return discord_username

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        if commit:
            user.save()
            discord_username = self.cleaned_data.get('discord_username')
            UserProfile.objects.create(user=user, discord_username=discord_username)
        return user


class CustomResetPasswordForm(PasswordResetForm):
    class Meta:
        models = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email Address"
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingEmail',
            'style': 'padding-left: 30px;'
        })


class CustomNewPassword(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class CustomPasswordResetView(PasswordResetView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('csgo')
        return super().dispatch(request, *args, **kwargs)
