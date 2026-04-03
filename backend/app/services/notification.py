"""Notification service: Firebase FCM push notifications and SMS OTP via Twilio."""

from app.config import settings


async def send_push_notification(
    device_token: str,
    title: str,
    body: str,
    data: dict | None = None,
) -> bool:
    """Send a Firebase FCM push notification to the given device token."""
    try:
        import firebase_admin
        from firebase_admin import credentials, messaging

        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_JSON)
            firebase_admin.initialize_app(cred)

        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            data=data or {},
            token=device_token,
        )
        messaging.send(message)
        return True
    except Exception:
        return False


async def send_sms_otp(phone: str) -> str:
    """Generate an OTP, send it via Twilio SMS, and return the code."""
    from app.services.auth import send_otp

    otp = await send_otp(phone)

    if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
        try:
            from twilio.rest import Client

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=f"Your QARD verification code is: {otp}",
                from_=settings.TWILIO_FROM_NUMBER,
                to=phone,
            )
        except Exception:
            pass

    return otp
