from typing import Optional
from pydantic import BaseModel


class AccountType(BaseModel):
    id: Optional[int] = None
    user_id: int
    account_number: str
    balance: float
