from django.shortcuts import render
from django.http import JsonResponse
from django_redis import get_redis_connection

from web.forms.account_form import RegisterModelForm
from web.models import UserInfo
from utils.SendMail import send_text_mail

from random import randrange
from re import fullmatch


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})


def register_verify_email(request):
    new_email = request.GET.get('email')
    result = {'status': False, 'error': None}

    # check email address format
    pattern = r'[a-zA-Z0-9_+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}'
    if not fullmatch(pattern, new_email):
        result['error'] = 'Invalid email address format.'
        return JsonResponse(result)

    # check if registered
    if UserInfo.objects.filter(email=new_email):
        result['error'] = 'The email address has been registered.'
        return JsonResponse(result)

    # generate verification code
    verification_code = randrange(1000, 9999)
    conn = get_redis_connection()
    conn.set(new_email, verification_code, ex=180)

    # send email
    mail_subject = 'Email address verification'
    mail_body = 'MP verification code: {}.\nIt will be expired in 3 minutes.'.format(verification_code)
    receiver_addr = [new_email, ]
    send_result = send_text_mail(receiver_addr, mail_subject, mail_body)
    if send_result.get('status'):
        result['status'] = True
        return JsonResponse(result)
    else:
        result['error'] = send_result['error_info']
        return JsonResponse(result)
