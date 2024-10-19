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

    def add_transaction(self, phone: str, transaction: str, otp):
        try:
            response = (
                self.db.table("transactions")
                .insert({"account": phone, "command": transaction, "otp": otp})
                .execute()
            )
            return [True, response]
        except Exception as error:
            print(error)
            return [True, "Something went wrong. Try again"]

    def validate_transaction(self, phone: str, pin: str):
        try:
            transaction = (
                self.db.table("transactions").select("*").eq("account", phone).execute()
            )
            print(transaction)
            if transaction.data[0]:
                transaction = transaction.data[0]
                if transaction["otp"] == pin:
                    return [True, transaction]
                else:
                    return [False, "Something went wrong. Try again"]
            else:
                return [False, "Something went wrong. Try again"]
        except Exception as error:
            print(error)
            return [False, "Something went wrong. Try again"]

    def delete_transaction(self, id: int):
        try:
            self.db.table("transactions").delete().eq("id", id).execute()
        except Exception as error:
            print(error)
            return [False, "Something went wrong. Try again"]
