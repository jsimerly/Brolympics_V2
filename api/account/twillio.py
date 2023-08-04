from twilio.rest import Client
import os

account_sid = os.environ['TWILIO_ACCOUNT_SID_PROD']
auth_token = os.environ['TWILIO_AUTH_TOKEN_PROD']
verify_service_sid=os.environ['TWILIO_BROLYMPICS_VERIFY_SERVICE_ID']
twilio_number=os.environ['TWILIO_PHONE_NUMBER']

def send_verification_code(phone_number):
    client = Client(account_sid, auth_token)
    verification = client.verify \
        .services(verify_service_sid) \
        .verifications \
        .create(to=phone_number, channel='sms')

def check_verification_code(phone_number, code):
    client = Client(account_sid, auth_token)
    verification_check = client.verify \
        .services(verify_service_sid) \
        .verification_checks \
        .create(to=phone_number, code=code)

    return verification_check.status 


def reset_password_sms(phone_number, link):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Please follow this link to reset your password: {link}',
        from_=twilio_number,
        to=phone_number
    )
