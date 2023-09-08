# I have a directory called merger_csv, under the directory, i have a lot of csv file, every csv file has the same header, read the 4th column, skip the first row since it is a header.
# and read each row, each row is a url, please remove the prefix like http:// https:// and to judge if a file called the row removed prefix and end up with .txt in response directory,
# if in, put the file into a directory as the same name with .csv file.
import concurrent
import os
import shutil
from urllib.parse import urlparse

import pandas as pd


# import os
# import shutil
#
# # Specify the source directory where the files are located
# source_directory = "./response"
#
# # Define the destination directories
# destination_directories = {}
#
# # Loop through the files in the source directory
# for filename in os.listdir(source_directory):
#     if filename.endswith(".txt"):
#         # Extract the domain name from the file name
#         domain_parts = filename.split(".")
#
#         # Check if the file name has at least four parts (including .txt)
#         if len(domain_parts) >= 4:
#             domain_name_parts = domain_parts[-4:-1]
#             domain_name = ".".join(domain_name_parts)
#         else:
#             # If the file name doesn't have enough parts, skip the file
#             continue
#
#         # Create the destination directory if it doesn't exist
#         if domain_name not in destination_directories:
#             destination_directory = os.path.join('domain_directory', domain_name)
#             os.makedirs(destination_directory, exist_ok=True)
#             destination_directories[domain_name] = destination_directory
#         else:
#             destination_directory = destination_directories[domain_name]
#
#         # Move the file to the destination directory
#         source_path = os.path.join(source_directory, filename)
#         destination_path = os.path.join(destination_directory, filename)
#         shutil.copy(source_path, destination_path)


def get_domain():
    directory = '../merged_csv/'  # Replace with the path to your directory

    # List all CSV files in the directory
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
    all_domain = []
    failed_domains = []
    for file in csv_files:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path, skiprows=1)

        # Extract the fourth column as the domain name
        domain_column = df.iloc[:, 3]  # Assuming the fourth column is at index 3 (zero-based)

        # Process each domain name
        for domain in domain_column:
            processed_domain = process_domain(domain)
            filename = f"./response/{processed_domain.split('//')[1]}.txt"
            if os.path.isfile(filename):
                print(f"File already exists: {filename}")
                # Move the file to the destination directory
                source_path = os.path.join(filename, filename)
                # Todo
                destination_path = os.path.join(file.split('.csv')[0], filename)
                shutil.copy(source_path, destination_path)

            all_domain.append(processed_domain)
    return all_domain


def process_domain(domain):
    # Add "http://" to domain names that don't have it
    if not domain.startswith("http"):
        domain = "http://" + domain

    # Parse the URL and extract the base domain
    parsed_url = urlparse(domain)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc

    return base_url