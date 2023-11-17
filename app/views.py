from django.shortcuts import render
from django.core.validators import RegexValidator
from django import forms
from app import models


class RegisterModelForm(forms.ModelForm):
    userName = forms.CharField(label='User Name',
                               widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(label='Email Address',
                            validators=[RegexValidator(r'[a-zA-Z0-9_+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}',
                                                       'Email address format wrong.')],
                            widget=forms.TextInput(attrs={'class':'form-control'}))
    mobilePhone = forms.CharField(label='Mobile Phone',
                                  widget=forms.NumberInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirmPassword = forms.CharField(label='Confirm Password',
                                      widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = models.UserInfo
        fields = '__all__'


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})
