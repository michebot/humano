import twilio
from twilio.rest import Client

import os


def send_message_to_recipients(contact_phone_number, message):
    """When a user clicks on button, a message will be sent."""

    # Account SID from twilio.com/console
    ACCOUNT_SID = os.environ["ACCOUNT_SID"]
    # Auth Token from twilio.com/console
    AUTH_TOKEN = os.environ["AUTH_TOKEN"]

    MY_NUM = os.environ.get("MY_NUM")
    TWILIO_NUM = os.environ.get("TWILIO_NUM")

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
    to="+1"+contact_phone_number,
    from_=TWILIO_NUM,
    body=message)

    error_code = ""

    if message.error_code:
        error_code = message.error_code

    return [message.sid, message.date_created, error_code]