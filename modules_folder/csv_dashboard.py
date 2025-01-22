import streamlit as st
import pandas as pd

# Function to load the CSV data
def load_csv(csv_file):
    """Load the CSV file into a DataFrame."""
    return pd.read_csv(csv_file)

# Function to save the modified DataFrame back to CSV
def save_csv(df, csv_file):
    """Save the DataFrame back to the specified CSV file."""
    df.to_csv(csv_file, index=False)

# Predefined list of categories for the dropdown
CATEGORY_LIST = ['Select category', 'Food', 'Transport', 'Grocery', 'Entertainment', 'Other']

# Function to display the CSV data in an interactive dashboard
def display_csv_dashboard(csv_file):
    """Display the CSV file data in a Streamlit dashboard with edit functionality."""
    
    # Load the CSV data
    df = load_csv(csv_file)
    
    # Display the CSV header
    st.write("### CSV Data with Editable Categories")
    
    # Dictionary to hold the updated categories
    category_editors = {}
    
    # Create a header for the table
    cols = st.columns([1, 2, 2, 2, 3])
    cols[0].write("Index")
    cols[1].write("Date")
    cols[2].write("Time")
    cols[3].write("Vendor")
    cols[4].write("Category")
    
    # Loop through the DataFrame and create dropdowns for each row
    for idx, row in df.iterrows():
        cols = st.columns([1, 2, 2, 2, 3])
        
        # Display the data from the row in the first few columns
        cols[0].write(idx + 1)  # Display index number
        cols[1].write(row['date'])  # Display date
        cols[2].write(row['time'])  # Display time
        cols[3].write(row['vendor'])  # Display vendor
        
        # Create the dropdown for the category column
        category_editors[idx] = cols[4].selectbox(
            " ",  # Provide a placeholder label (can be a space)
            CATEGORY_LIST,
            index=CATEGORY_LIST.index(row['category']) if row['category'] in CATEGORY_LIST else 0,
            key=idx,
            label_visibility="hidden"  # Hide the label for accessibility purposes
        )
    
    # Save the changes when the button is clicked
    if st.button('Save Changes'):
        for idx, new_category in category_editors.items():
            # If the user selects "Select Category", replace it with None or empty string before saving
            df.at[idx, 'category'] = new_category if new_category != "Select category" else None
        
        # Save the updated dataframe back to the CSV
        save_csv(df, csv_file)
        st.success(f"Changes saved successfully to {csv_file}!")

if __name__ == '__main__':
    display_csv_dashboard("./data/csvs/All_expenses_till_now_expenses.csv")
