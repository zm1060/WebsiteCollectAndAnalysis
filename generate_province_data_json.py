import json
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse


def extract_links_from_html(html_path, base_url):
    with open(html_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    links = []

    for a in soup.find_all('a', href=True):
        link = urljoin(base_url, a['href'])
        # 过滤掉JavaScript和特殊链接
        if not link.startswith(('javascript:', 'file:')):
            links.append(link)

    return links


def classify_links(links, base_url):
    internal_links = []
    external_links = []
    potential_threat_links = []

    for link in links:
        parsed_link = urlparse(link)
        parsed_base_url = urlparse(base_url)

        if parsed_link.netloc == parsed_base_url.netloc:
            internal_links.append(link)
        else:
            external_links.append(link)

            # 判断是否为潜在威胁的外链
            if not parsed_link.netloc.endswith('gov.cn'):
                potential_threat_links.append(link)

    return internal_links, external_links, potential_threat_links


def analyze_directory(directory_path):
    province_data = []

    for province_folder in os.listdir(directory_path):
        province_path = os.path.join(directory_path, province_folder)
        print(f"Analyzing province: {province_folder}")

        if os.path.isdir(province_path):
            province_info = {'province': province_folder, 'sites': []}

            for html_file in os.listdir(province_path):
                if html_file.endswith('.html'):
                    # 使用下划线分隔文件名，然后替换下划线为斜杠
                    url_part = html_file.split('.html')[0].replace('_', '/')
                    parts = url_part.split('/')

                    # 假设文件名中的第一个部分是协议（http或https），第二个部分是域名
                    if len(parts) >= 2:
                        protocol = parts[0]
                        domain = parts[1]

                        # 构建原始URL
                        original_url = f"{protocol}://{domain}"

                        print(f"Original URL for {html_file}: {original_url}")

                        html_path = os.path.join(province_path, html_file)
                        base_url = original_url  # 使用原始URL作为base_url
                        links = extract_links_from_html(html_path, base_url)
                        internal_links, external_links, potential_threat_links = classify_links(links, base_url)

                        site_info = {
                            'url': original_url,
                            'internal_links': internal_links,
                            'external_links': external_links,
                            'potential_threat_links': potential_threat_links,
                            'internal_links_count': len(internal_links),
                            'external_links_count': len(external_links),
                            'potential_threat_links_count': len(potential_threat_links),
                            'total_links_count': len(links)
                        }

                        province_info['sites'].append(site_info)

            province_data.append(province_info)

    return province_data


def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    directory_path = "./new_response/"
    province_data = analyze_directory(directory_path)

    output_json_file = 'province_data.json'
    save_to_json(province_data, output_json_file)
    print(f"\nResults saved to {output_json_file}")
