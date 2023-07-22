from twilio.rest import Client
import os

account_sid = os.environ['TWILIO_ACCOUNT_SID_PROD']
auth_token = os.environ['TWILIO_AUTH_TOKEN_PROD']
verify_service_sid = os.environ['TWILIO_BROLYMPICS_VERIFY_SERVICE_ID']
twilio_number = os.environ['TWILIO_PHONE_NUMBER']

client = Client(account_sid, auth_token)

def send_sms(message, phone):
    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=phone
    )
    print("Message sent:", message.sid)