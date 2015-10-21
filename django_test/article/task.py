from celery import task

@task()
def Mailsend():
    if error_messages:
            # succes bit has changed to '1'
            # success = 1 : mail has not been send
            result['success'] = 1

            # result['message'] : expected errors has been stored their
            result['message'] = error_messages
            print '*' * 30
            print result
            print '*' * 30
            HttpResponse(json.dumps(result))

        else:
            # TODO: correct to_email here used list for testing purpose
            mail = EmailMessage(subject, message, from_email, [to_email])
            # Handling mail without an attachment
            if not attachments:
                mail.send()
            # Handling mail with attachments
            else:
                mail.attach(attachments.name, attachments.read(),
                            attachments.content_type)
                mail.send()
            print '*' * 30
            print result
            print '*' * 30
            HttpResponse(json.dumps(result))