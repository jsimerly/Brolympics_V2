from twilio.rest import Client
import os

account_sid = os.environ['TWILIO_ACCOUNT_SID_PROD']
auth_token = os.environ['TWILIO_AUTH_TOKEN_PROD']
verify_service_sid=os.environ['TWILIO_BROLYMPICS_VERIFY_SERVICE_ID']

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

