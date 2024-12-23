# main.py
import streamlit as st
from modules_folder.csv_dashboard import display_csv_dashboard

from modules_folder.auth import authenticate_gmail
from modules_folder.fetcher import fetch_email_data
from modules_folder.save_utils import save_to_csv_force, save_to_csv_update, save_to_json  # noqa: F401

if __name__ == '__main__':
    # Authenticate and get Gmail service
    service = authenticate_gmail()
    
    # Fetch JDebit emails
    extracted_data = fetch_email_data(service)
    
    if extracted_data:
        # Print extracted data
        # for x in extracted_data:
        #     print(f' Date : {x['date']} \n Time : {x['time']} \n Vendor : {x['vendor']} \n Amount : {x['amount']} \n- - - - - - - - - - - - - - - - -\n')
        
        # Save to CSV and JSON
        save_to_csv_update(extracted_data)
        save_to_json(extracted_data)

        # Set your CSV file path here
        csv_file_path = './data/csvs/All_expenses_till_now_expenses.csv'

        # Display the dashboard
        display_csv_dashboard(csv_file_path)

    else:
        print("No JDebit data to save.")
