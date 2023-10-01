import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests

# def store_response(domain):
#     try:
#         headers = {'Connection': 'close',
#                    'User-Agent': "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"}
#
#         filename = f"./response/{domain.split('//')[1]}.txt"
#         if os.path.isfile(filename):
#             print(f"File already exists: {filename}")
#             return True
#
#         # Check the URL scheme
#         if domain.startswith("http://"):
#             # HTTP request
#             response = requests.get(domain, stream=True, headers=headers, verify=False, timeout=10,
#                                     allow_redirects=False)
#         elif domain.startswith("https://"):
#             # HTTPS request
#             response = requests.get(domain, stream=True, headers=headers, verify=False, timeout=10,
#                                     allow_redirects=False)
#         else:
#             # Invalid URL scheme
#             print(f"Invalid URL scheme for domain: {domain}")
#             return False
#
#         if response.status_code == 200:
#             with open(filename, "w", encoding="utf-8") as file:
#                 file.write(response.text)
#             print(f"Response stored: {filename}")
#             response.close()
#             return True
#         elif response.status_code == 403:
#             print(f"Failed to request website: {domain} (Status code: {response.status_code})")
#             response.close()
#             # Retry with an HTTPS request if it's an HTTP URL
#             if domain.startswith("http://"):
#                 return store_response(domain.replace("http://", "https://"))
#             else:
#                 with open(f"{str(response.status_code)}.txt", "a") as file:
#                     file.write(domain + "\n")
#                 response.close()
#                 return False
#         else:
#             print(f"Failed to request website: {domain} (Status code: {response.status_code})")
#             with open(f"{str(response.status_code)}.txt", "a") as file:
#                 file.write(domain + "\n")
#             response.close()
#             return False
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to request website: {domain} ({str(e)})")
#         with open(f"{str(type(e).__name__)}.txt", "a") as file:
#             file.write(domain + "\n")
#         return False
#





def store_response(domain):
    try:
        driver = webdriver.Chrome()  # Provide the path to your Chrome driver executable

        filename = f"./response/{domain.split('//')[1]}.txt"
        if os.path.isfile(filename):
            print(f"File already exists: {filename}")
            return True

        # Check the URL scheme
        if domain.startswith("http://") or domain.startswith("https://"):
            driver.get(domain)
            sleep(5)
            response_text = driver.page_source
        else:
            # Invalid URL scheme
            print(f"Invalid URL scheme for domain: {domain}")
            return False

        with open(filename, "w", encoding="utf-8") as file:
            file.write(response_text)

        print(f"Response stored: {filename}")
        driver.quit()
        return True
    except Exception as e:
        print(f"Failed to request website: {domain} ({str(e)})")
        with open(f"{str(type(e).__name__)}.txt", "a") as file:
            file.write(domain + "\n")
        return False







#
# requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
#

# # Read the failed domains from the file
failed_domains = []
with open("failed_domains.txt", "r") as file:
    failed_domains = [line.strip() for line in file]

# Re-request and store responses for the failed domains
for domain in failed_domains:
    store_response(domain)



