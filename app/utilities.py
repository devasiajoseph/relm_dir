import sha
import random
import datetime
from django.core.mail import send_mail
from django.conf import settings


def send_activation_email(email, key):
    email_subject = 'Activate your account'
    email_body = 'Account activation Link %(site_url)s/activate/%(activation_key)s' % {"site_url": settings.SITE_URL, "activation_key": key}
    send_mail(email_subject,
              email_body,
              settings.ADMIN_EMAIL,
              [email],
              fail_silently=False)


def send_password_reset_email(email, key):
    email_subject = 'Password reset'
    email_body = 'Password Reset Link %(site_url)s/password/reset/form/%(activation_key)s' % {"site_url": settings.SITE_URL, "activation_key": key}
    send_mail(email_subject,
              email_body,
              settings.ADMIN_EMAIL,
              [email],
              fail_silently=False)


def send_register_success_email(email):
    email_subject = 'Registration request received'
    email_body = 'Registration request received successfully. We will let you know when it is approved'
    send_mail(email_subject,
              email_body,
              settings.ADMIN_EMAIL,
              [email],
              fail_silently=True)


def send_seller_approval_email(email, key):
    email_subject = 'Request approved'
    email_body = ' Approval link: %(site_url)s/seller/signup/%(approval_key)s' % {"site_url": settings.SITE_URL, "approval_key": key}
    send_mail(email_subject,
              email_body,
              settings.ADMIN_EMAIL,
              [email],
              fail_silently=False)


def create_key(mixer, expiry):
    salt = sha.new(str(random.random())).hexdigest()[:10]
    key = sha.new(salt + mixer).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    return {"key": key, "expiry": key_expires}


def reply_object():
    """
    reference for the reply json object
    """
    reply_object = {"code": ""}
    return reply_object
