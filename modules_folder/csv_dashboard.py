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
CATEGORY_LIST = [ 'Select category', 'Food', 'Transport', 'Grocery', 'Entertainment', 'Other']

# Function to display the CSV data in an interactive dashboard
def display_csv_dashboard(csv_file):
    """Display the CSV file data in a Streamlit dashboard with edit functionality."""
    
    # Load the CSV data
    df = load_csv(csv_file)
    
    # Display the data in a table
    st.write("### CSV Data")
    st.dataframe(df)
    
    # Allow users to edit the 'category' column using a dropdown
    st.write("### Edit Categories")
    
    # Dictionary to hold the updated categories
    category_editors = {}
    
    # Create dropdowns for each row in the 'category' column
    for idx, row in df.iterrows():
        category_editors[idx] = st.selectbox(
            f"Select category for row {idx+1}",
            CATEGORY_LIST,
            index=CATEGORY_LIST.index(row['category']) if row['category'] in CATEGORY_LIST else 0,
            key=idx
        )
    
    # Save the changes when the button is clicked
    if st.button('Save Changes'):
        for idx, new_category in category_editors.items():
            # If the user selects "Select Category", replace it with None or empty string before saving
            df.at[idx, 'category'] = new_category if new_category != "Select Category" else None
        
        # Save the updated dataframe back to the CSV
        save_csv(df, csv_file)
        st.success(f"Changes saved successfully to {csv_file}!")

if __name__ == '__main__':
    display_csv_dashboard("./data/csvs/All_expenses_till_now_expenses.csv")