import re
import time
from datetime import datetime, timedelta
# from email.utils import parsedate_to_datetime

def fetch_email_data(service, days=None, start_date=None, end_date=None):
    now = time.time()
    query = 'from:yuchodebit@jp-bank.japanpost.jp '
    # For manual expenses (from your personal account)
    manual_query = 'from:s-singhal@ugo.plus'

    # If days is provided, fetch emails from the last X days
    if days is not None:
        after_date = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
        query += f' after:{after_date}'
        manual_query += f' after:{after_date}'  # Same filter for personal emails

    # If a specific start_date and/or end_date is provided, use them
    if start_date:
        query += f' after:{start_date.strftime("%Y/%m/%d")}'
        manual_query += f' after:{start_date.strftime("%Y/%m/%d")}'
    if end_date:
        query += f' before:{end_date.strftime("%Y/%m/%d")}'
        manual_query += f' before:{end_date.strftime("%Y/%m/%d")}'

    # Fetch emails
    results = service.users().messages().list(userId='me', q=query).execute()
    manual_results = service.users().messages().list(userId='me', q=manual_query).execute()

    messages = results.get('messages', [])
    manual_messages = manual_results.get('messages', [])
    
    extracted_data = []
    
    if not messages and not manual_messages:
        print("No messages found.")
        return []
    else:
        print("Messages Found !!")
    
    # Process JDebit emails
    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        email_body = message['snippet']

        # Skip emails containing "ご利用いただけません" (failure)
        if "ご利用いただけません" in email_body:
            continue
        
        # Extract date, vendor, and amount using regex for JDebit emails
        date_time = re.search(r'利用日時\s+([\d/: ]+)', email_body)
        vendor = re.search(r'利用店舗\s+(.+?)利用金額', email_body)  # Modified vendor regex
        amount = re.search(r'利用金額\s+(\d+)円', email_body)
        
        if date_time and vendor and amount:
            date_time = date_time.group(1)
            date_val, time_val = date_time.split(' ', 1)
            
            vendor = vendor.group(1)
            amount = int(amount.group(1))
            
            # Add the extracted JDebit data
            extracted_data.append({
                'date': date_val,
                'time': time_val,
                'vendor': vendor,
                'amount': amount,                
                'category':'Select category'
            })

    # Process manual expense emails from personal account (s-singhal@ugo.plus)
    for msg in manual_messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        email_body = message['snippet']
        
        email_timestamp = int(message['internalDate']) / 1000  # Convert from milliseconds to seconds
        email_date = datetime.fromtimestamp(email_timestamp)  # Convert timestamp to datetime

        # Extract vendor and amount from manual emails (simple assumption)
        vendor = re.search(r'Vendor[\s=:]*([a-zA-Z\s]+)', email_body, re.IGNORECASE)
        amount = re.search(r'Amount[\s=:]*([\d]+)', email_body, re.IGNORECASE)


        if vendor and amount:
            vendor_name = vendor.group(1).strip()
            amount_value = int(amount.group(1).strip())

            # Use the email timestamp for date and time
            date_str = email_date.strftime('%Y-%m-%d')
            time_str = email_date.strftime('%H:%M:%S')

            # Add the extracted manual expense data
            extracted_data.append({
                'date': date_str,
                'time': time_str,
                'vendor': vendor_name,
                'amount': amount_value,
                'category':'Select category'
            })
    
    print(f'Total time for API: {time.time() - now}')

    return extracted_data


if __name__ == "__main__":
    now = time.time()

    from auth import authenticate_gmail
    service = authenticate_gmail()
    results = fetch_email_data(service, days=0)

    print(f"Total script time = {time.time() - now}")

    # Process and print results
    for x in results:
        res_str = (f'Date: {x["date"]}\nTime: {x["time"]}\nVendor: {x["vendor"]}\nAmount: {x["amount"]}\n- - - - - - - - - - - - - - -\n')
        print(res_str)
