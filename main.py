from typing import Optional
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from sms.models import SMSModel

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
    command, *segments = sms.text.split(" ")
    print(command, segments)

    return True
