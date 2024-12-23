import os
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# --- Authentication ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",  # Google Sheets API scope
    "https://www.googleapis.com/auth/drive",        # Google Drive API scope
    "https://www.googleapis.com/auth/gmail.readonly",  # Gmail read-only scope
    "https://www.googleapis.com/auth/gmail.send",      # Gmail send scope
]

def authenticate_gmail_and_sheets():
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
    gmail_service = build('gmail', 'v1', credentials=creds)
    
    # Build the Google Sheets API service using gspread
    sheets_client = gspread.authorize(creds)
    
    return gmail_service, sheets_client


def test_authentication(gmail_service, sheets_client):
    # Test Gmail API by listing labels
    results = gmail_service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    print("Gmail Labels:")
    if not labels:
        print("No labels found.")
    for label in labels:
        print(f"- {label['name']}")
    
    # Test Google Sheets API by fetching data from a specific spreadsheet
    print("\nGoogle Sheets:")
    spreadsheet_name = "Budgeting"  # Replace with your spreadsheet's name or ID
    try:
        # Open the specific spreadsheet by title
        spreadsheet = sheets_client.open(spreadsheet_name)
        
        # Fetch data from the first sheet as a test
        worksheet = spreadsheet.sheet1
        print(f"Data from '{spreadsheet_name}':")
        data = worksheet.get_all_values()  # Get all values from the first sheet
        if not data:
            print("No data found in the spreadsheet.")
        else:
            for row in data[:20]:  # Limit to the first 5 rows for testing
                print(row)
    except Exception as e:
        print(f"Error accessing spreadsheet: {e}")


if __name__ == "__main__":
    # Authenticate for both Gmail and Google Sheets
    gmail_service, sheets_client = authenticate_gmail_and_sheets()
    
    # Test the authentication
    test_authentication(gmail_service, sheets_client)
