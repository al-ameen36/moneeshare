import os
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {"Authorization": f"Bearer {os.environ.get('KORA_SECRET')}"}
url = f"https://api.korapay.com/merchant/api/v1/charges/8181114416"

payload = {"reference": "8181114416", "amount": 100}

try:
    # res = requests.get(url=url, json=payload, headers=headers)
    res = requests.get(url=url, headers=headers)
    print(res.json())
except Exception as error:
    print(error)
