from statistics import median, mode

import json
import csv

with open('./total_name_server.json', 'r', encoding='utf-8') as f:
    nameservers = json.load(f)

# 创建一个字典用于存储每个nameserver的出现次数
nameserver_count = {}

# 统计每个nameserver的出现次数
for record in nameservers:
    # Extract second-level and top-level domains
    parts = record.lower().split('.')
    domain_length = len(parts)
    if len(parts) >= 2:
        if domain_length >= 2:
            # For domains with 3 parts, match the last 2
            if domain_length == 3:
                key = '.'.join(parts[-2:])
            # For domains with 4 parts, match the last 3
            elif domain_length == 4:
                key = '.'.join(parts[-3:])
            else:
                # Handle other cases as needed
                key = '.'.join(parts[-2:])

        nameserver_count[key] = nameserver_count.get(key, 0) + 1

# 排序结果
sorted_results = sorted(nameserver_count.items(), key=lambda x: x[1], reverse=True)

# 输出统计结果到CSV文件
csv_filename = 'nameserver_counts_full.csv'
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Domain', 'Nameserver Count'])  # Write header
    csv_writer.writerows(sorted_results)

print(f"Results written to {csv_filename}")

with open('./nameserver_ip.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ipv4_counts = []
ipv6_counts = []
unique_ipv4_addresses = set()
unique_ipv6_addresses = set()

for record in data:
    ipv4_count = sum(1 for ip in record['ips'] if ':' not in ip)
    ipv6_count = sum(1 for ip in record['ips'] if ':' in ip)
    unique_ipv4_addresses.update(ip for ip in record['ips'] if ':' not in ip)
    unique_ipv6_addresses.update(ip for ip in record['ips'] if ':' in ip)
    ipv4_counts.append(ipv4_count)
    ipv6_counts.append(ipv6_count)

# 计算每个记录中 IPv4 和 IPv6 地址数量的中位数和众数
median_ipv4_count = median(ipv4_counts)
mode_ipv4_count = mode(ipv4_counts)

median_ipv6_count = median(ipv6_counts)
mode_ipv6_count = mode(ipv6_counts)

# 计算单个记录中 IPv4 和 IPv6 地址数量的最大、最小和平均值
max_ipv4_count = max(ipv4_counts)
min_ipv4_count = min(ipv4_counts)
avg_ipv4_count = sum(ipv4_counts) / len(ipv4_counts)

max_ipv6_count = max(ipv6_counts)
min_ipv6_count = min(ipv6_counts)
avg_ipv6_count = sum(ipv6_counts) / len(ipv6_counts)

# 输出所有统计信息
print(f"Total IPv4: {sum(ipv4_counts)}")
print(f"Total IPv6: {sum(ipv6_counts)}")
print(f"Unique IPv4 Addresses: {len(unique_ipv4_addresses)}")
print(f"Unique IPv6 Addresses: {len(unique_ipv6_addresses)}")

print(f"Median IPv4 Count: {median_ipv4_count}")
print(f"Mode IPv4 Count: {mode_ipv4_count}")
print(f"Max IPv4 Count: {max_ipv4_count}")
print(f"Min IPv4 Count: {min_ipv4_count}")
print(f"Avg IPv4 Count: {avg_ipv4_count}")

print(f"Median IPv6 Count: {median_ipv6_count}")
print(f"Mode IPv6 Count: {mode_ipv6_count}")
print(f"Max IPv6 Count: {max_ipv6_count}")
print(f"Min IPv6 Count: {min_ipv6_count}")
print(f"Avg IPv6 Count: {avg_ipv6_count}")
