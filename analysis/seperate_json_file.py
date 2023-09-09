import os
import shutil
from urllib.parse import urlparse

import pandas as pd

def get_domain():
    directory = '../merged_csv/'  # Replace with the path to your directory

    # List all CSV files in the directory
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
    # csv_files = [file for file in os.listdir(directory) if file == '地方所属网站.csv']
    all_domain = []

    print(csv_files)
    print(len(csv_files))
    for file in csv_files:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)

        # Extract the fourth column as the domain name
        domain_column = df.iloc[:, 3]  # Assuming the fourth column is at index 3 (zero-based)
        directory_name = file.split('.csv')[0]
        print(directory_name)
        # Process each domain name
        for domain in domain_column:
            processed_domain = process_domain(domain)
            filename = f"./whois_result/{processed_domain.split('//')[1]}.json"
            if os.path.isfile(filename):
                destination_dir = os.path.join('./class', directory_name)
                os.makedirs(destination_dir, exist_ok=True)
                destination_path = os.path.join(destination_dir, f"{processed_domain.split('//')[1]}.json")
                shutil.copy(filename, destination_path)


def process_domain(domain):
    # Add "http://" to domain names that don't have it
    if not domain.startswith("http"):
        domain = "http://" + domain

    # Parse the URL and extract the base domain
    parsed_url = urlparse(domain)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc

    return base_url

get_domain()