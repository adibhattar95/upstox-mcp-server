import requests
import webbrowser
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json

class UpstoxAPI:
    def __init__(self, api_key, api_secret, redirect_uri="http://localhost:8000"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.redirect_uri = redirect_uri
        self.base_url = "https://api-v2.upstox.com"
        self.access_token = None
        self.auth_code = None

    def get_login_url(self):
        """Generate login URL"""
        params = {
            'response_type': 'code',
            'client_id': self.api_key,
            'redirect_uri': self.redirect_uri,
            'state': 'xyz'
        }
        return f"{self.base_url}/login/authorization/dialog?" + urllib.parse.urlencode(params)

    def _run_local_server(self):
        """Start HTTP server to receive the auth code"""

        class AuthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                query = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(query)

                if 'code' in params:
                    self.server.auth_code = params['code'][0]
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"<h2>Authorization successful. You may close this window.</h2>")
                    threading.Thread(target=self.server.shutdown, daemon=True).start()
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"<h2>Authorization failed. No code received.</h2>")

            def log_message(self, format, *args):
                return  # silence logs

        server = HTTPServer(('localhost', 8000), AuthHandler)
        server.auth_code = None
        print("🖥️ Waiting for authorization on http://localhost:8000 ...")
        server.handle_request()
        self.auth_code = server.auth_code

    def exchange_code_for_token(self):
        """Exchange auth code for access token"""
        if not self.auth_code:
            raise Exception("No auth code to exchange for token.")

        data = {
            'code': self.auth_code,
            'client_id': self.api_key,
            'client_secret': self.api_secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        res = requests.post(f"{self.base_url}/login/authorization/token", data=data, headers=headers)
        res.raise_for_status()
        tokens = res.json()
        self.access_token = tokens.get("access_token")
        print("✅ Access token received.")
        return tokens

    def login(self):
        """Run the complete login flow"""
        login_url = self.get_login_url()
        print("🌐 Opening browser for login...")
        webbrowser.open(login_url)
        self._run_local_server()

        if not self.auth_code:
            raise Exception("❌ Failed to receive authorization code.")
        print(f"🔑 Received authorization code: {self.auth_code[:6]}...")
        return self.exchange_code_for_token()

    def get_user_profile(self):
        if not self.access_token:
            raise Exception("Access token missing. Login first.")

        headers = {'Authorization': f'Bearer {self.access_token}', 'Accept': 'application/json'}
        res = requests.get(f"{self.base_url}/user/profile", headers=headers)
        res.raise_for_status()
        return res.json()

    def get_positions(self):
        if not self.access_token:
            raise Exception("Access token missing. Login first.")

        headers = {'Authorization': f'Bearer {self.access_token}', 'Accept': 'application/json'}
        res = requests.get(f"{self.base_url}/portfolio/long-term-positions", headers=headers)
        res.raise_for_status()
        return res.json()


def main():
    API_KEY = ""       # 🔁 Replace with your actual API key
    API_SECRET = ""    # 🔁 Replace with your actual secret

    upstox = UpstoxAPI(API_KEY, API_SECRET)

    try:
        tokens = upstox.login()
        print(f"\n🎉 Login successful! Access Token: {tokens['access_token'][:20]}...")

        print("\n📄 Fetching user profile...")
        profile = upstox.get_user_profile()
        print(json.dumps(profile, indent=2))

        print("\n📊 Fetching positions...")
        positions = upstox.get_positions()
        print(json.dumps(positions, indent=2))

    except Exception as e:
        print(f"⚠️ Error: {e}")