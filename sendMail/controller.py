from django.core.mail import EmailMultiAlternatives
from CSEPcon.settings import DEFAULT_FROM_EMAIL
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import extencion


url = "http://localhost:3000/auth/password-change"

def send_email(user, email, title):
    token = RefreshToken.for_user(user)
    new_url = f"{url}?token={token.access_token}"

    context = {"username": user.username, "new_url": new_url}
    html_content = render_to_string(
        'sendMail/correo.html', context
    )
    text = strip_tags(html_content)
    email = EmailMultiAlternatives(
        title,text,DEFAULT_FROM_EMAIL,email
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    
        
    