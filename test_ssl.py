import os
from urllib.parse import urlparse

from ssllabs import ssllabsscanner

directory = './domain_txt'


def process_url(url):
    parsed_url = urlparse(url)
    domains = parsed_url.netloc
    return domains


for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        unit_name = filename.split('.txt')[0]
        urls = []
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            urls = file.readlines()
        for url in urls:
            url = url.strip()  # Remove leading/trailing whitespace and newlines
            if url:
                sdomain = process_url(url)
                print(sdomain)

# cached_data = ssllabsscanner.resultsFromCache("www.baidu.com")
#
# print(cached_data)
# print(cached_data['endpoints'][0]['grade'])

data = ssllabsscanner.newScan("www.baidu.com")

print(data)
