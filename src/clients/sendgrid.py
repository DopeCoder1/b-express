from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class MailClient:
    def __init__(self):
        self.api_key = "api_key"
        self.sender = "info@b-express.kz"
        self.sg = SendGridAPIClient(self.api_key)

    def send(self, to, subject, content):
        message = Mail(
            from_email=self.sender,
            to_emails=to,
            subject=subject,
            html_content=content
        )
        response = self.sg.send(message)
        return response

mail_client = MailClient()
