import os
from flask import Flask 
from flask_mail import Mail,Message

app= Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] =  587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEBUG"] = True
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_USERNAME"]
app.config["MAIL_MAX_EMAILS"] = None
app.config["MAIL_SUPRESS_SEND"] = False
app.config["MAIL_ASCII_ATTACHMENTS"] =  False


mail = Mail(app)


@app.route("/send")
def send():
    msg =  Message("Hey There",recipients=["user@gmail.com"])
    msg.body = "This is a sample email for default users"
    msg.html = "<br>Adding HTML to your email</br>"
    mail.send(msg)

    return f"Mail Sent Successfully"

if __name__ =="__main__":
    app.run(debug=True)