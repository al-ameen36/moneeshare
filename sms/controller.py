import os
import africastalking
from dotenv import load_dotenv

load_dotenv()


username = os.environ.get("AFRICASTALKING_USER")
api_key = os.environ.get("AFRICASTALKING_KEY")
africastalking.initialize(username, api_key)


class SMS:
    def __init__(self):
        self.sms = africastalking.SMS

    def send(self, recipients: list[str], message: str):
        try:
            response = self.sms.send(
                message, recipients, os.environ.get("AFRICASTALKING_NUMBER")
            )
            print(response)
        except Exception as e:
            print(f"Houston, we have a problem: {e}")
