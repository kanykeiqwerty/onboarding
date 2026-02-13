from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_intern_credentials_email(user_email, password, login_url):
    """
    Отправка учетных данных новому стажеру
    """
    subject = 'Добро пожаловать! Ваши учетные данные для входа'
    
    # HTML версия письма
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 20px; margin: 20px 0; }}
            .credentials {{ background-color: white; padding: 15px; border-left: 4px solid #4CAF50; margin: 15px 0; }}
            .button {{ display: inline-block; padding: 12px 30px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Добро пожаловать!</h1>
            </div>
            <div class="content">
                <p>Здравствуйте!</p>
                <p>Для вас была создана учетная запись стажера в нашей системе.</p>
                
                <div class="credentials">
                    <h3>Ваши учетные данные для входа:</h3>
                    <p><strong>Email:</strong> {user_email}</p>
                    <p><strong>Пароль:</strong> {password}</p>
                </div>
                
                <p>Для входа в систему перейдите по ссылке ниже:</p>
                <a href="{login_url}" class="button">Войти в систему</a>
                
                <p><strong>Важно:</strong> Рекомендуем изменить пароль после первого входа в систему.</p>
            </div>
            <div class="footer">
                <p>Это автоматическое письмо, пожалуйста, не отвечайте на него.</p>
                <p>Если у вас возникли вопросы, свяжитесь с вашим администратором.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Текстовая версия (для клиентов, не поддерживающих HTML)
    plain_message = f"""
    Добро пожаловать!
    
    Для вас была создана учетная запись стажера в нашей системе.
    
    Ваши учетные данные для входа:
    Email: {user_email}
    Пароль: {password}
    
    Для входа в систему перейдите по ссылке: {login_url}
    
    Важно: Рекомендуем изменить пароль после первого входа в систему.
    
    ---
    Это автоматическое письмо, пожалуйста, не отвечайте на него.
    Если у вас возникли вопросы, свяжитесь с вашим администратором.
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {str(e)}")
        return False