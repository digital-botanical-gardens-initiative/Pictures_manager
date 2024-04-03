import pandas as pd

# Read the CSV file
df = pd.read_csv("C:/Users/edoua/Desktop/correction.csv")

# Create an empty list to store rows of the new DataFrame
new_rows = []

# Loop over the DataFrame row by row
for index, row in df.iterrows():
    if ',' in row['sample_id']:
        # Split the sample_id by comma
        parts = row['sample_id'].split(', ')
        
        # Create two new rows with the parts before and after the comma
        new_row_1 = row.copy()
        new_row_1['sample_id'] = parts[0]
        new_rows.append(new_row_1)
        
        new_row_2 = row.copy()
        new_row_2['sample_id'] = parts[1]
        new_rows.append(new_row_2)
    else:
        # If sample_id doesn't contain a comma, simply append the original row
        new_rows.append(row)

# Create a new DataFrame from the list of rows
new_df = pd.DataFrame(new_rows)

# Write the DataFrame to a CSV file
new_df.to_csv("new_dataframe.csv", index=False)
