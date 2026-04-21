import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_service():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cred_path = os.path.join(BASE_DIR, "credentials.json")

    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Missing credentials.json at {cred_path}")

    flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
    creds = flow.run_local_server(port=0)

    return build("gmail", "v1", credentials=creds)


def fetch_emails(service):
    results = service.users().messages().list(userId="me", maxResults=5).execute()
    return results.get("messages", [])