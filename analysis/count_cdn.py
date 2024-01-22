import json
import os
from urllib.parse import urlparse
import subprocess
import concurrent.futures
from tqdm import tqdm


def extract_domain(url):
    if not url.startswith("http"):
        url = "http://" + url
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


def extract_addresses(lines, start_index):
    addresses = []
    for i in range(start_index, len(lines)):
        if lines[i].startswith('Addresses:'):
            address_part = lines[i].split('Addresses:')[1].strip()
            addresses.extend(addr.strip() for addr in address_part.split())
        elif lines[i].startswith('Address:'):
            address_part = lines[i].split('Address:')[1].strip()
            addresses.extend(addr.strip() for addr in address_part.split())
        elif lines[i].startswith((' ', '\t')):
            addresses.extend(addr.strip() for addr in lines[i].split())
        elif lines[i].startswith(('Name:', 'Aliases:')):
            break
    return addresses


def extract_aliases(lines, start_index):
    aliases = []
    for i in range(start_index, len(lines)):
        if lines[i].startswith('Aliases:'):
            aliases_part = lines[i].split('Aliases:')[1].strip()
            aliases.extend(addr.strip() for addr in aliases_part.split(','))
        elif lines[i].startswith((' ', '\t')):
            aliases.extend(addr.strip() for addr in lines[i].split(','))
        elif lines[i].startswith(('Name:', 'Addresses:', 'Address')) or lines[i].strip() == '':
            break
    return aliases


def nslookup_domain(domain):
    result = subprocess.run(['nslookup', domain], capture_output=True, text=True)
    if result.returncode != 0:
        return {'error': result.stderr}

    lines = result.stdout.splitlines()

    current_entry = {'Name': '', 'Addresses': [], 'Aliases': [], 'original_url': ''}

    for i in range(len(lines)):
        if lines[i].startswith('名称:'):
            current_entry = {'Name': lines[i].split(':')[1].strip(), 'Addresses': [], 'Aliases': []}
        elif lines[i].startswith('Addresses:') or lines[i].startswith('Address:'):
            addresses = extract_addresses(lines, i)
            if addresses == ['172.26.26.3']:
                continue
            current_entry['Addresses'].extend(addresses)
        elif lines[i].startswith('Aliases:'):
            aliases = extract_aliases(lines, i)
            current_entry['Aliases'].extend(aliases)

    if current_entry['Name']:
        return current_entry

    return current_entry


def process_url(url):
    try:
        domain = extract_domain(url)
        info = nslookup_domain(domain)
        info['original_url'] = url
        return info
    except Exception as e:
        return {}


def get_all_concurrent():
    total_url_file = 'total.txt'
    output_file = './nslookup_info.json'

    total_urls = []

    with open(total_url_file, 'r', encoding='utf-8') as total_file:
        total_urls = [url.strip() for url in total_file.readlines()]

    result_list = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_url, total_urls), desc="Processing URLs", unit="URL"))

    # Filter out empty results
    result_list = [result for result in results if result]

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(result_list, file, ensure_ascii=False, indent=2)


# get_all_concurrent()

# Example
# print(nslookup_domain("www.gxdzj.gov.cn"))

import json

with open('./nslookup_info.json', 'r', encoding='utf-8') as file:
    result_list = json.load(file)

# Dictionary to store counts of different lengths of 'Addresses' list
address_length_counts = {}
total_entries = 0
full_entries = 0
for info in result_list:
    full_entries += 1
    if info['Name'] != '':
        # Get the length of the 'Addresses' list
        addresses_length = len(info['Addresses'])

        # Update the count in the dictionary
        if addresses_length in address_length_counts:
            address_length_counts[addresses_length] += 1
        else:
            address_length_counts[addresses_length] = 1

        # Update overall total count
        total_entries += 1

# Print the total counts
for length in sorted(address_length_counts.keys()):
    total_count = address_length_counts[length]
    print(f"Total number of entries with {length} Addresses: {total_count}")

# Print overall total count
print(f"Overall total number of entries without null content: {total_entries}")
print(f"Overall total number of entries with null content: {full_entries}")
#
# Total number of entries with 1 Addresses: 607
# Total number of entries with 2 Addresses: 9433
# Total number of entries with 3 Addresses: 1509
# Total number of entries with 4 Addresses: 1691
# Total number of entries with 5 Addresses: 84
# Total number of entries with 6 Addresses: 102
# Total number of entries with 7 Addresses: 56
# Total number of entries with 8 Addresses: 184
# Total number of entries with 9 Addresses: 44
# Total number of entries with 10 Addresses: 11
# Total number of entries with 12 Addresses: 94
# Total number of entries with 15 Addresses: 1
# Total number of entries with 18 Addresses: 1
# Total number of entries with 19 Addresses: 2
# Total number of entries with 20 Addresses: 1
# Total number of entries with 22 Addresses: 1
# Overall total number of entries without null content: 13821
# Overall total number of entries with null content: 14000
