from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import ValidationError
from django.shortcuts import redirect


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


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
