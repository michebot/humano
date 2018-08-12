import twilio
from twilio.rest import Client

import os


def send_message_to_recipients(contact_phone_number, message):
    """When a user clicks on button, a message will be sent."""

    # Your Account SID from twilio.com/console
    ACCOUNT_SID = os.environ["ACCOUNT_SID"]
    # Your Auth Token from twilio.com/console
    AUTH_TOKEN = os.environ["AUTH_TOKEN"]

    MY_NUM = os.environ.get("MY_NUM")
    TWILIO_NUM = os.environ.get("TWILIO_NUM")

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # message = client.messages.create(
    #     to=MY_NUM, 
    #     from_=TWILIO_NUM,
    #     body="Hi my name's Marcelle and I'm a shell.")

    message = client.messages.create(
    to=contact_phone_number,
    from_=TWILIO_NUM,
    body=message)

    print(message.sid)


    # """I'm testing out my app. Please save this number as "Michelle's app" 
    # and respond back to Michelle (not this number) with a "yes" if you get this messgae. PROMPTLY :)"""