import pandas as pd
import csv

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# Define the credentials and authenticate using gspread
# def authenticate_sheets():
#     # Define the scope of the API
#     scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

#     # Authenticate using the service account (ensure the credentials file is correct)
#     creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_credentials.json', scope)
#     client = gspread.authorize(creds)
#     return client


# Function to upload CSV to a specific sheet in Google Sheets
def upload_csv_to_sheet(
    sheets_client, spreadsheet_name, csv_file_path, sheet_name="Sheet1"
):
    client = sheets_client

    try:
        # Open the spreadsheet
        print(f"Opening spreadsheet: {spreadsheet_name}")
        spreadsheet = client.open(spreadsheet_name)

        # List all sheet names to check if the target sheet exists
        sheet_titles = [sheet.title for sheet in spreadsheet.worksheets()]
        print(f"Available sheet names: {sheet_titles}")

        if sheet_name in sheet_titles:
            # If the sheet exists, open it
            print(f"Sheet '{sheet_name}' found, updating data...")
            sheet = spreadsheet.worksheet(sheet_name)
        else:
            # If the sheet does not exist, create it
            print(f"Sheet '{sheet_name}' not found, creating a new sheet...")
            sheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")

        # Load the CSV file into a pandas DataFrame
        print(f"Reading CSV file from: {csv_file_path}")
        df = pd.read_csv(csv_file_path)

        # Convert the DataFrame into a list of lists
        data = df.values.tolist()

        # Logging to check what data we're uploading
        print(
            f"Data to upload (first 5 rows): {data[:5]}"
        )  # Print first 5 rows of data

        # Clear existing contents of the sheet (if any)
        print(f"Clearing existing data from the sheet: {sheet_name}")
        sheet.clear()

        # Update the sheet with the CSV data
        print(f"Uploading data to sheet: {sheet_name}")
        sheet.update(
            [df.columns.values.tolist()] + data
        )  # First row is header, then data

        print(
            f"Successfully uploaded the CSV data to {spreadsheet_name} - {sheet_name}."
        )

    except Exception as e:
        print(f"Error uploading CSV to sheet: {e}")


def save_sheet_to_csv(sheets_client, spreadsheet_name, worksheet_name, output_csv_file):
    """Fetches a Google Sheet worksheet and saves it as a CSV."""
    # Open the Google Sheet
    sheet = sheets_client.open(spreadsheet_name)

    # Select the worksheet by name
    worksheet = sheet.worksheet(worksheet_name)

    # Get all values from the worksheet
    data = worksheet.get_all_values()

    # Save the data as a CSV file locally
    with open(output_csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(
        f"Sheet '{worksheet_name}' from '{spreadsheet_name}' saved to {output_csv_file}"
    )
