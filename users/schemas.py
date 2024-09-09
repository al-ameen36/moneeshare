from typing import List, Optional
from pydantic import BaseModel

from accounts.schemas import AccountType


class UserType(BaseModel):
    id: Optional[int] = None
    full_name: Optional[str] = None
    phone_number: str
    pin: str
    accounts: Optional[List[AccountType]] = None
