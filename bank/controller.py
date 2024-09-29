import requests
import os
from dotenv import load_dotenv

load_dotenv()
urls = {
    "create account": f"{os.environ.get("KORA_BASE_URL")}/virtual-bank-account",
    "transfer":f"{os.environ.get("KORA_BASE_URL")}/virtual-bank-account/sandbox/credit",
}
headers = {"Authorization": f"Bearer {os.environ.get('KORA_SECRET')}"}


class Bank:
    def create_account(
        self,
        acc_name: str,
        phone: str,
        bank_code: str,
        customer_name: str,
        bvn: str,
        nin: str,
    ):
        payload = {
            "account_name": acc_name,
            "account_reference": phone,
            "permanent": True,
            "bank_code": bank_code,
            "customer": {"name": customer_name},
            "kyc": {"bvn": bvn, "nin": nin},
        }
        try:
            response = requests.post(
                url=urls["create account"], json=payload, headers=headers
            )
            print(response.json())
        except Exception as error:
            print(error)

        return response.json()
    
    def transfer(self, beneficiary:str, amount:float):
        try:
                payload = {"reference": beneficiary, "amount": amount}
                response = requests.get(url=urls["transfer"], json=payload, headers=headers)
                print(response.json())
        except Exception as error:
            print(error)

        return response.json()
