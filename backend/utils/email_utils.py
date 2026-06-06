import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def send_otp_email(recipient_email, otp_code):
    """Send OTP email using Brevo API."""
    try:
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": recipient_email}],
            sender={
                "name": "AI Risk Auth",
                "email": os.getenv("MAIL_USERNAME")
            },
            subject="Your Security Verification Code",
            text_content=f"""
Hello,

A login attempt was detected from an unrecognised device or location.

Your one-time verification code is: {otp_code}

This code expires in 5 minutes.

If you did not attempt to login, please secure your account immediately.

— AI Risk Auth System
            """
        )

        response = api_instance.send_transac_email(send_smtp_email)
        print(f"OTP email sent! Status: {response.message_id}")
        return True

    except ApiException as e:
        print(f"Brevo API error: {e}")
        return False
    except Exception as e:
        print(f"Email error: {e}")
        return False