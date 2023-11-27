from django import forms
from django.core.exceptions import ValidationError
from django_redis import get_redis_connection

from utils.Encrypt import md5
from web import models


class RegisterModelForm(forms.ModelForm):
    username = forms.CharField(label='Username',
                               max_length=32,
                               min_length=4,
                               error_messages={
                                   'required': 'Creat your user name.',
                                   'min_length': 'User name is too short.',
                                   'max_length': 'User name is too long.',
                               },
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',
                               max_length=32,
                               min_length=8,
                               error_messages={
                                   'required': 'Set your password.',
                                   'min_length': 'Password is too short.',
                                   'max_length': 'Password is too long',
                               },
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password',
                                       error_messages={
                                           'required': 'Repeat your password'
                                       },
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    mobile_phone = forms.CharField(label='Mobile Phone',
                                   max_length=16,
                                   error_messages={
                                       'required': 'Enter your mobile phone number.',
                                       'max_length': 'Enter a valid phone number',
                                   },
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email Address',
                             max_length=32,
                             error_messages={
                                 'required': 'Enter your email address.',
                                 'max_length': 'Email address is too long',
                             },
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    verification_code = forms.CharField(label='Verification Code',
                                        max_length=16,
                                        error_messages={
                                            'required': 'Enter your verification code.',
                                            'max_length': 'Wrong verification code.',
                                        },
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 'confirm_password', 'mobile_phone', 'email', 'verification_code']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if models.UserInfo.objects.filter(username=username).exists():
            raise ValidationError('Username already existed.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password = md5(password)
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        # If password is invalid, quit clean function.
        if not password:
            return confirm_password

        # Check if password matches confirm_password.
        confirm_password = md5(confirm_password)
        if password != confirm_password:
            raise ValidationError('Passwords do not match.')
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if models.UserInfo.objects.filter(email=email).exists():
            raise ValidationError('Email address already existed.')
        return email

    def clean_verification_code(self):
        email = self.cleaned_data.get('email')
        verification_code = self.cleaned_data.get('verification_code')

        # If email address is invalid, quit clean function.
        if not email:
            return verification_code

        # Check the verification code stored in redis pool.
        conn = get_redis_connection()
        redis_code = conn.get(email)
        if not redis_code:
            raise ValidationError('Verification code is invalid or not sent.')
        redis_code = redis_code.decode('utf-8')
        if redis_code != verification_code:
            raise ValidationError('Wrong verification code.')
        return verification_code


class EmailVerifyForm(forms.Form):
    email = forms.EmailField(label='Email Address',
                             max_length=32,
                             error_messages={
                                 'required': 'Enter your email address.',
                                 'max_length': 'Email address is too long',
                             })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if models.UserInfo.objects.filter(email=email).exists():
            raise ValidationError('Email address already existed.')
        return email


class LoginEmailForm(forms.Form):
    email = forms.EmailField(label='Email Address',
                             max_length=32,
                             error_messages={
                                 'required': 'Enter your email address.',
                                 'max_length': 'Email address is too long',
                             },
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    verification_code = forms.CharField(label='Verification Code',
                                        max_length=16,
                                        error_messages={
                                            'required': 'Enter your verification code.',
                                            'max_length': 'Wrong verification code.',
                                        },
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not models.UserInfo.objects.filter(email=email).exists():
            raise ValidationError('Email address does not exist.')
        return email

    def clean_verification_code(self):
        email = self.cleaned_data.get('email')
        verification_code = self.cleaned_data.get('verification_code')

        # If email address is invalid, quit clean function.
        if not email:
            return verification_code

        # Check the verification code stored in redis pool.
        conn = get_redis_connection()
        redis_code = conn.get(email)
        if not redis_code:
            raise ValidationError('Verification code is invalid or not sent.')
        redis_code = redis_code.decode('utf-8')
        if redis_code != verification_code:
            raise ValidationError('Wrong verification code.')
        return verification_code
