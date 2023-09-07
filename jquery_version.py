import os
import re
import requests
from bs4 import BeautifulSoup
import json


def check_jquery_vulnerabilities(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    jquery_script = soup.select_one('script[src*="jquery"]')
    print(html_content)
    if jquery_script:
        jquery_version = jquery_script.get('src').split('/')[-1].split('-')[1].split('.')[0]
        print(jquery_version)

        headers = {'Connection': 'close',
                   'User-Agent': "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"}
        # Query the NVD API to check for vulnerabilities
        nvd_api_url = f"https://services.nvd.nist.gov/rest/json/cves/1.0?cpeMatchString=cpe:/a:jquery:jquery:{jquery_version}"
        response = requests.get(nvd_api_url, stream=True, headers=headers, verify=False, timeout=10, allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            if data is not None and data.get('result', {}).get('totalResults') > 0:
                print(f"Potential vulnerabilities found for jQuery version {jquery_version}")
                # Process the vulnerability information as needed
                vulnerabilities = True
            else:
                print(f"No known vulnerabilities found for jQuery version {jquery_version}")
                vulnerabilities = False
        else:
            print("Failed to query the NVD API")
            vulnerabilities = None
    else:
        print("jQuery script tag not found in the HTML")
        vulnerabilities = None

    return {
        'version': jquery_version,
        'vulnerabilities': vulnerabilities
    }


response_directory = "./dns/response"  # Directory name where the response files are stored
file_extension = ".txt"  # File extension to filter

# Iterate over the files in the directory
for filename in os.listdir(response_directory):
    if filename.endswith(file_extension):
        file_path = os.path.join(response_directory, filename)
        with open(file_path, "r") as file:
            html_content = file.read()
            result = check_jquery_vulnerabilities(html_content)

            # Create the output JSON file path
            json_file_path = os.path.splitext(file_path)[0] + ".json"

            # Write the result to the JSON file
            with open(json_file_path, "w") as json_file:
                json.dump(result, json_file)
                print(f"Result saved to {json_file_path}")


# import requests
# from bs4 import BeautifulSoup
#
# def check_jquery_vulnerabilities(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     jquery_script = soup.select_one('script[src*="jquery"]')
#
#     if jquery_script:
#         jquery_version = jquery_script.get('src').split('/')[-1].split('.')[0]
#
#         # Query the NVD API to check for vulnerabilities
#         nvd_api_url = f"https://services.nvd.nist.gov/rest/json/cves/1.0?cpeMatchString=cpe:/a:jquery:jquery:{jquery_version}"
#         response = requests.get(nvd_api_url)
#         if response.status_code == 200:
#             data = response.json()
#             if data.get('result', {}).get('totalResults') > 0:
#                 print(f"Potential vulnerabilities found for jQuery version {jquery_version}")
#                 # Process the vulnerability information as needed
#             else:
#                 print(f"No known vulnerabilities found for jQuery version {jquery_version}")
#         else:
#             print("Failed to query the NVD API")
#     else:
#         print("jQuery script tag not found in the HTML")
#
#
# headers = {'Connection': 'close',
#            'User-Agent': "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"}
#
# # Example usage
# url = 'https://agri.jian.gov.cn/'  # Replace with your HTML source URL
# response = requests.get(url, stream=True, headers=headers, verify=False, timeout=10,
#                         allow_redirects=False)
# html_content = response.text
# print(html_content)
# check_jquery_vulnerabilities(html_content)


