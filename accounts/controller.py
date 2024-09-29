from db.controller import db
from users.schemas import UserType


class Account:

    def __init__(self):
        self.db = db

    def create(self, user: UserType, account_number: str):
        try:
            response = (
                self.db.table("accounts")
                .insert(
                    {
                        "account_number": account_number,
                        "user_id": user.id,
                    }
                )
                .execute()
            )
            return [True, response.data[0]]
        except Exception as error:
            print(error)
            return [False, "Account creation failed"]

    def update(self, user_id: int, amount: float):
        try:
            response = (
                self.db.table("accounts")
                .update({"balance": amount})
                .eq("user_id", user_id)
                .execute()
            )
            return [True, response]
        except Exception as error:
            print(error)
            return [True, "Something went wrong. Try again"]
