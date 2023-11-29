from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django_redis import get_redis_connection

from web.forms.account_form import RegisterModelForm, EmailVerifyForm, LoginEmailForm, LoginUsernameForm
from web import models
from utils.SendMail import send_text_mail
from utils.ImageCode import generate_image_code

from random import randrange
from io import BytesIO


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    # POST
    form = RegisterModelForm(data=request.POST)
    result = {'status': False, 'error': None, 'data': None}

    # Verify
    if form.is_valid():
        # Import new user's data into database.
        # instance = form.save()
        result['status'] = True
        result['data'] = '/login/'
    else:
        error_list = list(form.errors.values())
        result['error'] = error_list[0]
    return JsonResponse(result)


def email_verify(request):
    form = EmailVerifyForm(data=request.GET)
    email = request.GET.get('email')
    result = {'status': False, 'error': None}

    # verify
    if not form.is_valid():
        result['error'] = form.errors['email'][0]
        return JsonResponse(result)

    # generate verification code
    verification_code = randrange(1000, 9999)
    conn = get_redis_connection()
    conn.set(email, verification_code, ex=180)

    print(verification_code)
    result['status'] = True
    return JsonResponse(result)

    # send email
    mail_subject = 'Email address verification'
    mail_body = 'Verification code for MP: {}.\nIt will be expired in 3 minutes.'.format(verification_code)
    receiver_addr = [email, ]
    send_result = send_text_mail(receiver_addr, mail_subject, mail_body)
    if send_result.get('status'):
        result['status'] = True
    else:
        result['error'] = send_result['error']
    return JsonResponse(result)


def login_email(request):
    # log in with email and email verification
    if request.method == 'GET':
        form = LoginEmailForm()
        return render(request, 'login_email.html', {'form': form})

    # 'POST'
    form = LoginEmailForm(data=request.POST)
    result = {'status': False, 'error': None, 'data': None}

    # Verify
    if form.is_valid():
        email = form.cleaned_data['email']
        user = models.UserInfo.objects.filter(email=email).first()
        request.session['user_id'] = user.id
        request.session['user_username'] = user.username

        result['status'] = True
        result['data'] = '/index/'
    else:
        error_list = list(form.errors.values())
        result['error'] = error_list[0]
    return JsonResponse(result)


def login_username(request):
    # log in with username and password
    if request.method == 'GET':
        form = LoginUsernameForm()
        return render(request, 'login_username.html', {'form': form})


def image_verify(request):
    img, code = generate_image_code()
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())
