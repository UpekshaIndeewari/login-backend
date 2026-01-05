# services/email_service.py
import smtplib, ssl
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
# EMAIL_FROM = "indiedirisooriya@gmail.com" #should change in to company email
# EMAIL_PASSWORD = "wktctvgvupygbcrs" #should change in to company pw

def send_verification_email(to_email: str, token: str):
    link = f"http://localhost:8000/auth/verify-email?token={token}"

    body = f"""
    Hello,

    Thank you for registering.
    Please verify your email by clicking the link below:

    {link}

    This link is valid for 15 minutes.
    """

    msg = MIMEText(body)
    msg["Subject"] = "Verify your email"
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

def send_reset_email(to_email: str, token: str):
    link = f"http://localhost:5173/resetpw?token={token}"  # React reset page

    body = f"""
    Hello,

    You requested to reset your password.
    Please click the link below to set a new password:

    {link}

    This link is valid for 15 minutes.
    """

    msg = MIMEText(body)
    msg["Subject"] = "Reset your password"
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
