from django.core.mail import send_mail


def send_email(subject, message, to_email):
    print("Sending email to: ", to_email)
    from_email = "easyhome.applicationhelp@gmail.com"
    send_mail(subject, message, from_email, [to_email], fail_silently=False)
