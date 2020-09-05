import requests
from typing import List

class MailGun:
    @classmethod
    def send_mail(cls,email,subject,text,html) -> Response:
        link = request.url_root[:-1] + url_for("userconfirm",user_id=self.username)
        requests.post(
            f"http://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api",cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )