import json
import os
import ipaddress


count_cdn = 0
all_data = []
cdn_list = []
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
            # print(data['Name'] + ' use CDN!')
            count_cdn += 1
            # print(addresses)
            cdn_list.append(data)
        is_ipv6 = False
        is_ipv4 = False
        for address in addresses:
            try:
                ip = ipaddress.ip_address(address)
                if ip.version == 6:
                    is_ipv6 = True
                if ip.version == 4:
                    is_ipv4 = True

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
    with open('./use_cdn.json', 'w', encoding='utf-8') as write_file:
        json.dump(cdn_list, write_file,  ensure_ascii=False, indent=None)

print(len(all_data))
# Deduplicating based on the 'Name' field
unique_data = {}
for item in all_data:
    if item['Name'] not in unique_data:
        unique_data[item['Name']] = item

# Convert the dictionary back to a list
deduplicated_data = list(unique_data.values())
print(len(unique_data))

print('CDN total: ', {count_cdn})
print('IPV4 total: ', {ipv4_count})
print('IPV6 total: ', {ipv6_count})
print('Dual Stack total: ', {both_count})
print('None IP: ', {none_count})


'''
    统计结果
    13821
    12795
    CDN total:  {2137}
    IPV4 total:  {710}
    IPV6 total:  {161}
    Dual Stack total:  {12950}
    None IP:  {0}
'''