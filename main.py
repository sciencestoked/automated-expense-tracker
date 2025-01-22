# main.py

from modules_folder.auth import authenticate_gmail_and_sheets
from modules_folder.fetcher import fetch_email_data
from modules_folder.save_utils import (
    save_to_csv_force,
    save_to_csv_update,
    save_to_json,
)  # noqa: F401
from modules_folder.sheets_module import upload_csv_to_sheet

if __name__ == "__main__":
    # Authenticate and get Gmail service
    gmail_service, sheets_client = authenticate_gmail_and_sheets()

    # Fetch JDebit emails
    extracted_data = fetch_email_data(gmail_service)

    if extracted_data:
        # Print extracted data
        # for x in extracted_data:
        #     print(f' Date : {x['date']} \n Time : {x['time']} \n Vendor : {x['vendor']} \n Amount : {x['amount']} \n- - - - - - - - - - - - - - - - -\n')

        # Save to CSV and JSON
        save_to_csv_update(extracted_data)
        save_to_json(extracted_data)
    else:
        print("No JDebit data to save.")

    csv_file_path = "./data/csvs/All_expenses_till_now_expenses.csv"
    spreadsheet_name = "Budgeting"
    sheet_name = "All_expenses_till_now_expenses"  # Optional, defaults to "Sheet1"

    upload_csv_to_sheet(sheets_client, spreadsheet_name, csv_file_path, sheet_name)
