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


def get_ip_address_isp(ip):
    q = QQwry()
    q.load_file(IPDB_FILE)
    res = q.lookup(ip.strip())
    return res[0], res[1]


def get_ip_addres_isp_by_api(ip):
    url = "https://api.ip2location.io/?key=3396D10054F53DC2768CB93656AFCBD8&ip=" + ip


def process_province_directories(class_directory):
    # ...
    # Your existing code here
    # ...
    processed_nameservers = set()  # Keep track of processed nameservers

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

    # ...
    # Continue with the rest of your code
    # ...


if __name__ == "__main__":
    class_directory = "./class"
    output_dir = "./new_whois_analyze"
    os.makedirs('./new_whois_analyze', exist_ok=True)
    process_province_statistics(class_directory, output_dir)
