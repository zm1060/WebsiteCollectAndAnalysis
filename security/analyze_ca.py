import os
import json
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
    print("Certificate Fields Analysis:")

    collect = {'commonName': {}, 'organizationName': {}, 'countryName': {}}

    for item in data:
        cert_chains = item['cert_chain']
        for cert in cert_chains:
            subject = cert['subject']
            issuer = cert['issuer']

            # Extract values from subject and issuer
            for field in ['commonName', 'organizationName', 'countryName']:
                if field in subject[0][0]:
                    value = subject[0][0][1]
                    if value not in collect[field]:
                        collect[field][value] = 0
                    collect[field][value] += 1

                if field in issuer[0][0]:
                    value = issuer[0][0][1]
                    if value not in collect[field]:
                        collect[field][value] = 0
                    collect[field][value] += 1

    # Plot the results
    for field, values in collect.items():
        plt.figure(figsize=(10, 6))
        plt.bar(values.keys(), values.values(), color='skyblue')
        plt.title(f"{field.capitalize()} Distribution in Certificates")
        plt.xlabel(f"{field.capitalize()} Value")
        plt.ylabel("Count")
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
    tls_versions = Counter(item.get("version", "") for item in data)

    # 绘制 TLS 版本分布图
    plt.bar(tls_versions.keys(), tls_versions.values(), color='lightblue', edgecolor='black')
    plt.title("TLS Versions Distribution")
    plt.xlabel("TLS Version")
    plt.ylabel("Count")
    plt.show()
    return tls_versions


def analyze_issuer(data):
    issuer = Counter(item.get("issuer", "") for item in data)

    # 绘制 TLS 版本分布图
    plt.bar(issuer.keys(), issuer.values(), color='lightblue', edgecolor='black')
    plt.title("Issuer Distribution")
    plt.xlabel("Issuer")
    plt.ylabel("Count")
    plt.show()
    return issuer


def analyze_subject(data):
    subject = Counter(item.get("subject", "") for item in data)

    # 绘制 TLS 版本分布图
    plt.bar(subject.keys(), subject.values(), color='lightblue', edgecolor='black')
    plt.title("Subject Distribution")
    plt.xlabel("Subject")
    plt.ylabel("Count")
    plt.show()
    return subject


def analyze_certificate_validity_period(data):
    # 提取日期信息
    valid_from_dates = [datetime.strptime(item.get("valid_from", ""), "%Y%m%d%H%M%SZ") for item in data]
    valid_until_dates = [datetime.strptime(item.get("valid_until", ""), "%Y%m%d%H%M%SZ") for item in data]

    # 生成证书索引列表
    certificate_indices = list(range(1, len(valid_from_dates) + 1))

    # 按照日期升序排列
    valid_from_dates, valid_until_dates, certificate_indices = zip(
        *sorted(zip(valid_from_dates, valid_until_dates, certificate_indices)))

    # 绘制证书有效期时间序列图
    plt.figure(figsize=(12, 6))
    plt.plot(certificate_indices, valid_from_dates, label='Valid From', marker='o', linestyle='-', color='orange')
    plt.plot(certificate_indices, valid_until_dates, label='Valid Until', marker='o', linestyle='--', color='purple')

    # 设置标题和标签
    plt.title("Certificate Validity Period")
    plt.xlabel("Certificate Index")
    plt.ylabel("Date")

    # 设置日期格式
    date_format = "%Y-%m-%d"

    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(date_format))

    # 自动旋转日期标签，使其更美观
    plt.gcf().autofmt_xdate()

    # 添加网格线
    plt.grid(True, linestyle='--', alpha=0.7)

    # 设置 x 轴刻度为证书索引
    plt.xticks(certificate_indices)

    # 显示图例
    plt.legend()

    # 显示图表
    plt.tight_layout()
    plt.show()

    return valid_from_dates, valid_until_dates


# 设置你的根目录
root_folder = "./ca"

# 进行数据分析
all_data = analyze_tls_certificates(root_folder)
# 将数据转换为JSON格式
json_data = json.dumps(all_data, ensure_ascii=False, indent=2)  # indent参数用于格式化输出，使其更易读

# 将JSON数据写入文件
with open('tls_certificates_data.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
# analyze_country_and_organization(all_data)
# analyze_certificate_versions(all_data)
# analyze_certificate_validity_period(all_data)
# analyze_tls_version(all_data)
# analyze_subject(all_data)
# analyze_issuer(all_data)

# import os
# import json
# from collections import Counter
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from datetime import datetime
# import pandas as pd
#
#
# def analyze_tls_certificates(root_folder):
#     all_data = []
#
#     for province_folder in os.listdir(root_folder):
#         province_path = os.path.join(root_folder, province_folder)
#
#         if os.path.isdir(province_path):
#             for json_file in os.listdir(province_path):
#                 json_file_path = os.path.join(province_path, json_file)
#
#                 if os.path.isfile(json_file_path) and json_file.endswith(".json"):
#                     with open(json_file_path, 'r', encoding='utf-8') as f:
#                         json_data = json.load(f)
#                         all_data.append(json_data)
#
#     return all_data
#
#
# def analyze_country_and_organization(data):
#     print("Certificate Fields Analysis:")
#
#     collect = {'commonName': Counter(), 'organizationName': Counter(), 'countryName': Counter()}
#
#     for item in data:
#         cert_chains = item['cert_chain']
#         for cert in cert_chains:
#             subject = cert['subject']
#             issuer = cert['issuer']
#
#             # Extract values from subject and issuer
#             for field in ['commonName', 'organizationName', 'countryName']:
#                 if field in subject[0][0]:
#                     value = subject[0][0][1]
#                     collect[field][value] += 1
#
#                 if field in issuer[0][0]:
#                     value = issuer[0][0][1]
#                     collect[field][value] += 1
#
#     # Plot the results
#     for field, values in collect.items():
#         plt.figure(figsize=(10, 6))
#         plt.bar(values.keys(), values.values(), color='skyblue')
#         plt.title(f"{field.capitalize()} Distribution in Certificates")
#         plt.xlabel(f"{field.capitalize()} Value")
#         plt.ylabel("Count")
#         plt.show()
#
#
# def analyze_certificate_versions(data):
#     print("Certificate Versions Analysis:")
#     versions = [cert.get("version", "") for item in data for cert in item.get("cert_chain", [])]
#
#     # Plot certificate versions distribution
#     plt.bar(Counter(versions).keys(), Counter(versions).values(), color='lightgreen', edgecolor='black')
#     plt.title("Certificate Versions Distribution")
#     plt.xlabel("Certificate Version")
#     plt.ylabel("Count")
#     plt.show()
#
#
# def analyze_tls_version(data):
#     tls_versions = Counter(item.get("version", "") for item in data)
#
#     # Plot TLS versions distribution
#     plt.bar(tls_versions.keys(), tls_versions.values(), color='lightblue', edgecolor='black')
#     plt.title("TLS Versions Distribution")
#     plt.xlabel("TLS Version")
#     plt.ylabel("Count")
#     plt.show()
#     return tls_versions
#
#
# def analyze_issuer(data):
#     issuer = Counter(item.get("issuer", "") for item in data)
#
#     # Plot Issuer distribution
#     plt.bar(issuer.keys(), issuer.values(), color='lightblue', edgecolor='black')
#     plt.title("Issuer Distribution")
#     plt.xlabel("Issuer")
#     plt.ylabel("Count")
#     plt.show()
#     return issuer
#
#
# def analyze_subject(data):
#     subject = Counter(item.get("subject", "") for item in data)
#
#     # Plot Subject distribution
#     plt.bar(subject.keys(), subject.values(), color='lightblue', edgecolor='black')
#     plt.title("Subject Distribution")
#     plt.xlabel("Subject")
#     plt.ylabel("Count")
#     plt.show()
#     return subject
#
#
# def analyze_certificate_validity_period(data):
#     # Extract date information
#     valid_from_dates = [datetime.strptime(item.get("valid_from", ""), "%Y%m%d%H%M%SZ") for item in data]
#     valid_until_dates = [datetime.strptime(item.get("valid_until", ""), "%Y%m%d%H%M%SZ") for item in data]
#
#     # Generate certificate index list
#     certificate_indices = list(range(1, len(valid_from_dates) + 1))
#
#     # Sort by date in ascending order
#     valid_from_dates, valid_until_dates, certificate_indices = zip(
#         *sorted(zip(valid_from_dates, valid_until_dates, certificate_indices)))
#
#     # Plot certificate validity period time series
#     plt.figure(figsize=(12, 6))
#     plt.plot(certificate_indices, valid_from_dates, label='Valid From', marker='o', linestyle='-', color='orange')
#     plt.plot(certificate_indices, valid_until_dates, label='Valid Until', marker='o', linestyle='--', color='purple')
#
#     # Set title and labels
#     plt.title("Certificate Validity Period")
#     plt.xlabel("Certificate Index")
#     plt.ylabel("Date")
#
#     # Set date format
#     date_format = "%Y-%m-%d"
#
#     # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(date_format))
#
#     # Automatically rotate date labels for better readability
#     plt.gcf().autofmt_xdate()
#
#     # Add grid lines
#     plt.grid(True, linestyle='--', alpha=0.7)
#
#     # Set x-axis ticks to certificate indices
#     plt.xticks(certificate_indices)
#
#     # Show legend
#     plt.legend()
#
#     # Show the plot
#     plt.tight_layout()
#     plt.show()
#
#     return valid_from_dates, valid_until_dates
#
#
# def export_to_excel(data, file_path):
#     dfs = [pd.DataFrame({key: [value]}) for key, value in data.items()]
#     result_df = pd.concat(dfs, axis=1)
#     result_df.to_excel(file_path, index=False)
#     print(f"Data exported to {file_path}")
#
#
# # Set your root directory
# root_folder = "./ca"
#
# # Perform data analysis
# all_data = analyze_tls_certificates(root_folder)
# analyze_country_and_organization(all_data)
# analyze_certificate_versions(all_data)
# valid_from_dates, valid_until_dates = analyze_certificate_validity_period(all_data)
# tls_versions = analyze_tls_version(all_data)
# issuer_data = analyze_issuer(all_data)
# subject_data = analyze_subject(all_data)
#
# # Export data to Excel
# export_to_excel({
#     'Valid_From_Dates': valid_from_dates,
#     'Valid_Until_Dates': valid_until_dates,
#     'TLS_Versions': dict(tls_versions),
#     'Issuer_Data': dict(issuer_data),
#     'Subject_Data': dict(subject_data),
# }, 'certificate_analysis_data.xlsx')
