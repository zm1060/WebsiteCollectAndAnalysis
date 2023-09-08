import os
from urllib.parse import urlparse

import pandas as pd
import requests
import concurrent.futures

import urllib3


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
            all_domain.append(processed_domain)

    # Request and store the website responses using multi-threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(store_response, all_domain)

        # Collect the failed domains
        for domain, result in zip(all_domain, results):
            if not result:
                failed_domains.append(domain)

    # Save the failed domains to a file
    save_failed_domains(failed_domains)

    return all_domain



def process_domain(domain):
    # Add "http://" to domain names that don't have it
    if not domain.startswith("http"):
        domain = "http://" + domain

    # Parse the URL and extract the base domain
    parsed_url = urlparse(domain)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc

    return base_url


def store_response(domain):
    try:
        headers = {
            'Connection': 'close',
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
        }
        filename = f"./response/{domain.split('//')[1]}.txt"
        if os.path.isfile(filename):
            print(f"File already exists: {filename}")
            return True

        # response = requests.get(domain, stream=True, headers=headers, verify='../venv/lib/python3.10/site-packages/certifi/cacert.pem', timeout=5, allow_redirects=True)
        response = requests.get(domain, stream=True, headers=headers, verify=False, timeout=5, allow_redirects=True)

        if response.status_code == 200:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"Response stored: {filename}")
            response.close()
            return True
        else:
            print(f"Failed to request website: {domain} (Status code: {response.status_code})")
            response.close()
            return False
    except requests.exceptions.RequestException as e:
        print(f"Failed to request website: {domain} ({str(e)})")
        return False

# def store_response(domain):
#     try:
#         #
#         # brefore return, please close the request.
#         # and add header to request
#         # tls configuration
#         # headers = {'connection':'close','User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
#         # response = requests.get(domain, straem=True,headers=headers, verify=False，timeout=5)
#         response = requests.get(domain, stream=True)
#         if response.status_code == 200:
#             # Save the HTTP response to a file in the html directory
#             filename = f"./response/{domain.split('//')[1]}.txt"
#             #
#             # If file exisits, return True
#             with open(filename, "w", encoding="utf-8") as file:
#                 file.write(response.text)
#             print(f"Response stored: {filename}")
#             # response.close()
#             return True
#         else:
#             print(f"Failed to request website: {domain} (Status code: {response.status_code})")
#             # response.close()
#             return False
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to request website: {domain} ({str(e)})")
#         # response.close()
#         return False


def save_failed_domains(failed_domains):
    with open("failed_domains.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(failed_domains))


urllib3.disable_warnings()
# Call get_domain() to start the process
get_domain()







