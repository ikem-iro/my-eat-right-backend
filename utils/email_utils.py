import emails
from jinja2 import Template
from auth.models import EmailData
from .config_utils import settings
from pathlib import Path
import smtplib, ssl
from email.message import EmailMessage



def render_email_template(template_name:str, context:dict[str, any]) -> str:
    """
    Render an email template with the given template name and context.

    Args:
        template_name (str): The name of the email template file.
        context (dict[str, any]): The context data used to render the template.

    Returns:
        str: The rendered HTML content of the email template.
    """
    template_str = (Path(__file__).parent.parent/"email-templates"/"build"/ template_name).read_text()
    html_content = Template(template_str).render(context)
    return html_content



def generate_verification_email(email_to: str, email: str, token: str):
    """
    Generate a verification email for the given email address.

    Args:
        email_to (str): The email address to send the verification email to.
        email (str): The email address of the user to verify.
        token (str): The verification token.

    Returns:
        EmailData: An object containing the HTML content and subject of the verification email.
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Verify your email for user {email}"
    link = f"{settings.FRONTEND_URL}verify-email?token={token}"
    html_content = render_email_template(template_name="verify_email.html", context={
        "project_name": project_name,
        "username": email,
        "email": email_to,
        "valid_minutes": settings.VERIFY_EMAIL_TOKEN_EXPIRES,
        "link": link
    })
    return EmailData(html_content=html_content, subject=subject)

def generate_reset_password_email(email_to: str, email: str, token: str):
    """
    Generate a password reset email for the given email address.

    Args:
        email_to (str): The email address to send the password reset email to.
        email (str): The email address of the user requesting the password reset.
        token (str): The password reset token.

    Returns:
        EmailData: An object containing the HTML content and subject of the password reset email.
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{settings.FRONTEND_URL}reset-password?token={token}"
    html_content = render_email_template(template_name="reset_password.html", 
        context= {
            "project_name": project_name,
            "username": email,
            "email": email_to,
            "valid_minutes": settings.PASSWORD_RESET_TOKEN_EXPIRES,
            "link": link
        }
    )

    return EmailData(html_content=html_content, subject=subject)





def send_mail(email_to: str, subject: str, html_content: str):
    """
    Sends an email to the specified recipient.

    Args:
        email_to (str): The email address of the recipient.
        subject (str): The subject of the email.
        html_content (str): The HTML content of the email.

    Returns:
        dict: A dictionary indicating the status of the email sending process. If successful, it will contain the key "success" with the value "successfully sent". If there is an error, it will contain the key "error" with the corresponding error message.
    """
    port = settings.SMTP_PORT
    smtp_server = settings.SMTP_SERVER
    username= settings.SMTP_USER
    password = settings.SMTP_PASS
    message = html_content
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = settings.EMAILS_FROM_MAIL
    msg['To'] = email_to
    msg.add_alternative(message, subtype="html")
    try:
        match port:
            case settings.SMTP_PORT:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(username, password)
                    server.send_message(msg)
            case settings.SMTP_ALT_PORT:
                with smtplib.SMTP(smtp_server, port) as server:
                    server.starttls()
                    server.login(username, password)
                    server.send_message(msg)
            case _:
                return {"error": "use 465 / 587 as port value"}
        return {"success": "Email successfully sent"}
    except Exception as e:
        return {"error": e}























# def send_email(email_to: str, subject: str, html_content: str):
#     mail = emails.Message(subject=subject, html=html_content, mail_from=settings.EMAILS_FROM_NAME)
#     smtp_options = {
#         "host": settings.SMTP_HOST,
#         "port": settings.SMTP_PORT,
#         "user": settings.SMTP_USER,
#         "password": settings.SMTP_PASSWORD
#     }

#     if settings.SMTP_TLS:
#         smtp_options["tls"] = True
#     elif settings.SMTP_SSL:
#         smtp_options["ssl"] = True
#     mail.send(to=email_to, smtp=smtp_options)

