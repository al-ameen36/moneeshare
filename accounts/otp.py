import pyotp
import os
from dotenv import load_dotenv

load_dotenv()


def generate_otp() -> str:
    totp = pyotp.TOTP(
        os.environ.get("OPT_SECRET"), interval=300
    )  # OTP valid for 5 minutes
    return totp.now()


def validate_otp(otp: str) -> bool:
    totp = pyotp.TOTP(os.environ.get("OPT_SECRET"), interval=300)
    return totp.verify(otp)
