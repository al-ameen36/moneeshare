from typing import Optional
from fastapi import Form
from pydantic import BaseModel


class SMSModel(BaseModel):
    date: Optional[str] = Form(None)
    from_: str = Form(
        ..., alias="from"
    )  # handle "from" being a reserved keyword in python
    id: Optional[str] = Form(None)
    linkId: Optional[str] = Form(None)
    text: str = Form(...)
    to: str = Form(...)
    networkCode: Optional[str] = Form(None)
