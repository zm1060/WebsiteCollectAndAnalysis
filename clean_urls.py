import requests
from urllib.parse import urlparse, urlunparse

# Open the text file containing URLs
with open('total.txt', 'r', encoding='utf-8') as file:
    # Read the file line by line
    lines = file.readlines()

# Create two lists: one for valid URLs and another for URLs that need HTTP/HTTPS testing
valid_urls = []
test_urls = []

# Group the URLs
for line in lines:
    url = line.strip()  # Remove trailing newline characters and spaces
    parsed_url = urlparse(url)

    # Check if the URL contains an HTTP or HTTPS scheme
    if parsed_url.scheme in ('http', 'https'):
        valid_urls.append(url)
    else:
        # Add a default 'http://' scheme for URLs without a recognized scheme
        default_url = 'http://' + url
        test_urls.append(default_url)

# Create a new file to store the updated URLs
with open('updated_urls.txt', 'w') as updated_file:
    # Process URLs that are already valid
    for url in valid_urls:
        updated_file.write(url + '\n')

    # Process URLs that need HTTP/HTTPS testing
    for url in test_urls:
        parsed_url = urlparse(url)
        print(parsed_url)
        # Test the availability of the URL using requests
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                # If the response code is 200, add the HTTPS scheme
                updated_url = urlunparse(('https',) + parsed_url[1:])
                updated_file.write(updated_url + '\n')
            else:
                # If the response code is not 200, add the HTTP scheme
                updated_url = urlunparse(('http',) + parsed_url[1:])
                updated_file.write(updated_url + '\n')
        except requests.exceptions.RequestException:
            # If an exception occurs, or if the response code is not 200, use the default 'http://' scheme
            updated_url = urlunparse(('http',) + parsed_url[1:])
            updated_file.write(updated_url + '\n')
