import os
from time import sleep
from urllib.parse import urlparse
import requests
import concurrent.futures
import urllib3
import chardet
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
    base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
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
            # print(f"File already exists: {filename}")
            return True

        # response = requests.get(domain, stream=True, headers=headers, verify='../venv/lib/python3.10/site-packages/certifi/cacert.pem', timeout=5, allow_redirects=True)
        print(f"request: {domain}")
        response = requests.get(domain, stream=True, headers=headers, verify=False, timeout=10, allow_redirects=True)
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
            # Retry with an HTTPS request if it's an HTTP URL
            if domain.startswith("http://"):
                return store_response(domain.replace("http://", "https://"))
            else:
                with open(f"{str(response.status_code)}.txt", "a") as file:
                    file.write(domain + "\n")
                response.close()
                return False
            response.close()
            return False
    except requests.exceptions.RequestException as e:
        print(f"Failed to request website: {domain} ({str(e)})")
        with open(f"{str(type(e).__name__)}.txt", "a") as file:
            file.write(domain + "\n")
        return False



# def store_response(domain):
#     filename = f"./response/{domain.split('//')[1]}.txt"
#     if os.path.isfile(filename):
#         print(f"File already exists: {filename}")
#         return True
#
#     try:
#         driver = webdriver.Chrome()  # Provide the path to your Chrome driver executable
#         options = Options()
#         options.add_argument("--headless")  # Run Chrome in headless mode
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#
#         driver = webdriver.Chrome(options=options)  # Provide the path to your Chrome driver executable
#         # Check the URL scheme
#         if domain.startswith("http://") or domain.startswith("https://"):
#             driver.get(domain)
#             sleep(2)
#             response_text = driver.page_source
#         else:
#             # Invalid URL scheme
#             print(f"Invalid URL scheme for domain: {domain}")
#             return False
#
#         with open(filename, "w", encoding="utf-8") as file:
#             file.write(response_text)
#
#         print(f"Response stored: {filename}")
#         driver.quit()
#         return True
#     except Exception as e:
#         print(f"Failed to request website: {domain} ({str(e)})")
#         with open(f"{str(type(e).__name__)}.txt", "a") as file:
#             file.write(domain + "\n")
#         return False
#




def save_failed_domains(failed_domains):
    with open("./failed_domains.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(failed_domains))


urllib3.disable_warnings()
# Call get_domain() to start the process
get_domain()
