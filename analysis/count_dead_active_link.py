# in '../xdns/class' directory, has a lot of directories named with provience name, under the directory of it, has a lot of reponse file of request domain, which is .txt file,
# 分析首页中网站的链接（内链和外链）无效情况，包括域名解析和网页内容等等。
# 以数量+比例进行对比。
# 外链的数量和分布情况。

import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def analyze_links(directory):
    total_links = 0
    invalid_links = 0
    external_links = 0
    external_invalid_links = 0
    link_ratios = {}
    headers = {
        'Connent-Type': 'text/html',
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    # Traverse directories in the given directory
    for province_dir in os.listdir(directory):
        province_path = os.path.join(directory, province_dir)

        # Traverse files in the province directory
        for filename in os.listdir(province_path):
            if filename == 'ip_address_info.txt' or filename == 'ip_cdn_info.txt':
                continue
            if filename.endswith('.txt'):
                file_path = os.path.join(province_path, filename)

                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()

                # Parse the HTML content
                soup = BeautifulSoup(html_content, 'html.parser')

                # Find all <a> tags and extract the links
                links = []
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:
                        links.append(href)

                # Analyze the links and URLs
                for link in links:
                    total_links += 1
                    domain = urlparse(link).netloc
                    if domain != '':
                        external_links += 1
                        print(link, 'is a external link!')
                    try:
                        response = requests.get(link, stream=True, headers=headers, verify=False, timeout=5,
                                                allow_redirects=True)
                        print('requests to: ', link)
                        if response.status_code != 200 or len(response.text) == 0:
                            invalid_links += 1
                            print('invalid_links +1')
                            if domain != '':
                                external_invalid_links += 1
                                print(link, 'is a external invalid link!')
                        else:
                            print(link, 'is active!')
                    except requests.exceptions.RequestException:
                        invalid_links += 1
                        if domain != '':
                            external_invalid_links += 1
                            print(link, 'is a external invalid link!')

        # Calculate link ratios for each province
        # link_ratios[province_dir] = (invalid_links / total_links) * 100
        # Print the results
        print("Total links:", total_links)
        print("Invalid links:", invalid_links)
        print("Invalid link ratio:", (invalid_links / total_links) * 100, "%")
        print("External links:", external_links)
        print("Invalid external links:", external_invalid_links)
        print("Invalid external link ratio:", (external_invalid_links / external_links) * 100, "%")

        with open(f"./links/{province_dir}_links.txt", 'w', encoding='utf-8') as file:
            file.write(f"total links:{total_links}\n")
            file.write(f"invalid links:{invalid_links}\n")
            file.write(f"invalid links ratio:{(invalid_links / total_links) * 100}%\n")
            file.write(f"external links:{external_links}\n")
            file.write(f"invalid external links:{external_invalid_links}\n")
            file.write(f"invalud external links ratio:{(external_invalid_links / external_links) * 100}%\n")

        total_links = 0
        invalid_links = 0
        external_links = 0
        external_invalid_links = 0

    # print("Link ratios by province:")
    # for province, ratio in link_ratios.items():
    #     print(province, ":", ratio, "%")
    #


# Example usage
directory = '../xdns/class'
analyze_links(directory)
