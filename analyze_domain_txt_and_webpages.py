import json

with open('./province_data.json', 'r', encoding='utf-8') as f:
    province_data = json.load(f)

# 创建一个字典用于存储每个省的链接信息
province_links_data = {}



for data in province_data:
    province_name = data['province']
    province_sites = data['sites']

    # 初始化省的链接信息
    province_links_data[province_name] = {
        'internal_links_count': 0,
        'external_links_count': 0,
        'potential_threat_links_count': 0,
        'total_links_count': 0,
    }

    # 遍历每个站点，累加链接数量
    for site in province_sites:
        province_links_data[province_name]['internal_links_count'] += site['internal_links_count']
        province_links_data[province_name]['external_links_count'] += site['external_links_count']
        province_links_data[province_name]['potential_threat_links_count'] += site['potential_threat_links_count']
        province_links_data[province_name]['total_links_count'] += site['total_links_count']
        external_links = site['external_links']
