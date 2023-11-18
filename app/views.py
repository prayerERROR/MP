from django.shortcuts import render, HttpResponse
from random import randrange
from utils.SendMail import send_text_mail

from django.core.validators import RegexValidator
from django import forms
from app import models


def email_verification(request):
    verification_code = randrange(10000, 99999)
    mail_subject = 'Email address verification'
    mail_body = 'MP verification code: {}.\nIt will expired in 3 minutes.'.format(verification_code)
    res = send_text_mail([], mail_subject, mail_body)
    if res.get('status'):
        return HttpResponse('Send mail verification code successfully.')
    else:
        return HttpResponse('Failed to send mail.\n' + str(res.get('error_info')))


class RegisterModelForm(forms.ModelForm):
    userName = forms.CharField(label='User Name',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email Address',
                            validators=[RegexValidator(r'[a-zA-Z0-9_+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}',
                                                       'Email address format wrong.')],
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobilePhone = forms.CharField(label='Mobile Phone',
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirmPassword = forms.CharField(label='Confirm Password',
                                      widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.UserInfo
        fields = '__all__'


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})
