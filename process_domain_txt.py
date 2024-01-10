# import os
# from urllib.parse import urlparse
# import requests

# def fix_url(url):
#     # Try adding 'https://'
#     https_url = 'https://' + url
#     try:
#         response = requests.get(https_url, timeout=5)
#         response.raise_for_status()
#         return https_url
#     except requests.exceptions.RequestException:
#         pass
#
#     # If 'https://' fails, try adding 'http://'
#     http_url = 'http://' + url
#     try:
#         response = requests.get(http_url, timeout=5)
#         response.raise_for_status()
#         return http_url
#     except requests.exceptions.RequestException:
#         pass
#
#     # If both fail, return the original URL
#     return url
#
# def process_file(file_path):
#     with open(file_path, 'r', encoding='utf-8') as txt_file:
#         urls = txt_file.readlines()
#         urls = [url.strip() for url in urls]  # Remove newline characters
#         fixed_urls = []
#         for url in urls:
#             parsed_url = urlparse(url)
#             if not (parsed_url.scheme and parsed_url.netloc):
#                 fixed_url = fix_url(url)
#                 fixed_urls.append(fixed_url)
#             else:
#                 fixed_urls.append(url)
#
#     # Write back the fixed URLs to the same file
#     with open(file_path, 'w', encoding='utf-8') as txt_file:
#         txt_file.write('\n'.join(fixed_urls))
#
# # Process all files in the './domain_txt' directory
# for filename in os.listdir('./domain_txt'):
#     if filename.endswith('.bak'):
#         continue
#     file_path = f'./domain_txt/{filename}'
#     process_file(file_path)
#     print(f'Processed {file_path}')


import os
from urllib.parse import urlparse

import requests


def count_urls(file_path):
    total_urls = 0
    invalid_urls = 0
    with open(file_path, 'r', encoding='utf-8') as txt_file:
        urls = txt_file.readlines()
        urls = [url.strip() for url in urls]  # Remove newline characters
        for url in urls:
            total_urls += 1
            parsed_url = urlparse(url)
            if not (parsed_url.scheme and parsed_url.netloc):
                invalid_urls += 1
                print(url)

    return total_urls, invalid_urls


total_urls_count = 0
invalid_urls_count = 0

# Process all files in the './domain_txt' directory
for filename in os.listdir('./domain_txt'):
    if filename.endswith('.bak'):
        continue
    file_path = f'./domain_txt/{filename}'
    total, invalid = count_urls(file_path)
    total_urls_count += total
    invalid_urls_count += invalid

print(f'Total URLs: {total_urls_count}')
print(f'Invalid URLs: {invalid_urls_count}')



