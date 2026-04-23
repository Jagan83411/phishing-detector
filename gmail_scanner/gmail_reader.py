import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
TOKEN_DIR = os.path.join(BASE_DIR, "user_tokens")

os.makedirs(TOKEN_DIR, exist_ok=True)


def get_service(user_email=None):
    creds = None
    token_path = None

    if user_email:
        token_path = os.path.join(TOKEN_DIR, f"{user_email}.json")

    # Load existing token
    if token_path and os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    # If no valid creds, login
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_PATH, SCOPES
        )
        creds = flow.run_local_server(port=0)

        # Get user email after login
        service = build("gmail", "v1", credentials=creds)
        profile = service.users().getProfile(userId="me").execute()
        user_email = profile["emailAddress"]

        token_path = os.path.join(TOKEN_DIR, f"{user_email}.json")

        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

        return service, user_email

    return build("gmail", "v1", credentials=creds), user_email


def fetch_emails(service):
    results = service.users().messages().list(userId="me", maxResults=10).execute()
    return results.get("messages", [])