import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from MP import settings

smtp_server = settings.SMTP_SERVER
sender_name = settings.SENDER_NAME
sender_addr = settings.SENDER_ADDR
sender_pwd = settings.SENDER_PWD


def send_text_mail(receiver_addr, mail_subject, mail_body):
    mail = MIMEText(mail_body, "plain", "utf-8")
    mail["Subject"] = mail_subject
    mail["From"] = formataddr((sender_name, sender_addr))
    mail["To"] = ",".join(receiver_addr)
    result = {'status': False, 'error': None}
    mail_service = smtplib.SMTP_SSL(smtp_server, port=465)
    try:
        mail_service.login(sender_addr, sender_pwd)
        mail_service.sendmail(sender_addr, receiver_addr, mail.as_string())
        result['status'] = True
        # print('successfully')
    except Exception as err:
        result['status'] = False
        if err:
            result['error'] = str(err)
        else:
            result['error'] = 'Mail service failed.'
        # print(err)
    mail_service.quit()
    return result
