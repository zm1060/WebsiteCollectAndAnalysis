import os
import shutil
from urllib.parse import urlparse


def process_url(url):
    if not url.startswith("http"):
        url = "http://" + url
    parsed_url = urlparse(url)
    domains = parsed_url.netloc
    return domains

def save_failed_domains(failed_domains):
    for domain in failed_domains:
        with open("./class/failed_domains.txt", "a", encoding="utf-8") as file:
            file.write(f"{domain}\n")


directory = '../domain_txt/'

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
                sdomain = process_url(url)
                print(sdomain)
                sfilename = f'./response/{sdomain}.txt'
                if os.path.isfile(sfilename):
                    print(f"File exists: {sfilename}")

                    destination_dir = os.path.join('./class', unit_name)
                    os.makedirs(destination_dir, exist_ok=True)

                    destination_path = os.path.join(destination_dir, f"{sdomain}.txt")
                    shutil.copy(sfilename, destination_path)
                else:
                    print(f"File not exists: {sfilename}")
                    if sdomain:
                        failed_domains.append(url)
save_failed_domains(failed_domains)