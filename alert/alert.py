import twilio.rest

from alert import config


def send(message):
    client = twilio.rest.Client(*config.auth)
    client.messages.create(config.number, body=message, from_=config.source)
