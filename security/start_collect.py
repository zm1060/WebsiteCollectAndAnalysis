from urllib.parse import urlparse

from ca_chain import fetch_certificates
import os

response_dir = '../xdns/class'  # response目录路径

directory = '../domain_txt'
failed_domains = []


def process_domain(domain):
    # Add "http://" to domain names that don't have it
    if not domain.startswith("http"):
        domain = "http://" + domain

    # Parse the URL and extract the base domain
    parsed_url = urlparse(domain)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    if not parsed_url.scheme or not parsed_url.netloc:
        return
    return base_url


for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        unit_name = filename.split('.txt')[0]
        urls = []
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            urls = file.readlines()
        for url in urls:
            url = url.strip()  # Remove leading/trailing whitespace and newlines
            if url:
                sdomain = process_domain(url)
                if sdomain:
                    parsed_sdomain = urlparse(sdomain)
                    if os.path.exists(f'./ca/{unit_name}/{parsed_sdomain.netloc}.json'):
                        print(f'{unit_name}/{parsed_sdomain.netloc}')
                        continue
                    fetch_certificates(parsed_sdomain.netloc, unit_name)

# # 遍历每个单位目录
# for unit_dir in os.listdir(response_dir):
#     unit_path = os.path.join(response_dir, unit_dir)
#     unit_name = unit_dir
#     if os.path.isdir(unit_path):
#         # 遍历单位目录中的txt文件
#         for file_name in os.listdir(unit_path):
#             file_path = os.path.join(unit_path, file_name)
#             existing_node = file_name.split('.txt')[0]
#             print(existing_node)
#             fetch_certificates(existing_node, unit_name)

# certificate verify failed: unable to get local issuer certificate
# sslv3 alert handshake failure
# does not support HTTPS.
# certificate verify failed: Hostname mismatch, certificate is not valid for 'xxxx'

