from modules_folder.auth import authenticate_gmail_and_sheets
from modules_folder.sheets_module import upload_csv_to_sheet, save_sheet_to_csv
from modules_folder.fetcher import fetch_email_data
from modules_folder.save_utils import (
    save_to_csv_force,
    save_to_csv_update,
    save_to_json,
)  # noqa: F401


if __name__ == "__main__":

    csv_file_path = "./data/csvs/All_expenses_till_now_expenses.csv"
    spreadsheet_name = "Budgeting"
    sheet_name = "All_expenses_till_now_expenses"
    output_csv_file = "./data/csvs/All_expenses_till_now_expenses.csv"

    # Authenticate and get Gmail service and Google Sheets client
    gmail_service, sheets_client = authenticate_gmail_and_sheets()

    sheets_to_local_bool = (
        input(
            "Want to load data from google sheets and update the local csv? (Y/n) "
        ).lower()
        != "n"
    )
    if sheets_to_local_bool:
        print("Google Sheets to Local csv Download YESSSS")
        save_sheet_to_csv(sheets_client, spreadsheet_name, sheet_name, output_csv_file)

    gmail_to_local_bool = (
        input("Want to load data from Gmail and update the local csv? (Y/n) ").lower()
        != "n"
    )
    if gmail_to_local_bool:
        print("Gmail to Local Download YESSSS")
        # Fetch JDebit emails
        extracted_data = fetch_email_data(gmail_service)
        if extracted_data:
            # Save to CSV and JSON
            save_to_csv_update(extracted_data)
            save_to_json(extracted_data)
        else:
            print("No JDebit data to save.")

    local_to_sheets_bool = (
        input("Want to push the local data csv to google sheets? (Y/n) ").lower() != "n"
    )
    if local_to_sheets_bool:
        print("Local to Google Sheets upload YESSSS")
        upload_csv_to_sheet(sheets_client, spreadsheet_name, csv_file_path, sheet_name)
