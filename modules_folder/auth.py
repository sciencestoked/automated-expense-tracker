# modules_folder/auth.py

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# --- Authentication ---
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    creds_path = os.path.join(os.path.dirname(__file__), '../creds_folder/')
    
    token_path = os.path.join(creds_path, 'token.json')
    creds_file = os.path.join(creds_path, 'credentials.json')
    
    # Check if token already exists
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # Refresh the token if expired or authenticate if no token found
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    return service


if __name__ == "__main__":
    service = authenticate_gmail()
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    for x in labels:
        print(x)
  