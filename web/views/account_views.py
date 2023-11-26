from django.shortcuts import render
from django.http import JsonResponse
from django_redis import get_redis_connection

from web.forms.account_form import RegisterModelForm, VerifyEmailForm
from utils.SendMail import send_text_mail
from utils.Encrypt import md5

from random import randrange


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    else:
        form = RegisterModelForm(data=request.POST)
        result = {'status': False, 'error': None}

    # Verify
    if not form.is_valid():
        error_list = list(form.errors.values())
        result['error'] = error_list[0]
        return JsonResponse(result)
    else:
        # Import new user's data into database.
        form.instance.password = md5(form.cleaned_data['password'])
        instance = form.save()
        result['status'] = True
        return JsonResponse(result)


def register_verify_email(request):
    form = VerifyEmailForm(data=request.GET)
    new_email = request.GET.get('email')
    result = {'status': False, 'error': None}

    # verify
    if not form.is_valid():
        result['error'] = form.errors['email']
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
        result['error'] = send_result['error']
        return JsonResponse(result)
