import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("fixed_file.csv")


# Check for NaN values in the DataFrame
print(df.isna().sum())

# Optionally, print the rows containing NaN values
print(df[df.isna().any(axis=1)])

# Replace 'Select category' and empty values with 'Uncategorized'
# df["category"] = df["category"].replace(["Select category", ""], "Uncategorized")

# # Verify the replacement
# print("Updated 'category' column:")
# print(df["category"].head())

# # Save the fixed DataFrame back to a CSV file
# df.to_csv("fixed_file.csv", index=False)
