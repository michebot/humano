from twilio.rest import Client

import os

# Your Account SID from twilio.com/console
ACCOUNT_SID = os.environ['ACCOUNT_SID']
# Your Auth Token from twilio.com/console
AUTH_TOKEN = os.environ['AUTH_TOKEN']

client = Client(ACCOUNT_SID, AUTH_TOKEN)

message = client.messages.create(
    to="+17142091862", 
    from_="+14156049324",
    body="herro herro")

print(message.sid)