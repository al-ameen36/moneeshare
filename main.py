from typing import Optional
from urllib import response
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from sms.controller import SMS
from sms.models import SMSModel
from response_templates.help_tmpl import (
    help_template,
    help_send_template,
    help_create_template,
    help_info_template,
)


af_sms = SMS()
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
    # TODO
    # Connect supabase DB
    # Process user requests/command

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

    segments = [item for item in segments if item]  # remove empty strings
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
            response_to_user = "Account created successfully"

    match command.lower():
        case "info":
            response_to_user = "Account number: xxxxxxxxxx\nBalance: 5,000,000"

    match command.lower():
        case "send":
            amount, beneficiary_number = segments
            response_to_user = (
                f"Successfully transfered N{amount} to {beneficiary_number}"
            )

    print(response_to_user)
    af_sms.send([sms.from_], response_to_user)

    return True
