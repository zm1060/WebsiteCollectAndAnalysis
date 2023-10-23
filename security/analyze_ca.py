import os
import json
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime


def analyze_tls_certificates(root_folder):
    all_data = []

    for province_folder in os.listdir(root_folder):
        province_path = os.path.join(root_folder, province_folder)

        if os.path.isdir(province_path):
            for json_file in os.listdir(province_path):
                json_file_path = os.path.join(province_path, json_file)

                if os.path.isfile(json_file_path) and json_file.endswith(".json"):
                    with open(json_file_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                        all_data.append(json_data)

    return all_data


def analyze_country_and_organization(data):
    print("Country and Organization Analysis:")
    countries = [item.get("issuer", [])[0][0][1] for item in data]
    organizations = [item.get("issuer", [])[1][0][1] if len(item.get("issuer", [])) > 1 else "" for item in data]

    # 创建子图
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # 绘制国家分布图
    axs[0].bar(Counter(countries).keys(), Counter(countries).values(), color='skyblue', edgecolor='black')
    axs[0].set_title("Countries Distribution")
    axs[0].set_xlabel("Country")
    axs[0].set_ylabel("Count")

    # 绘制组织分布图
    axs[1].bar(Counter(organizations).keys(), Counter(organizations).values(), color='lightcoral', edgecolor='black')
    axs[1].set_title("Organizations Distribution")
    axs[1].set_xlabel("Organization")
    axs[1].set_ylabel("Count")

    plt.tight_layout()  # 调整布局，防止重叠
    plt.show()


def analyze_certificate_versions(data):
    print("Certificate Versions Analysis:")
    versions = [cert.get("version", "") for item in data for cert in item.get("cert_chain", [])]

    # 绘制证书版本分布图
    plt.bar(Counter(versions).keys(), Counter(versions).values(), color='lightgreen', edgecolor='black')
    plt.title("Certificate Versions Distribution")
    plt.xlabel("Certificate Version")
    plt.ylabel("Count")
    plt.show()


def analyze_tls_version(data):
    tls_versions = Counter(item.get("tls_version", "") for item in data)

    # 绘制 TLS 版本分布图
    plt.bar(tls_versions.keys(), tls_versions.values(), color='lightblue', edgecolor='black')
    plt.title("TLS Versions Distribution")
    plt.xlabel("TLS Version")
    plt.ylabel("Count")
    plt.show()
    return tls_versions


def analyze_certificate_validity_period(data):
    valid_from_dates = [datetime.strptime(item.get("valid_from", ""), "%b %d %H:%M:%S %Y %Z") for item in data]
    valid_until_dates = [datetime.strptime(item.get("valid_until", ""), "%b %d %H:%M:%S %Y %Z") for item in data]

    # 绘制证书有效期时间序列图
    plt.figure(figsize=(12, 6))
    plt.plot(valid_from_dates, label='Valid From', marker='o', linestyle='-', color='orange')
    plt.plot(valid_until_dates, label='Valid Until', marker='o', linestyle='--', color='purple')
    plt.title("Certificate Validity Period")
    plt.xlabel("Certificate Index")
    plt.ylabel("Date")
    plt.legend()
    plt.show()

    return valid_from_dates, valid_until_dates


# 设置你的根目录
root_folder = "./ca"

# 进行数据分析
all_data = analyze_tls_certificates(root_folder)
analyze_country_and_organization(all_data)
analyze_certificate_versions(all_data)
analyze_certificate_validity_period(all_data)
analyze_tls_version(all_data)
