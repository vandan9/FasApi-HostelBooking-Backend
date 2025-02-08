# this file user for sending mail to user for email verifycation
from pydantic import EmailStr
import pyotp
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from .config import settings as email_settings
from fastapi import HTTPException
import time

# Configure email
conf = ConnectionConfig(
    MAIL_USERNAME=email_settings.EMAIL_HOST_USER,
    MAIL_PASSWORD=email_settings.EMAIL_HOST_PASSWORD,
    MAIL_FROM=email_settings.EMAIL_HOST_USER,
    MAIL_PORT=587,
    MAIL_SERVER=email_settings.EMAIL_HOST,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

fastmail = FastMail(conf)

otp_store = {}

def send_otp(email: EmailStr):
    totp = pyotp.TOTP(pyotp.random_base32())
    otp = totp.now()

    otp_store[email] = {
        "otp": otp,
        "timestamp": time.time()
    }

    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=f"Your OTP code is {otp}",
        subtype="plain"
    )

    return fastmail.send_message(message)

def verify_otp(email: EmailStr, otp: str):
    if email in otp_store:
        stored_otp_info = otp_store[email]
        stored_otp = stored_otp_info["otp"]
        timestamp = stored_otp_info["timestamp"]

        if stored_otp == otp and time.time() - timestamp < 300:
            del otp_store[email]
            return True
    return False

