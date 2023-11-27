from django.shortcuts import render
from django.http import JsonResponse
from django_redis import get_redis_connection

from web.forms.account_form import RegisterModelForm, EmailVerifyForm, LoginEmailForm
from utils.SendMail import send_text_mail

from random import randrange


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    # 'POST'
    form = RegisterModelForm(data=request.POST)
    result = {'status': False, 'error': None}

    # Verify
    if not form.is_valid():
        error_list = list(form.errors.values())
        result['error'] = error_list[0]
    else:
        # Import new user's data into database.
        # instance = form.save()
        result['status'] = True
        result['data'] = '/login/'
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

    # send email
    mail_subject = 'Email address verification'
    mail_body = 'MP verification code: {}.\nIt will be expired in 3 minutes.'.format(verification_code)
    receiver_addr = [email, ]
    send_result = send_text_mail(receiver_addr, mail_subject, mail_body)
    if send_result.get('status'):
        result['status'] = True
        return JsonResponse(result)
    else:
        result['error'] = send_result['error']
        return JsonResponse(result)


def login_email(request):
    if request.method == 'GET':
        form = LoginEmailForm()
        return render(request, 'login_email.html', {'form': form})


def login_username(request):
    pass
