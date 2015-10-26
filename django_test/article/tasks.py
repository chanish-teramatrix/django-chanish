from __future__ import absolute_import
from celery import task
from django.core.mail import send_mail, EmailMessage
from celery import Celery
import logging
logger = logging.getLogger(__name__)
# from django.http import HttpResponse
# import json
app = Celery('tasks', broker='redis://localhost//')

@task
def Mailsend(result):
    """
    This is a Celery function which send mail for given parameters(valid and checked) used If Else for case of attachments availability

    :Args:
    result = {
    success : bit represents either mail successfully delivered or not 0:Delivered, 1:Not Delivered
    message : Contains error message if there any
    attachments: This is file attachments variable
        data = {
        subject : mail subject
        message : Message Body
        from_email : sender email id
        to_email : List/Tuple of receivers email id's
        }
    }

    :return: True/False
    """
    mail = EmailMessage(result['data']['subject'], result['data']['message'],
                        result['data']['from_email'],
                        result['data']['to_email'])


    # Handling mail without an attachment.
    if not result['attachments']:
        mail.send()

    # Mail with attachments.
    else:
        mail.attach(result['attachments'].name, result['attachments'].read(),
                    result['attachments'].content_type)
        mail.send()

    return True
