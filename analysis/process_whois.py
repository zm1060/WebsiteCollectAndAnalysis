import os
import json
import random
import re
import socket
import time
import folium
from collections import Counter, defaultdict

import matplotlib
from folium.plugins import MarkerCluster
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

import seaborn as sns
import pandas as pd
from qqwry import QQwry

IPDB_FILE = "qqwry.dat"

font_path = '../SimHei.ttf'  # Replace with the path to a Chinese font file (.ttf)
font_prop = FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'

sns.set(style="whitegrid")


def get_ip_address_isp(ip):
    q = QQwry()
    q.load_file(IPDB_FILE)
    res = q.lookup(ip.strip())
    return res[0], res[1]


def process_province_directories(class_directory):
    # 存储地理位置信息的列表
    location_data = []
    # 已解析的nameserver集合
    processed_nameservers = set()

    # 遍历省份目录
    for province_dir in os.listdir(class_directory):
        province_path = os.path.join(class_directory, province_dir)

        # 遍历每个省份目录下的json文件
        for file in os.listdir(province_path):
            if file.endswith(".json"):
                file_path = os.path.join(province_path, file)

                # 读取json文件内容
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    domain_data = json.load(json_file)
                # 获取每个nameserver的地理位置信息
                if domain_data["name_servers"]:
                    for nameserver in domain_data["name_servers"]:
                        if nameserver not in processed_nameservers:
                            processed_nameservers.add(nameserver)

                            print(nameserver)
                            time.sleep(0.2)
                            try:
                                ip = socket.gethostbyname(nameserver)
                                region, isp = get_ip_address_isp(ip)
                            except Exception as e:
                                print()

                            # 存储地理位置信息到列表
                            location_info = {
                                'province': province_dir,
                                'nameserver': nameserver,
                                'ip': ip,
                                'region': region,
                                'isp': isp
                            }
                            location_data.append(location_info)

            # 将地理位置信息写入JSON文件
            with open(f'./whois_full/{province_dir}.json', 'w', encoding='utf-8') as json_output:
                json.dump(location_data, json_output, ensure_ascii=False, indent=2)


region_data = [
    {"name": '中国', "value": [116.3979471, 39.9081726, 0]},
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
    {"name": "巴西圣保罗", "value": [-23.5505, -46.6333, 1]}
]


def get_coordinates(region_name, region_data):
    for item in region_data:
        if item["name"] in region_name:
            return item["value"]  # 返回经度、纬度和数值
    return None  # 如果没有匹配的数据，返回 None 或其他适当的值


def geospatial_analysis(nameservers, province_dir, output_dir):
    # Creating a colormap for ISPs
    isp_colors = {
        '移动': 'blue',
        '电信': 'red',
        '联通': 'green',
        '阿里云': 'purple',
        '腾讯云': 'orange',
        # Add more ISPs and their respective colors as needed
    }

    # 创建地图
    m = folium.Map(location=[35, 105], zoom_start=5)

    # Creating a dictionary to store MarkerClusters for each province
    province_clusters = defaultdict(MarkerCluster)

    for nameserver in nameservers:
        if is_valid_domain(nameserver):
            try:
                ip = socket.gethostbyname(nameserver)
                region, isp = get_ip_address_isp(ip)
                coordinates = get_coordinates(region, region_data)
                longitude = 116.3979471
                latitude = 39.9081726
                if coordinates:
                    longitude, latitude, value = coordinates
                    longitude += random.uniform(-0.2, 0.2)
                    latitude += random.uniform(-0.2, 0.2)
                    print(f"Region: {region}, Longitude: {longitude}, Latitude: {latitude}, Value: {value}")
                else:
                    print(f"No coordinates found for {region}")

                # Get the color for the ISP
                isp_color = 'gray'  # Default color if not found
                for keyword, color in isp_colors.items():
                    if keyword in isp:
                        isp_color = color
                        break

                # 添加标记到地图上
                folium.Marker([float(latitude), float(longitude)],
                              icon=folium.Icon(color=isp_color),
                              popup=f"Nameserver: {nameserver}\nIP: {ip}\nRegion: {region}\nISP: {isp}").add_to(province_clusters[region])
            except Exception as e:
                print(f"Error for {nameserver}: {str(e)}")

    # Adding MarkerClusters for each province to the map
    for region, cluster in province_clusters.items():
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
