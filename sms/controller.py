import os
import re
import africastalking
from dotenv import load_dotenv
from response_templates.help_tmpl import (
    help_create_template,
    help_info_template,
    help_send_template,
    help_template,
)

load_dotenv()


username = os.environ.get("AFRICASTALKING_USER")
api_key = os.environ.get("AFRICASTALKING_KEY")
africastalking.initialize(username, api_key)


class SMS:
    patterns = {
        "send": {"regex": r"^send \d+ (\+?\d{1,3})?\d{8,13}$", "msg": ""},
        "help": {"regex": r"^help(?: (info|send|create))?$", "msg": ""},
        "info": {"regex": r"^info$", "msg": ""},
        "create": {"regex": r"^create$", "msg": ""},
    }

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

    def check_structure(self, input_string: str):
        # Split the input string to get the command
        command = input_string.split()[0]

        if command in self.patterns and re.match(
            self.patterns[command]["regex"], input_string
        ):
            return [True, f"'{input_string}' matches the expected structure."]
        else:
            if "info" in command.lower() or command.lower() in "info":
                return [False, help_info_template]
            elif "create" in command.lower() or command.lower() in "create":
                return [False, help_create_template]
            elif "send" in command.lower() or command.lower() in "send":
                return [False, help_send_template]
            else:
                return [
                    False,
                    help_template,
                ]
