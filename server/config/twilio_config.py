from twilio.rest import Client
from os import getenv

twilio_client = Client(getenv('TWILIO_ACCOUNT_SID'), getenv('TWILIO_AUTH_TOKEN'))