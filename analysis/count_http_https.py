
import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import json


def analyze_links(directory):
    total_links = 0
    invalid_links = 0
    internal_links = 0
    external_links = 0
    internal_invalid_links = 0
    external_invalid_links = 0
    http_links = 0
    https_links = 0

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    available_links = set()  # Set to store available links
    invalid_link_cache = {}  # Dictionary to cache invalid links

    # Traverse directories in the given directory
    for province_dir in os.listdir(directory):
        province_path = os.path.join(directory, province_dir)
        if not os.path.isdir(province_path):
            continue

        # Traverse files in the province directory
        for filename in os.listdir(province_path):
            if not filename.endswith('.txt'):
                continue

            file_path = os.path.join(province_path, filename)
            src_domain = filename.split('.txt')[0]

            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all <a> tags and extract the links
            links = [link.get('href') for link in soup.find_all('a') if link.get('href')]

            # Analyze the links and URLs
            for link in links:
                total_links += 1
                domain = urlparse(link).netloc

                # Handle relative paths as internal links
                if not domain and link.startswith('/'):
                    link = urljoin(f'http://{src_domain}', link)  # Construct the absolute URL with 'http://'
                    domain = src_domain

                if domain == src_domain or domain == '':
                    internal_links += 1
                elif domain != '':
                    external_links += 1

                # Check if the link has been cached as invalid
                if link in invalid_link_cache:
                    invalid_links += 1
                    if domain == src_domain:
                        internal_invalid_links += 1
                    elif domain != '':
                        external_invalid_links += 1
                # Check if the link is available in the cache
                elif link in available_links:
                    pass
                else:
                    # Check if the link uses HTTPS or HTTP
                    if link.startswith(('https://', 'http://')):
                        if link.startswith('https://'):
                            https_links += 1
                        elif link.startswith('http://'):
                            http_links += 1

                        try:
                            response = requests.get(link, headers=headers, verify=False, timeout=5,
                                                    allow_redirects=True)

                            # Handle redirections and normalize URLs
                            final_url = response.url
                            link = urljoin(link, final_url)

                            if response.status_code != 200:
                                print(f'{link} is invalid!')
                                invalid_links += 1
                                invalid_link_cache[link] = True  # Cache invalid link
                                if domain == src_domain:
                                    internal_invalid_links += 1
                                elif domain != '':
                                    external_invalid_links += 1
                            elif 'content-length' in response.headers:
                                print(f'{link} is available!')
                                available_links.add(link)
                                content_length = int(response.headers['content-length'])
                                if content_length > 10 * 1024 * 1024:
                                    continue

                        except requests.exceptions.RequestException:
                            print(f'{link} is invalid!')
                            invalid_links += 1
                            invalid_link_cache[link] = True  # Cache invalid link
                            if domain == src_domain:
                                internal_invalid_links += 1
                            elif domain != '':
                                external_invalid_links += 1

        # Calculate link ratios for each province
        if total_links > 0:
            invalid_link_ratio = (invalid_links / total_links) * 100
        else:
            invalid_link_ratio = 0

        if internal_links > 0:
            internal_link_ratio = (internal_invalid_links / internal_links) * 100
        else:
            internal_link_ratio = 0

        if external_links > 0:
            external_link_ratio = (external_invalid_links / external_links) * 100
        else:
            external_link_ratio = 0

        http_https_info = {
            'province': province_dir,
            'total_links': total_links,
            'invalid_links': invalid_links,
            'invalid_link_ratio': f'{invalid_link_ratio:.2f}%',
            'internal_links': internal_links,
            'invalid_internal_links': internal_invalid_links,
            'invalid_internal_link_ratio': f'{internal_link_ratio:.2f}%',
            'external_links': external_links,
            'invalid_external_links': external_invalid_links,
            'invalid_external_link_ratio': f'{external_link_ratio:.2f}%',
            'http_links': http_links,
            'https_links': https_links,
        }

        output_directory = f"./http_https"
        os.makedirs(output_directory, exist_ok=True)
        output_filename = os.path.join(output_directory, f"{province_dir}.json")

        with open(output_filename, 'w', encoding='utf-8') as json_file:
            json.dump(http_https_info, json_file, ensure_ascii=False, indent=4)

        print(f"http and https information for {province_dir} has been saved to {output_filename}")

        # Reset counters
        total_links = 0
        invalid_links = 0
        internal_links = 0
        external_links = 0
        internal_invalid_links = 0
        external_invalid_links = 0
        http_links = 0
        https_links = 0


# Example usage
directory = '../xdns/class'
analyze_links(directory)
