import json
from collections import defaultdict
from urllib.parse import urlparse

# 读取JSON数据
with open('http_https_results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 初始化统计变量
domain_data = defaultdict(lambda: {"http": False, "https": False, "error": None})

# 初始化域名列表
http_only_domains = []
https_only_domains = []
both_domains = []
no_support_domains = []
# 初始化域名列表
merged_domains = []

# 遍历所有记录
for result in data:
    domain = result["url"]

    if "https_support" in result:
        domain_data[domain]["https"] = result.get("https_support", False)
        continue
    if "http_support" in result:
        domain_data[domain]["http"] = result.get("http_support", False)
        continue

for result in data:
    domain = result["url"]
    # Check if 'error' key is present before accessing it
    if "error" in result and result["error"] and (not domain_data[domain]["http"] and not domain_data[domain]["https"]):
        domain_data[domain]["error"] = result["error"]


# 将不同类型的域名放入对应列表
for domain, info in domain_data.items():
    if info["http"] and not info["https"]:
        http_only_domains.append(domain)
    elif not info["http"] and info["https"]:
        https_only_domains.append(domain)
    elif info["http"] and info["https"]:
        both_domains.append(domain)
    else:
        no_support_domains.append(domain)

    # Access 'error' key with a default value of None
    merged_domains.append({
        "url": domain,
        "http_support": info["http"],
        "https_support": info["https"],
        "error": info.get("error", None)
    })

# 输出统计结果
print("Domains supporting only HTTP:", len(http_only_domains))
print("Domains supporting only HTTPS:", len(https_only_domains))
print("Domains supporting both HTTP and HTTPS:", len(both_domains))
print("Domains with no support:", len(no_support_domains))
print("Total number of domains:", len(domain_data))


count = 0
for domain in merged_domains:
    if domain['error']:
        print(domain)
        count += 1
print(count)
# for domain in no_support_domains:
#     print(domain)
#
# Domains supporting only HTTP: 6747
# Domains supporting only HTTPS: 329
# Domains supporting both HTTP and HTTPS: 6434
# Domains with no support: 488
# Total number of domains: 13998
#
#
# certificate verify failed: certificate has expired: 267
# certificate verify failed: unable to get local issuer certificate: 854
# certificate verify failed: self signed certificate: 646
# SSLCertVerificationError "hostname  doesn't match either of: 1607
# Exceeded 30 redirects: 31
# getaddrinfo failed: 346
# 502: 11
# 503: 5
# 404: 39
# 403: 190
# 412: 147
