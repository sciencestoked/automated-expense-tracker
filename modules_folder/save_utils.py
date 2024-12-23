# modules_folder/save_utils.py

import os
import csv
import json
from datetime import datetime, timedelta

# Helper function to get the filename based on the date range
def get_date_range_filename(days=None):
    if not days:
        return "All_expenses_till_now"
    
    today = datetime.today()
    start_date = today - timedelta(days=days)
    start_date_str = start_date.strftime('%Y-%m-%d')
    
    if days == 0:
        filename_suffix = f'{start_date_str}_to_{start_date_str}'
    else:
        today_str = today.strftime('%Y-%m-%d')
        filename_suffix = f'{start_date_str}_to_{today_str}'
    
    return filename_suffix

# Function to forcefully rewrite all data
def save_to_csv_force(data, days=None, base_dir='../data/csvs/'):
    if not data:
        return
    
    # Ensure the data directory exists
    os.makedirs(base_dir, exist_ok=True)
    
    # Get the appropriate filename based on the date range
    filename_suffix = get_date_range_filename(days)
    csv_file = os.path.join(base_dir, f'{filename_suffix}_expenses.csv')
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'time', 'vendor', 'amount', 'category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            row.setdefault('category', '')  # Add empty 'category' if not present
            writer.writerow(row)
    
    print(f"Data forcefully saved to {csv_file}")

# Function to update only with new rows (no overwriting of existing rows)
def save_to_csv_update(data, days=None, base_dir='../data/csvs/'):
    if not data:
        return
    
    # Ensure the data directory exists
    os.makedirs(base_dir, exist_ok=True)
    
    # Get the appropriate filename based on the date range
    filename_suffix = get_date_range_filename(days)
    csv_file = os.path.join(base_dir, f'{filename_suffix}_expenses.csv')
    
    # Load existing data if the file exists
    existing_data = []
    if os.path.exists(csv_file):
        with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            existing_data = [row for row in reader]

    # Convert existing data to a set of tuples (date, time) for faster lookup
    existing_entries = set((row['date'], row['time']) for row in existing_data)

    # Filter new data based on whether (date, time) already exists
    new_rows = [row for row in data if (row['date'], row['time']) not in existing_entries]

    if new_rows:
        with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['date', 'time', 'vendor', 'amount', 'category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write new rows
            for row in new_rows:
                row.setdefault('category', '')  # Add empty 'category' if not present
                writer.writerow(row)
        
        print(f"Added {len(new_rows)} new rows to {csv_file}")
    else:
        print(f"No new rows to add to {csv_file}")

# Function to forcefully save all data to JSON
def save_to_json(data, days=None, base_dir='../data/jsons/'):
    if not data:
        return
    
    # Ensure the data directory exists
    os.makedirs(base_dir, exist_ok=True)
    
    filename_suffix = get_date_range_filename(days)
    json_file = os.path.join(base_dir, f'{filename_suffix}_expenses.json')
    
    with open(json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {json_file}")
