import json
import os
from urllib.parse import urlparse
import subprocess
import json

from tqdm import tqdm


def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


def extract_addresses(lines, start_index):
    addresses = []
    for i in range(start_index, len(lines)):
        if lines[i].startswith('Addresses:'):
            address_part = lines[i].split('Addresses:')[1].strip()
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
        elif lines[i].startswith(('Name:', 'Addresses:')) or lines[i].strip() == '':
            break
    return aliases


def nslookup_domain(domain):
    result = subprocess.run(['nslookup', domain], capture_output=True, text=True)

    if result.returncode != 0:
        return {'error': result.stderr}

    lines = result.stdout.splitlines()

    current_entry = {'Name': '', 'Addresses': [], 'Aliases': [], 'original_url': ''}

    for i in range(len(lines)):
        # print(lines[i])
        if lines[i].startswith('名称:'):
            current_entry = {'Name': lines[i].split(':')[1].strip(), 'Addresses': [], 'Aliases': []}
        elif lines[i].startswith('Addresses:'):
            addresses = extract_addresses(lines, i)
            current_entry['Addresses'].extend(addresses)
        elif lines[i].startswith('Aliases:'):
            aliases = extract_aliases(lines, i)
            current_entry['Aliases'].extend(aliases)

    # Adding the last entry after the loop
    if current_entry['Name']:
        return current_entry

    return {'Name': '', 'Addresses': [], 'Aliases': [], 'original_url': ''}

def get_all():
    total_url_file = 'total.txt'
    output_file = './nslookup_info.json'

    total_urls = []

    with open(total_url_file, 'r', encoding='utf-8') as total_file:
        total_urls = [url.strip() for url in total_file.readlines()]

    result_list = []

    for url in tqdm(total_urls, desc="Processing URLs", unit="URL"):
        # Check if 'original_url' key is present in each existing_info
        try:
            domain = extract_domain(url)
            info = nslookup_domain(domain)
            info['original_url'] = url
            result_list.append(info)

        except Exception as e:
            pass

    # Write all results to the file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(result_list, file, ensure_ascii=False, indent=2)

# get_all()

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




# Total number of entries with 0 Addresses: 606
# Total number of entries with 2 Addresses: 9062
# Total number of entries with 3 Addresses: 1264
# Total number of entries with 4 Addresses: 1563
# Total number of entries with 5 Addresses: 171
# Total number of entries with 6 Addresses: 99
# Total number of entries with 7 Addresses: 9
# Total number of entries with 8 Addresses: 229
# Total number of entries with 9 Addresses: 37
# Total number of entries with 10 Addresses: 9
# Total number of entries with 12 Addresses: 91
# Total number of entries with 13 Addresses: 1
# Total number of entries with 14 Addresses: 1
# Total number of entries with 19 Addresses: 2
# Total number of entries with 20 Addresses: 1
# Total number of entries with 22 Addresses: 1
# Overall total number of entries: 13146
# Overall total number of entries with full info: 13998