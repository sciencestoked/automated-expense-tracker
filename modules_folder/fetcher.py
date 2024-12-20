# modules_folder/fetcher.py
# from translate import Translator
import re
import time
from datetime import datetime, timedelta

def fetch_jdebit_emails(service, days=None, start_date=None, end_date=None):
    now = time.time()
    query = 'from:yuchodebit@jp-bank.japanpost.jp '


    # If days is provided, fetch emails from the last X days
    if days is not None:
        after_date = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
        query += f' after:{after_date}'

    # If a specific start_date and/or end_date is provided, use them
    if start_date:
        query += f' after:{start_date.strftime("%Y/%m/%d")}'
    if end_date:
        query += f' before:{end_date.strftime("%Y/%m/%d")}'


    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    
    extracted_data = []
    
    if not messages:
        print("No messages found.")
        return []
    else:
        print("Messages Found !!")
    
    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        email_body = message['snippet']

        # Skip emails containing "ご利用いただけません" (failure)
        if "ご利用いただけません" in email_body:
            continue
        
        # Extract date, vendor, and amount using regex
        date_time = re.search(r'利用日時\s+([\d/: ]+)', email_body)
        vendor = re.search(r'利用店舗\s+(.+?)利用金額', email_body)  # Modified vendor regex
        amount = re.search(r'利用金額\s+(\d+)円', email_body)
        
        if date_time and vendor and amount:
            date_time = date_time.group(1)
            date_val, time_val = date_time.split(' ', 1)
            
            vendor = vendor.group(1)
            amount = int(amount.group(1))
            
            # Add the extracted data
            extracted_data.append({
                'date': date_val,
                'time': time_val,
                'vendor': vendor,
                'amount': amount
            })
    print(f' Total time for API : {time.time()-now}')

    return extracted_data


if __name__ == "__main__":
    now = time.time()

    from auth import authenticate_gmail
    service = authenticate_gmail()
    results = fetch_jdebit_emails(service, days = 5)
    # translator= Translator(to_lang="en")

    print(f" Total script time = {time.time()-now}")
    
    # now = time.time()

    for x in results:
        res_str = (f' Date : {x['date']} \n Time : {x['time']} \n Vendor : {x['vendor']} \n Amount : {x['amount']} \n- - - - - - - - - - - - - - -\n')
        # trans_str = translator.translate(res_str)
        # print (trans_str)

        print (res_str)
    
    # print(f" Total translate time = {time.time()-now}")

  