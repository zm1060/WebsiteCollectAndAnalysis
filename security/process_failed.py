from urllib.parse import urlparse

from certificate_tool import fetch_certificates
import os


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


directory = './ca'

for unit_name in os.listdir(directory):
    # print(unit_name)
    filename = 'error.txt'
    urls = []
    if os.path.exists(f'./ca/{unit_name}/error.txt'):
        with open(f'./ca/{unit_name}/error.txt', 'r', encoding='utf-8') as file:
            urls = file.readlines()
        for url in urls:
            url = url.strip()  # Remove leading/trailing whitespace and newlines
            if url:
                fetch_certificates(url, unit_name)
