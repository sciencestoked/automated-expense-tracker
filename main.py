# main.py

from modules_folder.auth import authenticate_gmail
from modules_folder.fetcher import fetch_jdebit_emails
from modules_folder.save_utils import save_to_csv, save_to_json

if __name__ == '__main__':
    # Authenticate and get Gmail service
    service = authenticate_gmail()
    
    # Fetch JDebit emails
    extracted_data = fetch_jdebit_emails(service)
    
    if extracted_data:
        # Print extracted data
        for x in extracted_data:
            print(f' Date : {x['date']} \n Time : {x['time']} \n Vendor : {x['vendor']} \n Amount : {x['amount']} \n- - - - - - - - - - - - - - - - -\n')
        
        # Save to CSV and JSON
        save_to_csv(extracted_data)
        save_to_json(extracted_data)
    else:
        print("No JDebit data to save.")
