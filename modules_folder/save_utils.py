import os
import pandas as pd
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
def save_to_csv_force(data, days=None, base_dir='./data/csvs/'):
    if not data:
        return
    
    # Ensure the data directory exists
    os.makedirs(base_dir, exist_ok=True)
    
    # Convert list of dicts to pandas DataFrame
    df = pd.DataFrame(data)
    
    # Get the appropriate filename based on the date range
    filename_suffix = get_date_range_filename(days)
    csv_file = os.path.join(base_dir, f'{filename_suffix}_expenses.csv')
    
    # Save DataFrame to CSV
    df.to_csv(csv_file, index=False)
    
    print(f"Data forcefully saved to {csv_file}")

# Function to update only with new rows (no overwriting of existing rows)
def save_to_csv_update(data, days=None, base_dir='./data/csvs/'):
    if not data:
        return
    
    # Ensure the data directory exists
    os.makedirs(base_dir, exist_ok=True)
    
    # Convert list of dicts to pandas DataFrame
    new_data_df = pd.DataFrame(data)
    
    # Get the appropriate filename based on the date range
    filename_suffix = get_date_range_filename(days)
    csv_file = os.path.join(base_dir, f'{filename_suffix}_expenses.csv')
    
    # Check if the CSV file already exists
    if os.path.exists(csv_file):
        existing_data_df = pd.read_csv(csv_file)
        
        # Merge new data with existing data, avoiding duplicates by 'date' and 'time'
        combined_df = pd.concat([existing_data_df, new_data_df]).drop_duplicates(subset=['date', 'time'], keep='first')
    else:
        combined_df = new_data_df
    
    # Save updated data to CSV
    combined_df.to_csv(csv_file, index=False)
    
    print(f"Data updated and saved to {csv_file}")

# Function to forcefully save all data to JSON
def save_to_json(data, days=None, base_dir='./data/jsons/'):
    if not data:
        return
    
    # Ensure the data directory exists
    os.makedirs(base_dir, exist_ok=True)
    
    filename_suffix = get_date_range_filename(days)
    json_file = os.path.join(base_dir, f'{filename_suffix}_expenses.json')
    
    # Save data as JSON
    pd.DataFrame(data).to_json(json_file, orient='records', indent=4)
    
    print(f"Data saved to {json_file}")
