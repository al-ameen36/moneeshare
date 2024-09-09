from accounts.controller import Account
from db.controller import db
from users.schemas import UserType
from response_templates.create_tmpl import (
    create_exists_template,
    create_failed_template,
)
from response_templates.account_tmpl import (
    account_not_found_template,
)

account_db = Account()


class User:

    def __init__(self):
        self.db = db

    def create(self, user: UserType):
        try:
            response = (
                self.db.table("users")
                .insert({"phone_number": user.phone_number, "pin": user.pin})
                .execute()
            )
            user_account = account_db.create(UserType(**response.data[0]))
            return [True, response.data[0]]
        except Exception as error:
            if "duplicate" in error.__dict__.get("message"):
                return [False, create_exists_template]
            else:
                print(error)
                return [False, create_failed_template]

    def get(self, user: UserType):
        try:
            response = (
                self.db.table("users")
                .select("*, accounts(*)")
                .eq("phone_number", user.phone_number)
                .execute()
            )
            if len(response.data):
                return [True, response.data[0]]
            else:
                return [False, account_not_found_template]
        except Exception as error:
            print(error)
            return [False, account_not_found_template]

    def get_by_phone_number(self, phone_number: str):
        try:
            response = (
                self.db.table("users")
                .select("*, accounts(*)")
                .eq("phone_number", phone_number)
                .execute()
            )
            if len(response.data):
                return [True, response.data[0]]
            else:
                return [False, account_not_found_template]
        except Exception as error:
            print(error)
            return [False, account_not_found_template]

    def send(self, sender_number: str, beneficiary_number: str, amount: float):
        try:
            db_sender = self.get_by_phone_number(sender_number)
            db_beneficiary = self.get_by_phone_number(beneficiary_number)

            if db_sender[0]:
                db_sender = UserType(**db_sender[1])
                sender_new_balance = db_sender.accounts[0].balance - amount

                if db_sender.accounts[0].balance < amount:
                    return [
                        False,
                        f"Insufficient funds N{amount}\nBalance: N{db_sender.accounts[0].balance}",
                    ]

                if db_beneficiary[0]:
                    db_beneficiary = UserType(**db_beneficiary[1])
                    beneficiary_new_balance = (
                        db_beneficiary.accounts[0].balance + amount
                    )

                    account_db.update(db_sender.id, sender_new_balance)
                    account_db.update(db_beneficiary.id, beneficiary_new_balance)
                    return [
                        True,
                        f"Successfully transfered N{amount} to {db_beneficiary.accounts[0].account_number}\nBalance: N{sender_new_balance}",
                        f"You just recieved N{amount} from {db_sender.accounts[0].account_number}\nBalance: N{beneficiary_new_balance}",
                    ]
                else:
                    db_beneficiary = self.create(
                        UserType(phone_number=beneficiary_number, pin="1234")
                    )
                    db_beneficiary = UserType(**db_beneficiary[1])

                    beneficiary_new_balance = 10000.0 + amount

                    account_db.update(db_sender.id, sender_new_balance)
                    account_db.update(db_beneficiary.id, beneficiary_new_balance)
                    beneficiary_account_number = db_beneficiary.phone_number.replace(
                        "+234", ""
                    )
                    return [
                        True,
                        f"Successfully transfered N{amount} to {beneficiary_account_number}",
                        f"Welcome to moneeshare. You just recieved N{amount} from {db_sender.accounts[0].account_number}.\nAccount Number: {beneficiary_account_number}\nBalance: N{beneficiary_new_balance}",
                    ]

            else:
                return [False, account_not_found_template]
        except Exception as error:
            print(error)
            return [False, account_not_found_template]
