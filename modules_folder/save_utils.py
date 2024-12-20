# modules_folder/save_utils.py

import os
import csv
import json
from datetime import datetime, timedelta

def get_date_range_filename(days=None):
    if not days:
        return "All_expenses_till_now"
    # Calculate the date range based on the number of days
    today = datetime.today()
    start_date = today - timedelta(days=days)  # Calculate the starting date
    start_date_str = start_date.strftime('%Y-%m-%d')
    
    if days == 0:
        # If 0 days, just use today's date
        filename_suffix = f'{start_date_str}_to_{start_date_str}'
    else:
        # For days > 0, use the start date and today as the range
        today_str = today.strftime('%Y-%m-%d')
        filename_suffix = f'{start_date_str}_to_{today_str}'
    
    return filename_suffix

def save_to_csv(data, days=None, base_dir='../data/csvs/'):
    if not data:
        return
    
    # Ensure the data directory exists
    os.makedirs(base_dir, exist_ok=True)
    
    # Get the appropriate filename based on the date range
    filename_suffix = get_date_range_filename(days)
    csv_file = os.path.join(base_dir, f'{filename_suffix}_expenses.csv')
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'time', 'vendor', 'amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    print(f"Data saved to {csv_file}")

def save_to_json(data, days=None, base_dir='../data/jsons'):
    if not data:
        return
    
    # Ensure the data directory exists
    os.makedirs(base_dir, exist_ok=True)
    
    # Get the appropriate filename based on the date range
    filename_suffix = get_date_range_filename(days)
    json_file = os.path.join(base_dir, f'{filename_suffix}_expenses.json')
    
    with open(json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {json_file}")
