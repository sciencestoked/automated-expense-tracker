import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load and clean the CSV data
def load_and_clean_data(csv_file):
    df = pd.read_csv(csv_file)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  # Ensure 'amount' is numeric
    df['date'] = pd.to_datetime(df['date'], errors='coerce')     # Ensure 'date' is datetime
    df = df.dropna(subset=['category', 'amount', 'date'])        # Drop rows with missing values
    return df

# Function to generate expense insights
def generate_expense_insights(df):
    total_expense = df['amount'].sum()
    print(f"Total Expense: {total_expense}")

    category_expense = df.groupby('category')['amount'].sum().reset_index()
    print("\nCategory-wise Expense Breakdown:\n", category_expense)

    monthly_expense = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().reset_index()
    print("\nMonthly Expense Breakdown:\n", monthly_expense)

# Function to plot category-wise expense breakdown (Pie chart)
def plot_category_pie_chart(df):
    category_expense = df.groupby('category')['amount'].sum().reset_index()
    plt.figure(figsize=(8, 8))
    plt.pie(category_expense['amount'], labels=category_expense['category'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3'))
    plt.title('Category-wise Expense Breakdown', fontsize=16)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

# Function to plot monthly expense trends (Line chart)
def plot_monthly_trend(df):
    df['month'] = df['date'].dt.to_period('M')
    monthly_expense = df.groupby('month')['amount'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=monthly_expense['month'].astype(str), y=monthly_expense['amount'], marker='o', color='b', linewidth=2.5)
    plt.title('Monthly Expense Trend', fontsize=16)
    plt.xlabel('Month')
    plt.ylabel('Total Expense')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Function to plot category-wise expenses as a bar chart
def plot_category_bar_chart(df):
    category_expense = df.groupby('category')['amount'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x='amount', y='category', data=category_expense, palette='coolwarm')
    plt.title('Category-wise Total Expenses', fontsize=16)
    plt.xlabel('Total Expense')
    plt.ylabel('Category')
    plt.tight_layout()
    plt.show()

# Function to analyze daily expenses (Box plot for variance)
def plot_daily_expense_distribution(df):
    df['day'] = df['date'].dt.day_name()
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='day', y='amount', data=df, palette='Set2')
    plt.title('Daily Expense Distribution (By Day of the Week)', fontsize=16)
    plt.xlabel('Day of the Week')
    plt.ylabel('Expense Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to generate all plots for expense analysis
def analyze_expenses(csv_file):
    # Load and clean the data
    df = load_and_clean_data(csv_file)
    
    # Display expense insights in the console
    generate_expense_insights(df)
    
    # Generate visualizations
    plot_category_pie_chart(df)           # Category-wise expense (Pie Chart)
    plot_monthly_trend(df)                # Monthly expense trends (Line Chart)
    plot_category_bar_chart(df)           # Category-wise expense breakdown (Bar Chart)
    plot_daily_expense_distribution(df)   # Daily variance of expenses (Box Plot)

# Main execution
if __name__ == '__main__':
    csv_file = "./data/csvs/All_expenses_till_now_expenses.csv"  # Replace with your actual file path
    analyze_expenses(csv_file)
