import json
import os
from urllib.parse import urlparse

import requests


def process_url(url):
    parsed_url = urlparse(url)
    domains = parsed_url.netloc
    return domains


def process_domain(domain):
    # Add "http://" to domain names that don't have it
    if not domain.startswith("http"):
        domain = "http://" + domain

    # Parse the URL and extract the base domain
    parsed_url = urlparse(domain)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc
    if not parsed_url.scheme or not parsed_url.netloc:
        return
    return base_url


def get_domain():
    directory = '../domain_txt'
    all_domain = []
    failed_domains = []
    total_direct_https = 0
    total_indirect_https = 0
    total_unused_https = 0
    total_failed_request = 0

    for filename in os.listdir(directory):

        if filename.endswith('.txt'):
            unit_name = filename.split('.txt')[0]
            if os.path.exists(f"./direct_or_indirect/{unit_name}/results.json"):
                continue
            urls = []
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                urls = file.readlines()
            direct_https = 0
            indirect_https = 0
            unused_https = 0
            failed_request = 0
            for url in urls:
                url = url.strip()  # Remove leading/trailing whitespace and newlines
                if url:
                    sdomain = process_domain(url)
                    if sdomain:
                        all_domain.append(sdomain)
                        print(sdomain)
                        try:
                            response = requests.get(sdomain, allow_redirects=False, timeout=10)
                            if response.status_code == 200:
                                if response.url.strip("https://"):
                                    direct_https += 1
                                else:
                                    unused_https += 1
                            elif response.status_code == 301 or response.status_code == 302:
                                redirect_location = response.headers.get("Location")
                                if redirect_location and redirect_location.startswith("https://"):
                                    indirect_https += 1
                                else:
                                    unused_https += 1
                            else:
                                failed_domains.append(sdomain)

                        except Exception as e:
                            print('Error' + str(e))
                            failed_request += 1
            unit_result = {
                "province": unit_name,
                "direct_https": direct_https,
                "indirect_https": indirect_https,
                "unused_https": unused_https,
                "failed_domains": failed_request
            }
            os.makedirs(f"./direct_or_indirect/{unit_name}", exist_ok=True)

            with open(f"./direct_or_indirect/{unit_name}/results.json", 'w', encoding='utf-8') as json_file:
                json.dump(unit_result, json_file, ensure_ascii=False, indent=2)

            total_direct_https += direct_https
            total_indirect_https += indirect_https
            total_unused_https += unused_https
            total_failed_request += failed_request
    total_result = {
        "direct_https": total_direct_https,
        "indirect_https": total_indirect_https,
        "unused_https": total_unused_https,
        "failed_request": total_failed_request
    }
    with open(f"./direct_or_indirect/total.json", 'w', encoding='utf-8') as json_file:
        json.dump(total_result, json_file, ensure_ascii=False, indent=4)


get_domain()
