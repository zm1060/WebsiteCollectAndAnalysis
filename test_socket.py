from urllib.parse import urlparse

def extract_domain(url):
    if not url.startswith("http"):
        url = "http://" + url
    parsed_url = urlparse(url)
    return parsed_url.netloc

def count_unique_domains(file_path):
    unique_domains = set()

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            if url:
                domain = extract_domain(url)
                unique_domains.add(domain)

    return len(unique_domains)

# 替换 'your_file.txt' 为实际的文件路径
file_path = 'total.txt'
unique_domains_count = count_unique_domains(file_path)

print(f"不重复的域名数量为: {unique_domains_count}")
