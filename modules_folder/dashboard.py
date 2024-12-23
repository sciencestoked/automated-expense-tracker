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

# Function to display the CSV data in an interactive dashboard
def display_csv_dashboard(csv_file):
    """Display the CSV file data in a Streamlit dashboard with edit functionality."""
    
    # Load the CSV data
    df = load_csv(csv_file)
    
    # Display the data in a table
    st.write("### CSV Data")
    st.dataframe(df)
    
    # Allow users to edit the 'category' column
    st.write("### Edit Categories")
    
    # Dictionary to hold the updated categories
    category_editors = {}
    
    # Create input fields for each row in the 'category' column
    for idx, row in df.iterrows():
        category_editors[idx] = st.text_input(f"Edit category for row {idx+1}", row['category'], key=idx)
    
    # Save the changes when the button is clicked
    if st.button('Save Changes'):
        for idx, new_category in category_editors.items():
            df.at[idx, 'category'] = new_category  # Update the category in the dataframe
        
        # Save the updated dataframe back to the CSV
        save_csv(df, csv_file)
        st.success(f"Changes saved successfully to {csv_file}!")

if __name__ == '__main__':
    display_csv_dashboard("./data/csvs/All_expenses_till_now_expenses.csv")