# import pandas as pd
# import os
#
# # Directory containing the CSV files
# directory = './total_csv'
#
# # Get a list of all CSV files in the directory
# csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
#
# # Dictionary to store the merged dataframes
# merged_dataframes = {}
#
# # Iterate over each CSV file
# for csv_file in csv_files:
#     # Extract the prefix before the first underscore as the key
#     key = csv_file.split('_')[0]
#
#     # Get the full file path
#     file_path = os.path.join(directory, csv_file)
#
#     # Check if the file is empty
#     if os.path.getsize(file_path) == 0:
#         print(f"Skipping empty file: {csv_file}")
#         continue
#
#     # Read the CSV file into a dataframe
#     df = pd.read_csv(file_path)
#
#     # Check if the key already exists in the dictionary
#     if key in merged_dataframes:
#         # Append the current dataframe to the existing one
#         merged_dataframes[key] = pd.concat([merged_dataframes[key], df], ignore_index=True)
#     else:
#         # Add the dataframe to the dictionary
#         merged_dataframes[key] = df
#
# # Write the merged dataframes to separate CSV files
# for key, df in merged_dataframes.items():
#     output_file = os.path.join(directory, f"{key}.csv")
#     df.to_csv(output_file, index=False)
#     print(f"Merged CSV file '{output_file}' created.")


import pandas as pd
import os

# Directory containing the CSV files
directory = './total_csv'

# Get a list of all CSV files in the directory
csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

# Dictionary to store the merged dataframes
merged_dataframes = {}

# Iterate over each CSV file
for csv_file in csv_files:
    # Extract the prefix before the first underscore as the key
    key = csv_file.split('_')[0]

    # Get the full file path
    file_path = os.path.join(directory, csv_file)

    # Check if the file is empty
    if os.path.getsize(file_path) == 0:
        print(f"Skipping empty file: {csv_file}")
        continue

    try:
        # Read the CSV file into a dataframe using the latin-1 encoding
        df = pd.read_csv(file_path, encoding='utf-8')

        # Check if the key already exists in the dictionary
        if key in merged_dataframes:
            # Append the current dataframe to the existing one
            merged_dataframes[key] = pd.concat([merged_dataframes[key], df], ignore_index=True)
        else:
            # Add the dataframe to the dictionary
            merged_dataframes[key] = df

    except UnicodeDecodeError:
        print(f"Error reading file: {csv_file}. Skipping file due to encoding issue.")

# Write the merged dataframes to separate CSV files
for key, df in merged_dataframes.items():
    if not key.endswith(".csv"):
        key += ".csv"
    output_file = os.path.join('./merged_csv', key)
    df.to_csv(output_file, index=False)
    print(f"Merged CSV file '{output_file}' created.")

