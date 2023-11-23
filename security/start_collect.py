from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from security.certificate_tool import fetch_certificates

directory = '../domain_txt'
failed_domains = []


def get_last_three_parts(domain):
    parts = domain.split('.')
    # 确保域名至少有三部分
    if len(parts) >= 3:
        return '.'.join(parts[-3:])
    else:
        # 如果域名没有三个部分，则返回整个域名
        return domain


def process_domain(domain):
    # Add "http://" to domain names that don't have it
    if not domain.startswith("http"):
        domain = "http://" + domain

    # Parse the URL and extract the base domain
    parsed_url = urlparse(domain)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    if not parsed_url.scheme or not parsed_url.netloc:
        return
    return base_url


# 设置最大并发线程数
MAX_THREADS = 10


def fetch_certificate_for_domain(domain, unit_name):
    fetch_certificates(get_last_three_parts(domain), unit_name)


def main():
    directory = '../domain_txt'
    failed_domains = []

    # 使用 ThreadPoolExecutor 实现并发处理
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_url = {}
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                unit_name = filename.split('.txt')[0]
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                    urls = [url.strip() for url in file.readlines() if url.strip()]
                    for url in urls:
                        sdomain = process_domain(url)
                        if sdomain:
                            parsed_sdomain = urlparse(sdomain)
                            domain = get_last_three_parts(parsed_sdomain.netloc)
                            if not os.path.exists(f'./ca/{unit_name}/{domain}.json'):
                                future = executor.submit(fetch_certificate_for_domain, domain, unit_name)
                                future_to_url[future] = url

        # 等待所有任务完成
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
                failed_domains.append(url)

    # 输出失败的域名
    if failed_domains:
        print("Failed domains:")
        for domain in failed_domains:
            print(domain)


if __name__ == '__main__':
    main()

# for filename in os.listdir(directory):
#     if filename.endswith('.txt'):
#         unit_name = filename.split('.txt')[0]
#         urls = []
#         with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
#             urls = file.readlines()
#         for url in urls:
#             url = url.strip()  # Remove leading/trailing whitespace and newlines
#             if url:
#                 sdomain = process_domain(url)
#                 if sdomain:
#                     parsed_sdomain = urlparse(sdomain)
#                     if os.path.exists(f'./ca/{unit_name}/{parsed_sdomain.netloc}.json'):
#                         continue
#                     fetch_certificates(get_last_three_parts(parsed_sdomain.netloc), unit_name)
# # 遍历每个单位目录
# for unit_dir in os.listdir(response_dir):
#     unit_path = os.path.join(response_dir, unit_dir)
#     unit_name = unit_dir
#     if os.path.isdir(unit_path):
#         # 遍历单位目录中的txt文件
#         for file_name in os.listdir(unit_path):
#             file_path = os.path.join(unit_path, file_name)
#             existing_node = file_name.split('.txt')[0]
#             print(existing_node)
#             fetch_certificates(existing_node, unit_name)

# certificate verify failed: unable to get local issuer certificate
# sslv3 alert handshake failure
# does not support HTTPS.
# certificate verify failed: Hostname mismatch, certificate is not valid for 'xxxx'
