from typing import Optional
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from accounts.controller import Account
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


# def split_phone_number(phone_number: str):
#     if phone_number.startswith("+") or len(phone_number) > 11:
#         return (phone_number[:4], phone_number[4:])
#     return (None, phone_number)


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
    is_valid = af_sms.check_structure(text.lower())
    if not is_valid[0]:
        af_sms.send([from_], is_valid[1])
        return True

    sms = SMSModel(
        date=date,
        from_=from_,
        id=id,
        linkId=linkId,
        text=text,
        to=to,
        networkCode=networkCode,
    )
    command, *segments = sms.text.split(" ")
    segments = [item.strip() for item in segments if item]  # remove empty strings
    response_to_user = ""

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
            amount, beneficiary_number = segments
            try:
                amount = float(amount)
            except ValueError:
                response_to_user = "Provide a valid amount"
                af_sms.send([sms.from_], response_to_user)
                return True

            if len(beneficiary_number) < 11:
                beneficiary_number = "+234" + beneficiary_number

            response = user_db.send(
                sender_number=sms.from_,
                beneficiary_number=beneficiary_number,
                amount=amount,
            )
            if response[0]:
                response_to_user = response
            else:
                response_to_user = response[1]

    if type(response_to_user) == list and len(response_to_user) > 2:
        _, beneficiary_number = segments
        af_sms.send([beneficiary_number], response_to_user[2])
    elif type(response_to_user) == list:
        af_sms.send([sms.from_], response_to_user[1])
    else:
        af_sms.send([sms.from_], response_to_user)

    return True
