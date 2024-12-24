# import os
# from urllib.parse import urlparse
# from tqdm import tqdm
# import whois
# import json
# import threading
#
# # 创建一个字典用于存储各省份的 WHOIS 信息
# province_data = {}
#
# # 统计未查询到 WHOIS 信息的域名
# unresolved_domains = []
#
# # 创建一个字典用于缓存已查询过的域名的 WHOIS 信息
# domain_cache = {}
#
#
# # 定义一个函数，用于处理每个省份的域名查询
# def process_domain(province, urls):
#     province_data[province] = []
#     for url in tqdm(urls, desc=f"Processing {province}"):
#         if not url.startswith("http"):
#             url = "http://" + url
#         domain = urlparse(url).netloc
#         # 提取域名的顶级域、二级域和子域
#         domain_parts = domain.split('.')
#         domain_parts = domain_parts[-3:] if len(domain_parts) >= 3 else domain_parts
#         domain_info = {}
#         domain_info['FQDN'] = domain
#         domain_info['query_domain'] = domain_parts
#
#         # 查询 WHOIS 信息
#         if domain in domain_cache:
#             # 如果缓存中已有该域名的信息，则直接使用缓存
#             domain_info['whois'] = domain_cache[domain]
#         else:
#             try:
#                 w = whois.whois(domain)
#                 # 格式化 WHOIS 信息
#                 formatted_whois = {
#                     'domain': w.domain_name,
#                     'name': w.name,
#                     'registrar': w.registrar,
#                     'emails': w.emails,
#                     'status': w.status,
#                     'nameservers': w.name_servers,
#                     'dnssec': w.dnssec,
#                     'creation_date': str(w.creation_date),
#                     'expiration_date': str(w.expiration_date),
#                     'last_updated': str(w.last_updated),
#                     'registrant': w.registrant,  # 添加注册人信息字段
#                     # 添加 nameservers、dnssec 和 registrant 字段
#                 }
#                 domain_info['whois'] = formatted_whois
#                 # 将查询结果存入缓存
#                 domain_cache[domain] = formatted_whois
#             except whois.parser.PywhoisError:
#                 unresolved_domains.append(domain)
#                 domain_info['whois'] = "Not found"
#         # print(domain_info)  # 这行注释掉，因为 tqdm 会显示进度
#         province_data[province].append(domain_info)
#
#
# # 遍历目录下的每个 txt 文件并启动线程处理
# threads = []
# for filename in os.listdir('../domain_txt'):
#     province = filename.split('.txt')[0]
#
#     with open(os.path.join('../domain_txt', filename), 'r', encoding='utf-8') as file:
#         urls = file.readlines()
#         urls = [url.strip() for url in urls]
#
#     # 创建线程并启动
#     thread = threading.Thread(target=process_domain, args=(province, urls))
#     thread.start()
#     threads.append(thread)
#
# # 等待所有线程完成
# for thread in threads:
#     thread.join()
#
# # 存储 WHOIS 信息到 JSON 文件
# for province, data in province_data.items():
#     with open(f'{province}_whois.json', 'w', encoding='utf-8') as json_file:
#         json.dump(data, json_file, ensure_ascii=False, indent=4)
#
# # 统计未查询到 WHOIS 信息的域名
# unresolved_domains_count = len(unresolved_domains)
# with open('unresolved_domains.txt', 'w', encoding='utf-8') as unresolved_file:
#     unresolved_file.write('\n'.join(unresolved_domains))
#
# print(f"总共有{unresolved_domains_count}个域名没有找到 WHOIS 信息。")


import os
from urllib.parse import urlparse
from tqdm import tqdm
import whois
import json

# 创建一个字典用于存储各省份的 WHOIS 信息
province_data = {}

# 统计未查询到 WHOIS 信息的域名
unresolved_domains = []

# 创建一个字典用于缓存已查询过的域名的 WHOIS 信息
domain_cache = {}


# 定义一个函数，用于处理每个省份的域名查询
def process_domain(province, urls):
    province_data[province] = []
    for url in tqdm(urls, desc=f"Processing {province}"):
        if not url.startswith("http"):
            url = "http://" + url
        domain = urlparse(url).netloc
        # 提取域名的顶级域、二级域和子域
        domain_parts = domain.split('.')
        domain_parts = domain_parts[-3:] if len(domain_parts) >= 3 else domain_parts
        domain_info = {}
        domain_info['FQDN'] = domain
        domain_info['query_domain'] = domain_parts

        # 查询 WHOIS 信息
        if domain in domain_cache:
            # 如果缓存中已有该域名的信息，则直接使用缓存
            domain_info['whois'] = domain_cache[domain]
        else:
            try:
                w = whois.whois(domain)
                # 格式化 WHOIS 信息
                formatted_whois = {
                    'domain': w.domain_name,
                    'name': w.name,
                    'registrar': w.registrar,
                    'emails': w.emails,
                    'status': w.status,
                    'nameservers': w.name_servers,
                    'dnssec': w.dnssec,
                    'creation_date': str(w.creation_date),
                    'expiration_date': str(w.expiration_date),
                    'last_updated': str(w.last_updated),
                    'registrant': w.registrant,  # 添加注册人信息字段
                    # 添加 nameservers、dnssec 和 registrant 字段
                }
                domain_info['whois'] = formatted_whois
                # 将查询结果存入缓存
                domain_cache[domain] = formatted_whois
            except whois.parser.PywhoisError:
                unresolved_domains.append(domain)
                domain_info['whois'] = "Not found"
        province_data[province].append(domain_info)


# 遍历目录下的每个 txt 文件并处理域名查询
for filename in os.listdir('../domain_txt'):
    province = filename.split('.txt')[0]

    with open(os.path.join('../domain_txt', filename), 'r', encoding='utf-8') as file:
        urls = file.readlines()
        urls = [url.strip() for url in urls]

    process_domain(province, urls)

# 存储 WHOIS 信息到 JSON 文件
for province, data in province_data.items():
    with open(f'{province}_whois.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# 统计未查询到 WHOIS 信息的域名
unresolved_domains_count = len(unresolved_domains)
with open('unresolved_domains.txt', 'w', encoding='utf-8') as unresolved_file:
    unresolved_file.write('\n'.join(unresolved_domains))

print(f"总共有{unresolved_domains_count}个域名没有找到 WHOIS 信息。")

