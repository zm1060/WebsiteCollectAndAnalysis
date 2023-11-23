import os
import json
import csv
import random
import re
import socket
import time
import pandas as pd

import folium

from collections import Counter, defaultdict

import matplotlib
import requests
from folium.plugins import MarkerCluster
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

import seaborn as sns
from qqwry import QQwry

IPDB_FILE = "qqwry.dat"

font_path = '../SimHei.ttf'  # Replace with the path to a Chinese font file (.ttf)
font_prop = FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'

sns.set(style="whitegrid")

import requests


def get_ipv6_info(ipv6_address):
    api_url = f'https://api.a76yyyy.cn/ip?function=ipv6Info&params1={ipv6_address}'

    try:
        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            if 'code' in data and data['code'] == 200:
                ipv6_info = data['data']
                return ipv6_info.get('详细地址', ''), ipv6_info.get('运营商/节点', '')
            else:
                print(f"API returned an error: {data.get('msg', 'Unknown error')}")
        else:
            print(f"HTTP error: {response.status_code}")

    except Exception as e:
        print(f"An error occurred while fetching IPv6 information: {e}")

    return '', ''


def get_ip_address_isp(ip):
    q = QQwry()
    q.load_file(IPDB_FILE)
    res = q.lookup(ip.strip())
    return res[0], res[1]


def get_ipv4_ipv6_addresses(domain):
    try:
        # Get address information for both IPv4 and IPv6
        addr_info = socket.getaddrinfo(domain, None, socket.AF_UNSPEC)

        # Extract and print the IPv4 and IPv6 addresses
        ipv4_addresses = []
        ipv6_addresses = []
        for info in addr_info:
            family, _, _, _, address = info
            if family == socket.AF_INET:
                ipv4_addresses.append(address[0])
            elif family == socket.AF_INET6:
                ipv6_addresses.append(address[0])

        return ipv4_addresses, ipv6_addresses
    except socket.gaierror:
        # Handle DNS resolution error here
        return [], []


def process_province_directories(class_directory):
    # 遍历省份目录
    for province_dir in os.listdir(class_directory):
        province_path = os.path.join(class_directory, province_dir)
        # 存储地理位置信息的列表
        location_data = []
        # 已解析的nameserver集合
        processed_nameservers = set()

        # 遍历每个省份目录下的json文件
        for file in os.listdir(province_path):
            if file.endswith(".json"):
                file_path = os.path.join(province_path, file)

                # 读取json文件内容
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    domain_data = json.load(json_file)
                # 获取每个nameserver的地理位置信息
                nameservers = domain_data.get("name_servers", [])
                if isinstance(nameservers, str):
                    nameservers = [nameservers]  # 如果是字符串，将其转换为列表
                if nameservers is not None:
                    for nameserver in nameservers:
                        if nameserver not in processed_nameservers:
                            processed_nameservers.add(nameserver)

                            print(nameserver)
                            time.sleep(0.2)
                            try:

                                ipv4_addresses, ipv6_addresses = get_ipv4_ipv6_addresses(nameserver)
                                if ipv4_addresses:
                                    # If IPv4 addresses are available, use the first one
                                    ipv4_address = ipv4_addresses[0]
                                    region, isp = get_ip_address_isp(ipv4_address)
                                    ip_version = 'IPv4'

                                elif ipv6_addresses:
                                    # If IPv6 addresses are available, use the first one
                                    ipv6_address = ipv6_addresses[0]
                                    region, isp = get_ipv6_info(ipv6_address)
                                    ip_version = 'IPv6'
                                ip = ipv4_addresses if ip_version == "IPv4" else ipv6_addresses
                            except Exception as e:
                                print()

                            # 存储地理位置信息到列表
                            location_info = {
                                'province': province_dir,
                                'nameserver': nameserver,
                                'ip': ip,
                                'ip_version': ip_version,
                                'region': region,
                                'isp': isp
                            }
                            print(location_info)
                            location_data.append(location_info)

        # 将地理位置信息写入JSON文件
        with open(f'./whois_full/{province_dir}.json', 'w', encoding='utf-8') as json_output:
            json.dump(location_data, json_output, ensure_ascii=False, indent=2)


def save_isp_data_to_csv(region_isp_data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Region', 'ISP', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for region, isp_count in region_isp_data.items():
            for isp, count in isp_count.items():
                writer.writerow({'Region': region, 'ISP': isp, 'Count': count})


region_data = [
    {"name": '中国', "value": [114.3979471, 37.9081726, 0]},
    {"name": '北京', "value": [116.3979471, 39.9081726, 78]},
    {"name": '上海', "value": [121.4692688, 31.2381763, 75]},
    {"name": '天津', "value": [117.2523808, 39.1038561, 95]},
    {"name": '重庆', "value": [106.548425, 29.5549144, 78]},
    {"name": '河北', "value": [114.4897766, 38.0451279, 42]},
    {"name": '山西', "value": [112.5223053, 37.8357424, 90]},
    {"name": '辽宁', "value": [123.4116821, 41.7966156, 96]},
    {"name": '吉林', "value": [125.3154297, 43.8925629, 46]},
    {"name": '黑龙江', "value": [126.6433411, 45.7414932, 97]},
    {"name": '浙江', "value": [120.1592484, 30.265995, 32]},
    {"name": '福建', "value": [119.2978134, 26.0785904, 2]},
    {"name": '山东', "value": [117.0056, 36.6670723, 32]},
    {"name": '河南', "value": [113.6500473, 34.7570343, 23]},
    {"name": '湖北', "value": [114.2919388, 30.5675144, 76]},
    {"name": '湖南', "value": [112.9812698, 28.2008247, 71]},
    {"name": '广东', "value": [113.2614288, 23.1189117, 6]},
    {"name": '海南', "value": [110.3465118, 20.0317936, 64]},
    {"name": '四川', "value": [104.0817566, 30.6610565, 54]},
    {"name": '贵州', "value": [106.7113724, 26.5768738, 1]},
    {"name": '云南', "value": [102.704567, 25.0438442, 78]},
    {"name": '江西', "value": [115.8999176, 28.6759911, 16]},
    {"name": '陕西', "value": [108.949028, 34.2616844, 14]},
    {"name": '青海', "value": [101.7874527, 36.6094475, 22]},
    {"name": '甘肃', "value": [103.7500534, 36.0680389, 37]},
    {"name": '广西', "value": [108.3117676, 22.8065434, 52]},
    {"name": '新疆', "value": [87.6061172, 43.7909393, 11]},
    {"name": '内蒙古', "value": [111.6632996, 40.8209419, 56]},
    {"name": '西藏', "value": [91.1320496, 29.657589, 6]},
    {"name": '宁夏', "value": [106.2719421, 38.4680099, 64]},
    {"name": '台湾', "value": [120.9581316, 23.8516062, 49]},
    {"name": '香港', "value": [114.139452, 22.391577, 49]},
    {"name": '澳门', "value": [113.5678411, 22.167654, 36]},
    {"name": '安徽', "value": [117.2757034, 31.8632545, 78]},
    {"name": '江苏', "value": [118.7727814, 32.0476151, 98]},
    {"name": "南非约翰内斯堡", "value": [-26.2041, 28.0473, 1]},
    {"name": "亚太地区", "value": [35, 105, 1]},
    {"name": "美国", "value": [37.7749, -122.4194, 1]},
    {"name": "法国", "value": [48.8566, 2.3522, 1]},
    {"name": "局域网", "value": [0, 0, 1]},
    {"name": "巴西圣保罗", "value": [-23.5505, -46.6333, 1]},
    {"name": "马来西亚", "value": [4.2105, 101.9758, 1]},
]


def get_coordinates(region_name, region_data):
    for item in region_data:
        if item["name"] in region_name:
            return item["value"]  # 返回经度、纬度和数值
    return None  # 如果没有匹配的数据，返回 None 或其他适当的值


def geospatial_analysis(nameservers, province_dir, output_dir):
    # 创建一个字典来跟踪每个区域的ISP计数
    region_isp_count = defaultdict(Counter)
    # Creating a colormap for ISPs
    isp_colors = {
        '移动': 'blue',
        '电信': 'red',
        '联通': 'green',
        '联通IDC机房': 'green',
        '阿里云': 'purple',
        '阿里云BGP数据中心': 'purple',
        '阿里云VIPDNS Anycast节点': 'purple',
        '腾讯云': 'orange',
        '公司': 'black',
        'local_or_error': 'red',
        # Add more ISPs and their respective colors as needed
    }
    isp_rgb_colors = {
        '移动': (0, 0, 255),  # Blue
        '电信': (255, 0, 0),  # Red
        '联通': (0, 128, 0),  # Green
        '阿里云': (128, 0, 128),  # Purple
        '腾讯云': (255, 165, 0),  # Orange
        '公司': (0, 0, 0),  # Black
        'local_or_error': (255, 0, 0),
        # Add more ISPs and their respective RGB values as needed
    }

    # 创建地图
    m = folium.Map(location=[35, 105], zoom_start=5,
                   tiles='http://webst02.is.autonavi.com/appmaptile?lang=en&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                   attr='default')

    # Creating a dictionary to store MarkerClusters for each province
    province_clusters = defaultdict(MarkerCluster)

    china_sea_center = [30.0, 125.0]

    # 保存每个nameserver负责解析域名的数量
    nameserver_domain_map = {}
    # 保存发生错误的nameserver
    error_nameservers = []

    for nameserver in nameservers:
        if is_valid_domain(nameserver):
            try:
                ip = ''
                region = ''
                isp = ''
                ip_version = ''
                try:
                    ipv4_addresses, ipv6_addresses = get_ipv4_ipv6_addresses(nameserver)
                    if ipv4_addresses:
                        # If IPv4 addresses are available, use the first one
                        ipv4_address = ipv4_addresses[0]
                        region, isp = get_ip_address_isp(ipv4_address)
                        ip_version = 'IPv4'

                    elif ipv6_addresses:
                        # If IPv6 addresses are available, use the first one
                        ipv6_address = ipv6_addresses[0]
                        region, isp = get_ipv6_info(ipv6_address)
                        ip_version = 'IPv6'
                    ip = ipv4_addresses if ip_version == "IPv4" else ipv6_addresses

                except Exception as e:
                    print()
                region_isp_count[region][isp] += 1
                # 记录nameserver负责解析的域名数量
                if region in nameserver_domain_map:
                    nameserver_domain_map[region][nameserver] = nameserver_domain_map[region].get(nameserver, 0) + 1
                else:
                    nameserver_domain_map[region] = {nameserver: 1}

                coordinates = get_coordinates(region, region_data)
                longitude = 116.3979471
                latitude = 39.9081726
                if coordinates:
                    longitude, latitude, value = coordinates
                    longitude += random.uniform(-0.02, 0.02)
                    latitude += random.uniform(-0.02, 0.02)
                    print(f"Region: {region}, Longitude: {longitude}, Latitude: {latitude}, Value: {value}")
                else:
                    print(f"No coordinates found for {region}")

                # Get the color for the ISP
                isp_color = 'gray'  # Default color if not found
                for keyword, color in isp_colors.items():
                    if keyword in isp:
                        isp_color = color
                        break

                # 使用 folium.Icon 时，确保 isp_color 在 Folium 支持的颜色列表中
                if isp_color not in ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige',
                                     'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue',
                                     'lightgreen', 'gray', 'black', 'lightgray']:
                    isp_color = 'gray'

                # 添加标记到地图上
                folium.Marker([float(latitude), float(longitude)],
                              icon=folium.Icon(color=isp_color),
                              popup=f"Nameserver: {nameserver}\nIP: {ip}\nRegion: {region}\nISP: {isp}").add_to(
                    province_clusters[region])
            except Exception as e:
                print(f"Error for {nameserver}: {str(e)}")
                # 如果发生错误，将标记放置在中国东海的中心
                error_nameservers.append(nameserver)

                folium.Marker(china_sea_center,
                              icon=folium.Icon(color='red'),
                              popup=f"Error for {nameserver}: {str(e)}").add_to(province_clusters['local_or_error'])
    # 保存每个省的 ISP 数据到 CSV 文件
    csv_output_path = os.path.join(output_dir, f"{province_dir}_isp_data.csv")
    save_isp_data_to_csv(region_isp_count, csv_output_path)

    # 写入nameserver负责解析域名的数量到JSON文件
    if nameserver_domain_map is not None:
        nameserver_domain_map_file = os.path.join(output_dir, f"{province_dir}_nameserver_domain_map.json")
        with open(nameserver_domain_map_file, 'w', encoding='utf-8') as f:
            json.dump(nameserver_domain_map, f, ensure_ascii=False, indent=2)

    # 写入发生错误的nameserver到JSON文件
    if error_nameservers is not None:
        error_nameservers_file = os.path.join(output_dir, f"{province_dir}_local_nameserver.json")
        with open(error_nameservers_file, 'w', encoding='utf-8') as f:
            json.dump({"error_nameservers": error_nameservers}, f, ensure_ascii=False, indent=2)

    # 遍历区域和对应的Cluster，找到每个区域最多的ISP，设置Cluster的颜色
    for region, cluster in province_clusters.items():
        isp_count = region_isp_count.get(region)
        if isp_count is None:
            continue

        # 找到最多的 ISP 和对应的颜色
        most_common_isp, count = isp_count.most_common(1)[0]
        isp_color = isp_rgb_colors.get(most_common_isp, (128, 128, 128,))  # Default to gray if ISP not found
        print(f"{region} Most common {most_common_isp}:{isp_count} with {isp_color} ")

        # 设置 Cluster 的颜色
        cluster.icon_create_function = f"""
            function(cluster) {{
                var childCount = cluster.getChildCount();
                var size = 5 + Math.min(childCount, 90) * 0.1;

                return new L.DivIcon({{
                    html: '<div style="border: 2px solid rgb({isp_color[0]}, {isp_color[1]}, {isp_color[2]}); background-color: rgba({isp_color[0]}, {isp_color[1]}, {isp_color[2]}, 0.8); color: white; font-size: 12px; display: flex; justify-content: center; align-items: center;" class="marker-cluster">' + childCount + '</div>',
                    className: 'marker-cluster',
                    iconSize: new L.Point(size, size)
                }});
            }}
        """
        cluster.layer_name = region
        # 将新的 Cluster 图层添加到地图上
        cluster.add_to(m)

    # 保存地图
    m.save(os.path.join(output_dir, f"{province_dir}_地理空间分析地图.html"))


def is_valid_domain(domain):
    # 使用正则表达式检查域名格式
    pattern = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*$")
    return bool(pattern.match(domain))


def process_province_statistics(class_directory, output_dir):
    total_registrar_counter = Counter()
    total_status_counter = Counter()
    total_dnssec_counter = Counter()
    total_name_server = []
    # 遍历省份目录
    for province_dir in os.listdir(class_directory):
        province_path = os.path.join(class_directory, province_dir)
        data = []
        nameservers = []

        registrar_counter = Counter()
        status_counter = Counter()
        dnssec_counter = Counter()
        # 遍历每个省份目录下的json文件
        for file in os.listdir(province_path):
            if file.endswith(".json"):
                file_path = os.path.join(province_path, file)

                # 读取json文件内容
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    domain_data = json.load(json_file)
                    data.append(domain_data)
                    # 获取nameservers
                    name_servers = domain_data.get("name_servers")
                    if name_servers:
                        if not isinstance(name_servers, list):
                            # Convert to list if it's not already
                            name_servers = [name_servers]
                        print(name_servers)
                        print("-------")
                        nameservers.extend(name_servers)
                        total_name_server.extend(name_servers)

                # 统计registrar
                registrar_key = domain_data["registrar"] if domain_data["registrar"] else "Unknown"
                registrar_counter[registrar_key] += 1
                total_registrar_counter[registrar_key] += 1

                # 统计status
                if isinstance(domain_data["status"], list):
                    # 如果 "status" 是一个列表，则逐个统计每个状态
                    for status in domain_data["status"]:
                        status_counter[status] += 1
                        total_status_counter[status] += 1
                # 统计status
                else:
                    status_key = domain_data["status"][0] if domain_data["status"] else "Unknown"
                    status_counter[status_key] += 1
                    total_status_counter[status_key] += 1

                # 统计dnssec
                dnssec_key = domain_data["dnssec"] if domain_data["dnssec"] else "Unknown"
                dnssec_counter[dnssec_key] += 1
                total_dnssec_counter[dnssec_key] += 1
        # 进行地理空间分析
        geospatial_analysis(nameservers, province_dir, output_dir)

        # df = pd.DataFrame(data)
        # df = df.dropna(subset=['dnssec', 'expiration_date'])
        #
        # # 创建Registrar统计条形图
        # plt.figure(figsize=(12, 6))
        # sns.countplot(x='registrar', data=df)
        # plt.title("Registrar统计")
        # plt.xlabel("Registrar")
        # plt.ylabel("Count")
        # plt.xticks(rotation=45, ha="right")
        # plt.tight_layout()
        # plt.show()
        #
        # # 创建Status统计饼图
        # plt.figure(figsize=(8, 8))
        # df['status'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
        # plt.title("Status统计")
        # plt.show()
        #
        # # 创建DNSSEC统计箱线图
        # plt.figure(figsize=(12, 6))
        # sns.boxplot(x='dnssec', y='expiration_date', data=df)
        # plt.title("DNSSEC统计")
        # plt.xlabel("DNSSEC")
        # plt.ylabel("Expiration Date")
        # plt.xticks(rotation=45, ha="right")
        # plt.tight_layout()
        # plt.show()
        #
        # # 将 'creation_date' 和 'expiration_date' 列转换为日期时间类型
        # df['creation_date'] = pd.to_datetime(df['creation_date'])
        # df['expiration_date'] = pd.to_datetime(df['expiration_date'])
        #
        # # 创建Creation Date vs Expiration Date散点图
        # plt.figure(figsize=(12, 8))
        # sns.scatterplot(x='creation_date', y='expiration_date', hue='registrar', data=df)
        # plt.title("Creation Date vs Expiration Date")
        # plt.xlabel("Creation Date")
        # plt.ylabel("Expiration Date")
        # plt.xticks(rotation=45, ha="right")
        # plt.tight_layout()
        # plt.show()

    #     # 创建一个散点图
    #     plt.figure(figsize=(12, 8))
    #     sns.scatterplot(x='creation_date', y='expiration_date', hue='registrar', data=df)
    #     plt.title(f"Creation Date vs Expiration Date - {province_dir}")
    #     plt.xlabel("Creation Date")
    #     plt.ylabel("Expiration Date")
    #     plt.xticks(rotation=45, ha="right")
    #     plt.tight_layout()
    #     plt.savefig(os.path.join(output_dir, f"{province_dir}_creation_vs_expiration_scatterplot.png"))
    #     plt.close()
    #     # 生成并保存每个省份的注册商统计结果的条形图
    #     plt.bar(registrar_counter.keys(), registrar_counter.values())
    #     plt.title(f"Registrar Statistics - {province_dir}")
    #     plt.xlabel("Registrar")
    #     plt.ylabel("Count")
    #     plt.xticks(rotation=45, ha="right")
    #     plt.tight_layout()
    #     plt.savefig(os.path.join(output_dir, f"{province_dir}_registrar.png"))
    #     plt.close()
    #
    #     # 生成并保存每个省份的状态统计结果的条形图
    #     plt.bar(status_counter.keys(), status_counter.values())
    #     plt.title(f"Status Statistics - {province_dir}")
    #     plt.xlabel("Status")
    #     plt.ylabel("Count")
    #     plt.xticks(rotation=45, ha="right")
    #     plt.tight_layout()
    #     plt.savefig(os.path.join(output_dir, f"{province_dir}_status.png"))
    #     plt.close()
    #
    #     # 生成并保存每个省份的DNSSEC统计结果的条形图
    #     plt.bar(dnssec_counter.keys(), dnssec_counter.values())
    #     plt.title(f"DNSSEC Statistics - {province_dir}")
    #     plt.xlabel("DNSSEC")
    #     plt.ylabel("Count")
    #     plt.xticks(rotation=45, ha="right")
    #     plt.tight_layout()
    #     plt.savefig(os.path.join(output_dir, f"{province_dir}_dnssec.png"))
    #     plt.close()
    #
    # # 生成并保存总体注册商统计结果的条形图
    # plt.bar(total_registrar_counter.keys(), total_registrar_counter.values())
    # plt.title("Total Registrar Statistics")
    # plt.xlabel("Registrar")
    # plt.ylabel("Count")
    # plt.xticks(rotation=45, ha="right")
    # plt.tight_layout()
    # plt.savefig(os.path.join(output_dir, "total_registrar.png"))
    # plt.close()
    #
    # # 生成并保存总体状态统计结果的条形图
    # plt.bar(total_status_counter.keys(), total_status_counter.values())
    # plt.title("Total Status Statistics")
    # plt.xlabel("Status")
    # plt.ylabel("Count")
    # plt.xticks(rotation=45, ha="right")
    # plt.tight_layout()
    # plt.savefig(os.path.join(output_dir, "total_status.png"))
    # plt.close()
    #
    # # 生成并保存总体DNSSEC统计结果的条形图
    # plt.bar(total_dnssec_counter.keys(), total_dnssec_counter.values())
    # plt.title("Total DNSSEC Statistics")
    # plt.xlabel("DNSSEC")
    # plt.ylabel("Count")
    # plt.xticks(rotation=45, ha="right")
    # plt.tight_layout()
    # plt.savefig(os.path.join(output_dir, "total_dnssec.png"))
    # plt.close()
    geospatial_analysis(total_name_server, 'total', output_dir)


if __name__ == "__main__":
    class_directory = "./class"
    # get location of nameserver
    # os.makedirs('./whois_full', exist_ok=True)
    # process_province_directories(class_directory)
    output_dir = "./new_whois_analyze"
    os.makedirs('./new_whois_analyze', exist_ok=True)
    process_province_statistics(class_directory, output_dir)
