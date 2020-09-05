import os
from flask import Flask 
from flask_mail import Mail 

app= Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] =  587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEBUG"] = True
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = ps.environ["MAIL_PASSWORD"]
app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_USERNAME"]
app.config["MAIL_MAX_EMAILS"] = None
app.config["MAIL_SUPRESS_SEND"] = False
app.config["MAIL_ASCII_ATTACHMENTS"] =  False


mail = Mail(app)