import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from django.conf import settings

smtp_server = settings.smtp_server
sender_name = settings.sender_name
sender_addr = settings.sender_addr
sender_pwd = settings.sender_pwd


def send_text_mail(receiver_addr, mail_subject, mail_body):
    mail = MIMEText(mail_body, "plain", "utf-8")
    mail["Subject"] = mail_subject
    mail["From"] = formataddr((sender_name, sender_addr))
    mail["To"] = ",".join(receiver_addr)
    result = {'status': 0, 'error_info': None}
    mail_service = smtplib.SMTP_SSL(smtp_server, port=465)
    try:
        mail_service.login(sender_addr, sender_pwd)
        mail_service.sendmail(sender_addr, receiver_addr, mail.as_string())
        result['status'] = 1
        print('successfully')
    except Exception as err:
        result['status'] = 0
        result['error_info'] = str(err)
        print(err)
    mail_service.quit()
    return result
