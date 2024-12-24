import datetime
import json
import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

count_tls_version = {}
count_issuer_country = {}
count_issuer_organization = {}
count_not_before_after = {}

import fnmatch


def check_certificate_host_match(cert_info, host):
    subject_common_name = cert_info.get("Subject_CommonName", "")
    if subject_common_name:
        if fnmatch.fnmatch(host, subject_common_name):
            return "Certificate subject matches the host."
        else:
            return f"Certificate subject does not match the host. Expected: {subject_common_name}, Actual: {host}"
    else:
        return "Subject common name not found in certificate."


def check_host_match_with_cert(cert_info, host):
    # 检查是否存在"Certificate_Info"键
    if "Certificate_Info" not in cert_info:
        return "Certificate information not found."

    # 提取证书信息
    certificate_info = cert_info["Certificate_Info"]

    # 获取Subject_CommonName和SubjectAltName
    subject_common_name = certificate_info.get("Subject_CommonName", "")
    subject_alt_name = certificate_info.get("SubjectAltName", "")

    # 检查主机名是否与Subject_CommonName匹配
    if subject_common_name and host_matches(subject_common_name, host):
        return True
    # 检查主机名是否与SubjectAltName匹配
    elif subject_alt_name and host_matches(subject_alt_name, host):
        return True
    else:
        return False


def host_matches(pattern, host):
    return fnmatch.fnmatch(host, pattern)


# 示例用法
cert_info = {
    "TLS_Version": "TLSv1.3",
    "Certificate_Info": {
        "Subject_CommonName": "*.sc.gov.cn",
        "SubjectAltName": "*.sc.gov.cn"
    },
    "Cipher": [
        "TLS_AES_256_GCM_SHA384",
        "TLSv1.3",
        256
    ],
    "Host": "sc.119.gov.cn"
}
# match_result = check_host_match_with_cert(cert_info, cert_info["Host"])
# print(match_result)
# 将字符串格式的时间转换为 datetime 对象
def parse_time(time_str):
    return datetime.datetime.strptime(time_str, "%b %d %H:%M:%S %Y %Z")

# 定义要比较的日期
expiration_date = datetime.datetime(2023, 12, 31)

# 统计失效时间在指定日期之前的证书数量
expired_cert_count = 0
mismatch_count = 0

for filename in os.listdir('result'):
    if filename.endswith(".json"):
        province_name = filename.split("_")[0]
        with open(os.path.join('result', filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
        records = data.get(province_name, [])  # Use get method to handle missing keys
        for record in records:
            tls_version = record.get('TLS_Version')
            issuer_country = record.get('Certificate_Info', {}).get('Issuer_Country')
            issuer_organization = record.get('Certificate_Info', {}).get('Issuer_Organization')
            not_before = record.get('Certificate_Info', {}).get('NotBefore')
            not_after = record.get('Certificate_Info', {}).get('NotAfter')
            host = record.get("Host")
            if not_after:
                expiration_time = parse_time(not_after)
                if expiration_time < expiration_date:
                    expired_cert_count += 1
            if host:
                result = check_host_match_with_cert(record, host)
                if not result:
                    mismatch_count += 1
            if tls_version:
                count_tls_version.setdefault(tls_version, 0)
                count_tls_version[tls_version] += 1
            else:
                print(f"Warning: TLS_Version not found in record for {province_name}")

            if issuer_country:
                count_issuer_country.setdefault(issuer_country, 0)
                count_issuer_country[issuer_country] += 1
            else:
                print(f"Warning: Issuer_Country not found in record for {province_name}")

            if issuer_organization:
                count_issuer_organization.setdefault(issuer_organization, 0)
                count_issuer_organization[issuer_organization] += 1
            else:
                print(f"Warning: Issuer_Organization not found in record for {province_name}")

            if not_before and not_after:
                period = f"{not_before} to {not_after}"
                count_not_before_after.setdefault(period, 0)
                count_not_before_after[period] += 1
            else:
                print(f"Warning: NotBefore or NotAfter not found in record for {province_name}")

print(f"Total mismatch count: {mismatch_count}")
print(f"Total expired cert count: {expired_cert_count}")

# # 将统计结果转换为DataFrame
# df_tls_version = pd.DataFrame(list(count_tls_version.items()), columns=['TLS_Version', 'Count'])
# df_issuer_country = pd.DataFrame(list(count_issuer_country.items()), columns=['Issuer_Country', 'Count'])
# df_issuer_organization = pd.DataFrame(list(count_issuer_organization.items()), columns=['Issuer_Organization', 'Count'])
# df_not_before_after = pd.DataFrame(list(count_not_before_after.items()), columns=['NotBefore_NotAfter', 'Count'])
#
#
#
# # Your TLS version count dictionary
# count_tls_version = {'TLSv1.2': 5875, 'TLSv1.3': 3133, 'TLSv1.1': 3}
#
# # Convert the dictionary to a DataFrame
# df_tls_version = pd.DataFrame(list(count_tls_version.items()), columns=['TLS_Version', 'Count'])
#
# # Set SCI style
# sns.set_style("white")
# sns.set_context("paper")
#
# # Plotting the count of TLS versions
# plt.figure(figsize=(10, 6), dpi=500)
# tls_plot = sns.barplot(x='TLS_Version', y='Count', data=df_tls_version, palette="viridis")
#
# # Adding labels and title
# plt.xlabel('TLS Version', size=16)
# plt.ylabel('Count', size=16)
# # Customize font size for x-axis and y-axis tick labels
# plt.xticks(fontsize=16)
# plt.yticks(fontsize=16)
# # Display percentage on top of each bar
# total = 3133 + 3 + 5875
# for p in tls_plot.patches:
#     height = p.get_height()
#     tls_plot.text(p.get_x() + p.get_width() / 2., height + 0.1,
#                   '{:.2%}'.format(height/total),
#                   ha="center", va="bottom", fontsize=16)
#
# plt.tight_layout()
# # Show the plot
# plt.show()
# 将DataFrame写入Excel文件
# with pd.ExcelWriter('statistics.xlsx', engine='xlsxwriter') as writer:
#     df_tls_version.to_excel(writer, sheet_name='TLS_Version', index=False)
#     df_issuer_country.to_excel(writer, sheet_name='Issuer_Country', index=False)
#     df_issuer_organization.to_excel(writer, sheet_name='Issuer_Organization', index=False)
#     df_not_before_after.to_excel(writer, sheet_name='NotBefore_NotAfter', index=False)
