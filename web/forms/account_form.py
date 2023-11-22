from django import forms
from django.core.validators import RegexValidator
from web import models


class RegisterModelForm(forms.ModelForm):
    user_name = forms.CharField(label='User Name',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    mobile_phone = forms.CharField(label='Mobile Phone',
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email Address',
                            validators=[RegexValidator(r'[a-zA-Z0-9_+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}',
                                                       'Email address format wrong.')],
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    verification_code = forms.CharField(label='Verification Code',
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.UserInfo
        fields = ['user_name', 'password', 'confirm_password', 'mobile_phone', 'email', 'verification_code']
