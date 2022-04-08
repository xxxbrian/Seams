from flask_mail import Mail, Message
from flask import Flask
from src.config import MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_USE_TLS, MAIL_USE_SSL

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
mail = Mail(app)


def email_send(text: str, recipients: list):
    msg = Message('UNSW-COMP1531', sender=MAIL_USERNAME, recipients=recipients)
    msg.body = text
    mail.send(msg)
