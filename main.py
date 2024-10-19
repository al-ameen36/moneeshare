import re
from typing import Optional
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import pyotp
from accounts.controller import Account
from accounts.otp import generate_otp
from sms.controller import SMS
from sms.models import SMSModel
from response_templates.help_tmpl import (
    help_template,
    help_send_template,
    help_create_template,
    help_info_template,
)
from response_templates.create_tmpl import create_user_template
from response_templates.account_tmpl import account_info_template
from users.controller import User
from users.schemas import UserType

af_sms = SMS()
user_db = User()
account_db = Account()

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {"app": "Monee share", "status": "ok"}


@app.post("/incoming-messages")
async def receive_sms(
    date: Optional[str] = Form(None),
    from_: str = Form(..., alias="from"),
    id: Optional[str] = Form(None),
    linkId: Optional[str] = Form(None),
    text: str = Form(...),
    to: str = Form(...),
    networkCode: Optional[str] = Form(None),
):
    sms = SMSModel(
        date=date,
        from_=from_,
        id=id,
        linkId=linkId,
        text=text,
        to=to,
        networkCode=networkCode,
    )

    # Check if the text is a 6-digit OTP (no command, just numbers)
    otp_pattern = r"^\d{6}$"
    if re.match(otp_pattern, sms.text.strip()):
        # Handle OTP automatically if it's a 6-digit number
        res = account_db.validate_transaction(sms.from_, sms.text.strip())
        if res[0]:
            transaction = res[1]
            command, *segments = transaction["command"].split(" ")
            amount, beneficiary_number = segments
            try:
                amount = float(amount)
            except ValueError:
                response_to_user = "Provide a valid amount"
                af_sms.send([sms.from_], response_to_user)
                return True

            if len(beneficiary_number) <= 11:
                beneficiary_number = "+234" + beneficiary_number

            response = user_db.send(
                sender_number=sms.from_,
                beneficiary_number=beneficiary_number,
                amount=amount,
            )

            # Handle response
            if response[0]:
                response_to_user = response
                # Delete transaction after processing
                account_db.delete_transaction(transaction["id"])
            else:
                response_to_user = response[1]

            # Send response to beneficiary and sender
            if type(response_to_user) == list and len(response_to_user) > 2:
                _, beneficiary_number = segments
            if len(beneficiary_number) <= 11:
                beneficiary_number = "+234" + beneficiary_number

            af_sms.send([beneficiary_number], response_to_user[2])
            af_sms.send([sms.from_], response_to_user[1])
            return True
        else:
            af_sms.send([sms.from_], "No pending transactions found")
            return True

    # Split the input string to extract the command
    command, *segments = sms.text.split(" ")
    segments = [item.strip() for item in segments if item]  # remove empty strings
    response_to_user = ""
    print(command, segments)

    # HELP COMMANDS
    match command.lower():
        case "help":
            if not len(segments):
                response_to_user = help_template
            else:
                match segments[0]:
                    case "info":
                        response_to_user = help_info_template
                    case "create":
                        response_to_user = help_create_template
                    case "send":
                        response_to_user = help_send_template

    match command.lower():
        case "create":
            user = user_db.create(UserType(phone_number=sms.from_, pin="1234"))
            if user[0]:
                user_account = UserType(**user[1])
                response_to_user = create_user_template.format(
                    account_number=user_account.phone_number.replace("+234", ""),
                    account_balance=10000.0,
                )
            else:
                response_to_user = user[1]

    match command.lower():
        case "info":
            user = user_db.get(UserType(phone_number=sms.from_, pin="1234"))
            print(user)
            if user[0]:
                user_account = UserType(**user[1])
                response_to_user = account_info_template.format(
                    account_number=user_account.accounts[0].account_number,
                    account_balance=user_account.accounts[0].balance,
                )
            else:
                response_to_user = user[1]

    match command.lower():
        case "send":
            otp = generate_otp()
            print(otp)
            account_db.add_transaction(sms.from_, sms.text, otp)
            response_to_user = f"Send {otp} to 34461 to process your transaction"

    # Send response back to the user
    if type(response_to_user) == list:
        af_sms.send([sms.from_], response_to_user[1])
    else:
        af_sms.send([sms.from_], response_to_user)

    print(response_to_user)
    return True
