import requests
import os
from dotenv import load_dotenv

load_dotenv()
urls = {"create account": f"{os.environ.get("KORA_BASE_URL")}/virtual-bank-account"}


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
        headers = {"Authorization": f"Bearer {os.environ.get('KORA_SECRET')}"}
        try:
            response = requests.post(
                url=urls["create account"], json=payload, headers=headers
            )
            print(response.json())
        except Exception as error:
            print(error)

        return response.json()
