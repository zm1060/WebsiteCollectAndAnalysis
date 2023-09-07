# i have request a lot of website, and their response was stored in the '/response' directory, all files named with domain name end with .txt

# import os
# import requests
# from urllib.parse import urlparse
#
# response_directory = "./response"  # Path to the response directory
# results = {
#     "https_http_usage": {},  # For tracking HTTPS and HTTP usage
#     "subdomain_https_usage": {},  # For tracking subdomain HTTPS usage
#     "tls_versions": {},  # For tracking TLS versions
#     "certificate_data": {},  # For storing certificate data
#     "certificate_grades": {},  # For storing certificate grades
#     "department_https_usage": {},  # For tracking HTTPS usage by departments
#     "common_cas": {},  # For tracking commonly used CAs
#     "site_https_coverage": {},  # For tracking full-site or partial-site HTTPS usage
#     "mixed_content": {}  # For tracking mixed content
# }
#
# # Loop through the files in the response directory
# for filename in os.listdir(response_directory):
#     if filename.endswith(".txt"):
#         # Extract the domain name from the file name
#         domain_name = filename[:-4]
#
#         # Read the contents of the response file
#         file_path = os.path.join(response_directory, filename)
#         with open(file_path, "r") as file:
#             response = file.read()
#
#         # Analyze HTTPS and HTTP usage on the homepage
#         if response.startswith("https://"):
#             results["https_http_usage"].setdefault("HTTPS", []).append(domain_name)
#         elif response.startswith("http://"):
#             results["https_http_usage"].setdefault("HTTP", []).append(domain_name)
#
#         # Analyze subdomain HTTPS usage
#         parsed_url = urlparse(response)
#         subdomain = parsed_url.netloc.split(".", 1)[0]
#         if subdomain:
#             if response.startswith("https://"):
#                 results["subdomain_https_usage"].setdefault(subdomain, "Direct HTTPS")
#             else:
#                 results["subdomain_https_usage"].setdefault(subdomain, "Redirects to HTTPS")
#
#         # Test TLS version used
#         tls_version = parsed_url.scheme
#         results["tls_versions"].setdefault(tls_version, []).append(domain_name)
#
#         # Obtain certificate data
#         response_cert = requests.get(response, verify=False).certificate
#         if response_cert:
#             cert_data = {
#                 "issuer": response_cert.issuer,
#                 "valid_from": response_cert.valid_from,
#                 "valid_until": response_cert.valid_until,
#                 # Add more relevant certificate data as needed
#             }
#             results["certificate_data"][domain_name] = cert_data
#
#         # Evaluate certificate grades (using placeholder logic)
#         # Certificates can be evaluated based on the criteria mentioned in the referenced paper [1]
#         # Implement the evaluation logic based on the grading criteria mentioned in the paper
#         cert_grade = "A"  # Placeholder grade
#         results["certificate_grades"][domain_name] = cert_grade
#
#         # Analyze HTTPS usage by departments
#         # Extract department information from the domain name and categorize accordingly
#         department = domain_name.split(".")[0]
#         if department:
#             if response.startswith("https://"):
#                 results["department_https_usage"].setdefault(department, "HTTPS")
#             else:
#                 results["department_https_usage"].setdefault(department, "HTTP")
#
#         # Analyze most commonly used CAs
#         cert_issuer = response_cert.issuer
#         results["common_cas"].setdefault(cert_issuer, 0)
#         results["common_cas"][cert_issuer] += 1
#
#         # Analyze full-site or partial-site HTTPS usage
#         # Implement the logic based on whether the entire site or specific pages use HTTPS
#         if response.startswith("https://"):
#             results["site_https_coverage"].setdefault(domain_name, "Full-site HTTPS")
#         else:
#             results["site_https_coverage"].setdefault(domain_name, "Partial-site HTTPS")
#
#         # Analyze mixed content
#         # Implement the logic to check for external links in the response content that are not using HTTPS
#         mixed_content = []  # Placeholder for mixed content links
#         results["mixed_content"][domain_name] = mixed_content
#
# # Print the collected information
# print("HTTPS and HTTP Usage on the Homepage:")
# print(results["https_http_usage"])
# print("--------------------")
#
# print("Subdomain HTTPS Usage:")
# print(results["subdomain_https_usage"])
# print("--------------------")
#
# print("TLS Versions:")
# print(results["tls_versions"])
# print("--------------------")
#
# print("Certificate Data:")
# print(results["certificate_data"])
# print("--------------------")
#
# print("Certificate Grades:")
# print(results["certificate_grades"])
# print("--------------------")
#
# print("HTTPS Usage by Departments:")
# print(results["department_https_usage"])
# print("--------------------")
#
# print("Most Commonly Used CAs:")
# print(results["common_cas"])
# print("--------------------")
#
# print("Full-site or Partial-site HTTPS Usage:")
# print(results["site_https_coverage"])
# print("--------------------")
#
# print("Mixed Content:")
# print(results["mixed_content"])
# print("--------------------")



#222222222222222222222222222222222222

# import os
# from bs4 import BeautifulSoup
#
# response_directory = "./response"  # Path to the response directory
# results = []
#
# # Loop through the files in the response directory
# for filename in os.listdir(response_directory):
#     if filename.endswith(".txt"):
#         # Extract the domain name from the file name
#         domain_name = filename[:-4]
#
#         # Read the contents of the response file
#         file_path = os.path.join(response_directory, filename)
#         with open(file_path, "r") as file:
#             html_content = file.read()
#
#         # Process the HTML content using BeautifulSoup
#         soup = BeautifulSoup(html_content, "html.parser")
#
#         # Perform analysis on the HTML content as needed
#         # Example: Check if external links are not using HTTPS
#         mixed_content_links = []
#         for link in soup.find_all("a"):
#             href = link.get("href")
#             if href and not href.startswith("https://"):
#                 mixed_content_links.append(href)
#
#         # Store the collected information in the results list
#         result = {
#             "domain": domain_name,
#             "mixed_content_links": mixed_content_links
#         }
#         print(result)
#         results.append(result)
#
# # Print the collected information
# for result in results:
#     print("Domain:", result["domain"])
#     print("Mixed Content Links:", result["mixed_content_links"])
#     print("--------------------")


import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

response_directory = "./response"  # Path to the response directory

# Variables to track link statistics
total_links = 0
invalid_links = 0
external_links = []

# Loop through the files in the response directory
for filename in os.listdir(response_directory):
    if filename.endswith(".txt"):
        # Extract the domain name from the file name
        domain_name = filename[:-4]

        # Read the contents of the response file
        file_path = os.path.join(response_directory, filename)
        with open(file_path, "r") as file:
            html_content = file.read()

        # Process the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all <a> tags in the HTML content
        links = soup.find_all("a")
        for link in links:
            href = link.get("href")
            if href:
                total_links += 1

                # Check if the link is external
                parsed_link = urlparse(href)
                if parsed_link.netloc and parsed_link.netloc != domain_name:
                    external_url = href
                else:
                    absolute_url = urljoin(domain_name, href)
                    print(absolute_url)
                    external_url = absolute_url if not absolute_url.startswith(domain_name) else ""

                # Add the external link to the list
                if external_url:
                    external_links.append(external_url)
                    print(external_url)

                # Check if the link is valid
                try:
                    parsed_url = urlparse(external_url or absolute_url)
                    if not parsed_url.scheme:
                        parsed_url = parsed_url._replace(scheme="https")  # Add a default scheme if none is found

                    response = requests.head(parsed_url.geturl())
                    if response.status_code != 200:
                        invalid_links += 1
                except requests.exceptions.RequestException:
                    # Skip invalid URLs or network errors
                    pass

# Calculate invalid link ratio
invalid_link_ratio = invalid_links / total_links * 100 if total_links > 0 else 0

# Print the link statistics

print("Total Links:", total_links)
print("Invalid Links:", invalid_links)
print("Invalid Link Ratio: {:.2f}%".format(invalid_link_ratio))
print("--------------------")
# Print the external links and their distribution
print("External Links:")
for link in external_links:
    print(link)
print("--------------------")

