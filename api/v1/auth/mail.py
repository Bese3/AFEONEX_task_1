#!/usr/bin/env python3
from flask_mail import Mail, Message
from models import app
from random import randint
from os import getenv
from datetime import datetime, timedelta


app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=587
sender_email = getenv('EMAIL')
sender_password = getenv('PASSWORD')
app.config["MAIL_USERNAME"]=sender_email
app.config['MAIL_PASSWORD']=sender_password
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
mail=Mail(app)


class MailProccesor:
    def __init__(self, recipient, subject='Verify Email') -> None:
        if not isinstance(subject, str):
            raise TypeError('subject must be string')
        if not isinstance(recipient, str):
            raise TypeError('recipient must be string')
        self.__otp = randint(000000,999999)
        self.__body = f'''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Verify Email</title>
                    </head>
                    <body>
                        <h1>One-Time Password (OTP)</h1>
                        <p>Your OTP for Email verification is: <strong>{str(self.__otp)}</strong></p>
                        <p>Use this OTP to complete your action.</p>
                        <p>If you didn't request this OTP, please ignore this email.</p>
                        <p>This is an automated email. Please do not reply.</p>
                    </body>
                    </html>
                    '''
        self.__subject = subject
        self.__recipient = recipient

    @property
    def otp(self):
        return self.__otp

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, value):
        if not isinstance(value, str):
            raise TypeError('value must be string')
        self.__body = value

    def send_mail(self):
        msg = Message(subject=self.__subject,
                      sender='Noreply@twittBuzz.com',
                      recipients=[self.__recipient])
        msg.html = self.__body
        mail.send(msg)
        return self.otp
