import pandas as pd

# Load the newly uploaded Excel file
file_path_new = 'Import_trade_data.xlsx'
trade_data_new = pd.ExcelFile(file_path_new)

# Load the first sheet
data_new = trade_data_new.parse('Sheet1')

# Clean the data
# Convert trade value columns to numeric (removing commas and handling NaNs)
data_cleaned_new = data_new.copy()
for col in data_cleaned_new.columns[3:]:  # Assuming year columns start from the 4th column
    data_cleaned_new[col] = (
        data_cleaned_new[col]
        .replace(",", "", regex=True)
        .replace("-", None)
        .astype(float)
    )

# Reshape the data for easier plotting (from wide to long format)
data_long_new = data_cleaned_new.melt(
    id_vars=["Commodity"], 
    var_name="Year", 
    value_name="Trade Value (USD)"
)

# Filter out invalid rows where 'Year' or 'Trade Value (USD)' is not valid
data_filtered_new = data_long_new[
    data_long_new["Year"].str.contains(r"\d{4}-\d{4}", na=False) &  # Year range format
    data_long_new["Trade Value (USD)"].notna()                      # Non-null trade values
]

# Convert trade values to numeric
data_filtered_new["Trade Value (USD)"] = data_filtered_new["Trade Value (USD)"].astype(float)

# Save the cleaned data to a new file
cleaned_file_path = 'cleaned_Import_trade_data.xlsx'
data_filtered_new.to_excel(cleaned_file_path, index=False)

cleaned_file_path
