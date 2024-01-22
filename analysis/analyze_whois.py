import json

from collections import Counter

import pandas as pd

with open('./new_whois_analyze/total_nameserver_domain_map.json', 'r', encoding='utf-8') as f:
    # 直接使用json.load解析为Python字典
    data = json.load(f)
with open('./total_name_server.json', 'r', encoding='utf-8') as f:
    name_servers = json.load(f)

# 转换为集合并获取唯一的DNS服务器
unique_name_servers = set(name_servers)
print(unique_name_servers)
# 统计唯一的DNS服务器数量
unique_count = len(unique_name_servers)

print("Total DNS Servers:", len(name_servers))
print("Unique DNS Servers:", unique_count)


# 使用Counter统计每个DNS服务器的总次数
dns_counter = Counter()
for city_data in data.values():
    dns_counter.update(city_data)

# 找出前100个最重要的DNS服务器
top_100_dns = dns_counter.most_common(100)
total_dns = dns_counter.most_common()
# 输出结果
for dns_server, count in top_100_dns:
    print(f"{dns_server}: {count} times")

print(top_100_dns)
# 转换为DataFrame
df = pd.DataFrame(top_100_dns, columns=["DNS Server", "Count"])
total_df = pd.DataFrame(total_dns, columns=["DNS Server", "Count"])

# 保存为Excel文件
excel_file_path = "./top_dns_servers.xlsx"
excel_file_path_for_total = "./total_dns_servers.xlsx"
df.to_excel(excel_file_path, index=False)
total_df.to_excel(excel_file_path_for_total, index=False)
print(f"Excel file saved at: {excel_file_path}")
print(f"Excel file saved at: {excel_file_path_for_total}")

# Counter({'unsigned': 12026, 'Unknown': 471})

# Beijing Guoke Cloud Computing Technology Co., Ltd. : 5324,
# Alibaba Cloud Computing Co. Ltd. : 2509
# Xin Net Technology Corp. :1974
# Bizcn.com, Inc. : 645
# LeascendTechnology Co., Ltd : 513
# Unknown: 471
# Guangdong HUYI Internet & IP Services Co., Ltd. : 334
# CE Dongli Technology Company Limited. : 114
# Xiamen Nawang Technology Co.,Ltd. : 86
# Beijing GuoxuNetwork Technology Co.,Ltd. : 75

# {
#  '北京中科三方网络技术有限公司': 5324,
#  '阿里云计算有限公司（万网）': 2509,
#  '北京新网数码信息技术有限公司': 1974,
#  '商中在线科技股份有限公司': 645,
#  '厦门三五互联科技股份有限公司': 513,
#  'Unknown': 471,
#  '广东互易网络知识产权有限公司': 334,
#  '中企动力科技股份有限公司': 114,
#  '厦门纳网科技股份有限公司': 86,
#  '北京国旭网络科技有限公司': 75,
# }
# Counter({'北京中科三方网络技术有限公司': 5324, '阿里云计算有限公司（万网）': 2509, '北京新网数码信息技术有限公司': 1974, '商中在线科技股份有限公司': 645, '厦门三五互联科技股份有限公司': 513, 'Unknown': 471, '广东互易网络知识产权有限公司': 334, '中企动力科技股份有限公司': 114, '厦门纳网科技股份有限公司': 86, '北京国旭网络科技有限公司': 75, '北京首信网创网络信息服务有限责任公司': 73, '北京万维通港科技有限公司': 61, '广东时代互联科技有限公司': 53, '成都西维数码科技有限公司': 41, '泛亚信息技术江苏有限公司': 41, '成都世纪东方网络通信有限公司': 38, '北京东方网景信息科技有限公司': 33, '江苏邦宁科技有限公司': 31, '上海美橙科技信息发展有限公司': 29, '厦门市中资源网络服务有限公司': 19, '浙江贰贰网络有限公司': 10, 'Alibaba Cloud Computing (Beijing) Co., Ltd.': 5, '深圳市万维网信息技术有限公司': 3, '上海福虎信息科技有限公司': 2, '天津追日科技发展有限公司': 2, '厦门易名科技股份有限公司': 2, '昆明乐网数码科技有限公司': 1, '上海有孚网络股份有限公司': 1, '北京光速连通科贸有限公司': 1, '中移（苏州）软件技术有限公司': 1, '佛山市亿动网络有限公司': 1, '阿里巴巴云计算（北京）有限公司': 1, 'WEST263 INTERNATIONAL LIMITED': 1, '北京宏网神州科技发展有限公司': 1, '北京资海科技有限责任公司': 1})