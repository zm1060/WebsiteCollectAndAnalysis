import os
from urllib.parse import urlparse
import requests
import concurrent.futures
import urllib3
import chardet

def process_url(url):
    parsed_url = urlparse(url)
    domains = parsed_url.netloc
    return domains


def get_domain():
    directory = '../domain_txt'
    all_domain = []
    failed_domains = []

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
                        all_domain.append(sdomain)
                        print(sdomain)

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
    if  not parsed_url.scheme or not parsed_url.netloc:
        return
    return base_url



def store_response(domain):
    try:
        headers = {
            'contentType' 'text/html;charset=utf-8'
            'Connection': 'close',
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
        }
        filename = f"./response/{process_url(domain)}.txt"
        if os.path.isfile(filename):
            print(f"File already exists: {filename}")
            return True

        # response = requests.get(domain, stream=True, headers=headers, verify='../venv/lib/python3.10/site-packages/certifi/cacert.pem', timeout=5, allow_redirects=True)
        response = requests.get(domain, stream=True, headers=headers, verify=False, timeout=5, allow_redirects=True)
        # Determine the encoding
        encoding = response.encoding
        if not encoding:
            # If encoding is not specified, use chardet to detect it
            encoding = chardet.detect(response.content)['encoding']

        # Set the correct encoding
        response.encoding = encoding

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


def save_failed_domains(failed_domains):
    with open("failed_domains.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(failed_domains))


urllib3.disable_warnings()
# Call get_domain() to start the process
get_domain()
