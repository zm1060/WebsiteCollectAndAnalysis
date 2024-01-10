import json
import os
import ipaddress

count_cdn = 0
all_data = []
cdn_list = []

ip_list = []
ipv6_list = []
all_ip_list = []

ipv6_count = 0
ipv4_count = 0
both_count = 0
none_count = 0

for filename in os.listdir('cleaned_cdn'):
    print(filename)
    unit_name = filename.split('.json')[0]
    unit_data = []

    with open(f'./cleaned_cdn/{filename}', 'r', encoding='utf-8') as json_file:
        unit_data = json.load(json_file)

    for data in unit_data:
        addresses = data['Addresses']
        all_data.append(data)

        if len(addresses) > 3:
            is_cdn = True
            count_cdn += 1
            cdn_list.append(data)

        is_ipv6 = False
        is_ipv4 = False

        for address in addresses:
            try:
                ip = ipaddress.ip_address(address)

                if ip.version == 6:
                    is_ipv6 = True
                    ipv6_list.append(address)

                if ip.version == 4:
                    is_ipv4 = True
                    ip_list.append(address)
                all_ip_list.append(address)
            except ValueError:
                print(f"{address}不是一个有效的IP地址.")

        if is_ipv4 and is_ipv6:
            both_count += 1
        if is_ipv6 and not is_ipv4:
            ipv6_count += 1
            print(data)
        if is_ipv4 and not is_ipv6:
            ipv4_count += 1
            print(data)
        if not is_ipv4 and not is_ipv6:
            none_count += 1
            print("None: ", data)

# 去重 IPv4 和 IPv6 地址
ip_set = set(ip_list)
ipv6_set = set(ipv6_list)
all_ip_list = set(all_ip_list)

# 转回列表，如果你仍然需要它们作为列表
unique_ip_list = list(ip_set)
unique_ipv6_list = list(ipv6_set)
unique_all_ip_list = list(all_ip_list)

# 将去重后的 ipv4 数据写入文件
with open('./ipv4.json', 'w', encoding='utf-8') as write_file:
    json.dump(unique_ip_list, write_file, ensure_ascii=False, indent=None)

# 将去重后的 ipv6 数据写入文件
with open('./ipv6.json', 'w', encoding='utf-8') as write_file:
    json.dump(unique_ipv6_list, write_file, ensure_ascii=False, indent=None)

with open('./ip.txt', 'w', encoding='utf-8') as all_file:
    for ip in all_ip_list:
        all_file.writelines(ip + '\n')

print(len(all_data))
print(len(unique_all_ip_list))
print(len(unique_ip_list))
print(len(unique_ipv6_list))
#  6897个dual stack

# 13821
# 6897
# 3544
# 3353
