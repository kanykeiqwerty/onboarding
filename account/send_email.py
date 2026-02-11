from django.core.mail import send_mail

def send_reset_password(user):
    code = user.activation_code
    to_email = user.email
    send_mail(
    subject='Reset password',
    message=f'Your code for reset password: {code}',
    from_email=None,  # возьмётся DEFAULT_FROM_EMAIL
    recipient_list=[to_email],
    fail_silently=False
)

