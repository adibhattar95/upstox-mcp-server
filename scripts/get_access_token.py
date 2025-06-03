import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lib.upstox_auth import UpstoxAPI
from src.utils.env import UPSTOX_API_KEY, UPSTOX_SECRET_KEY


def main():
    API_KEY = UPSTOX_API_KEY
    API_SECRET = UPSTOX_SECRET_KEY

    upstox = UpstoxAPI(API_KEY, API_SECRET)

    try:
        tokens = upstox.login()
        upstox.save_token_to_env()
        print(f"\n🎉 Login successful! Access token received and saved.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()