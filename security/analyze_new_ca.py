import json
import random

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import to_rgba
from wordcloud import WordCloud

# Load JSON data from file
with open('certificate_results_custom.json', 'r', encoding='utf-8') as file:
    certificates = json.load(file)
# Filter out certificates with empty issuer and subject
certificates = [cert for cert in certificates if cert.get('issuer') and cert.get('subject')]
# Convert to DataFrame
df = pd.DataFrame(certificates)
# Total number of certificates
total_certificates = len(df)
# Analyze different issuer counts
issuer_counts = df['issuer'].value_counts()
# Analyze certificate validity period distribution
df['notBefore'] = pd.to_datetime(df['notBefore'])
df['notAfter'] = pd.to_datetime(df['notAfter'])
df['validity_days'] = (df['notAfter'] - df['notBefore']).dt.days
# 获取'sans'列的长度统计
df['sans_count'] = df['sans'].apply(len)
# 打印'sans'列的长度统计信息
print("Statistics of 'sans' column:")
print(df['sans_count'].describe())

df['issuer_country'] = df['issuer'].apply(lambda x: x.get('countryName', 'Unknown'))
df['issuer_organization'] = df['issuer'].apply(lambda x: x.get('organizationName', 'Unknown'))
df['subject_organization'] = df['subject'].apply(lambda x: x.get('organizationName', 'Unknown'))
issuer_country_counts = df['issuer_country'].value_counts()
issuer_organization_counts = df['issuer_organization'].value_counts()
subject_organization_counts = df['subject_organization'].value_counts()
# English version of the data
english_subject_organization_counts = {
    'Unknown': 1902,
    'Guizhou Electronic Certification Technology': 371,
    'Henan Dahewan Digital Technology': 82,
    'Southern News Network': 76,
    'Nanning Big Data Development Bureau': 49,
    'Nanchang Municipal People\'s Government Office': 48,
    'Window of the Capital Operation Management Center': 47,
    'Anqing Data Resource Management Bureau': 45,
    'Chongqing Municipal People\'s Government Office': 44,
    'Wuxi Municipal People\'s Government Office': 44,
}
# Convert to DataFrame
df_subject_organization = pd.DataFrame(list(english_subject_organization_counts.items()),
                                       columns=['Organization', 'Count'])

print(df['sans_count'])
###################################################################################
#
# # Plot 1: Distribution of Certificate Validity Periods
# fig, ax1 = plt.subplots(figsize=(8, 6), dpi=500)
# sns.countplot(data=df, x='validity_days', color='lightcoral', ax=ax1)
# ax1.set_title('Certificate Validity Periods Distribution')
# ax1.set_xlabel('Validity Days')
# ax1.set_ylabel('Count')
# ax1.tick_params(axis='x', rotation=45)  # Rotate x-axis labels
# plt.show()

# Assuming df is your DataFrame with 'validity_days' column
df['validity_months'] = df['validity_days'] / 30.44  # average number of days in a month

# Define the custom color palette
custom_colors = ["#2878b5", "#9ac9db", "#f8ac8c", "#c82423", "#ff8884", "#8ECFC9", "#FFBE7A",
                 "#FA7F6F", "#82B0D2", "#BEB8DC", "#E7DAD2", "#F27970", "#BB9727", "#54B345",
                 "#32B897", "#05B9E2", "#8983BF", "#C76DA2", "#A1A9D0", "#F0988C", "#B883D4",
                 "#9E9E9E", "#CFEAF1", "#C4A5DE", "#F6CAE5", "#96CCCB"]

sns.set_palette(custom_colors)

# Plot histogram of 'validity_months' with multiple colors
plt.figure(figsize=(10, 6))
hist, bins, _ = plt.hist(df['validity_months'], bins=12, edgecolor='black', density=False)

# Iterate through bars and assign different colors
for i, patch in enumerate(plt.gca().patches):
    plt.setp(patch, 'facecolor', custom_colors[(i + 3) % len(custom_colors)])

plt.title('Certificate Validity Periods Distribution (Months)', fontsize=18)
plt.xlabel('Validity Months', fontsize=18)
plt.ylabel('Count', fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

# Adding specific value labels
total = len(df)
for i, count in enumerate(hist):
    percentage = count / total * 100
    plt.text(bins[i] + 0.5 * (bins[1] - bins[0]), count, f'{percentage:.2f}%', ha='center', va='bottom', fontsize=18)

plt.tight_layout()
plt.show()
#
# # 计算百分比
# total_count = issuer_country_counts.sum()
# percentage_values = (issuer_country_counts / total_count) * 100
#
# # 绘制柱状图
# fig, ax2 = plt.subplots(figsize=(8, 6), dpi=500)
# # 使用'mako'色图进行渐变效果
# sns.barplot(x=issuer_country_counts.index, y=percentage_values, palette='mako', ax=ax2)
# ax2.set_title('Top Issuer Countries')
# ax2.set_xlabel('Country')
# ax2.set_ylabel('Percentage (%)')
# ax2.tick_params(axis='x', rotation=0)
#
# # 在柱状图上显示百分比值
# for i, v in enumerate(percentage_values):
#     ax2.text(i, v + 0.5, f'{v:.2f}%', ha='center', va='bottom')
#
# plt.show()
#
# # 计算百分比
# total_count_org = issuer_organization_counts.sum()
# percentage_values_org = (issuer_organization_counts / total_count_org) * 100
#
# # 使用更加吸引人的颜色调色板，例如 'Set2'
# fig, ax3 = plt.subplots(figsize=(12, 10), dpi=500)
# sns.barplot(x=percentage_values_org.head(10), y=issuer_organization_counts.head(10).index, palette='Set2', ax=ax3)
#
# # 设置标题和坐标轴标签
# ax3.set_title('Top-10 Issuer Organizations', fontsize=16)
# ax3.set_xlabel('Percentage (%)', fontsize=14)
# ax3.set_ylabel('Organization', fontsize=14)
#
# # 调整y轴标签的旋转角度和字体大小，以提高可读性
# ax3.tick_params(axis='y', rotation=0, labelsize=12)
# ax3.tick_params(axis='x', labelsize=12)
#
#
# # 在每个柱形上显示具体的百分比值
# for i, v in enumerate(percentage_values_org.head(10)):
#     ax3.text(v + 0.5, i, f'{v:.2f}%', ha='left', va='center', fontsize=10, color='black')
#
# plt.tight_layout()
# plt.show()
###################################################################################
# No
# Plot 3: Top Issuer Organizations as a Pie Chart
# fig, ax3 = plt.subplots(figsize=(12, 10), dpi=500)
#
# # Calculate percentages
# total_count = issuer_organization_counts.head(10).sum()
# percentages = (issuer_organization_counts.head(10) / total_count) * 100
#
# # Plot as a pie chart
# ax3.pie(percentages, labels=issuer_organization_counts.head(10).index, autopct='%1.1f%%',
#         colors=sns.color_palette('pastel'), startangle=90)
# ax3.set_title('Top-10 Issuer Organizations')
# plt.show()
###################################################################################
# Yes
# Plot 4: Top Subject Organizations with a rich color palette
# fig, ax4 = plt.subplots(figsize=(12, 10), dpi=500)
#
# # Use a rich color palette for all bars
# sns.barplot(x='Organization', y='Count', data=df_subject_organization.head(10), palette='deep', ax=ax4)
#
# ax4.set_title('Top Subject Organizations')
# ax4.set_xlabel('Organization')
# ax4.set_ylabel('Count')
# ax4.tick_params(axis='x', rotation=90)  # Adjust rotation angle for better visibility
#
# plt.tight_layout()  # Ensure tight layout to prevent clipping
# plt.show()
print(issuer_organization_counts)
###################################################################################

# import squarify
#
# # Prepare the data
# companies = [
#     "DigiCert Inc",
#     "China Financial Certification Authority",
#     "Global Digital Cybersecurity Authority",
#     "Beijing Xinchacha Credit Management",
#     "WoTrus CA Limited",
#     "TrustAsia Technologies, Inc.",
#     "GlobalSign",
#     "sslTrus",
#     "Sectigo Limited",
#     "UniTrust"
# ]
# values = [1342, 1278, 1021, 930, 503, 408, 375, 259, 250, 218]
#
# # Create a tree map with improved label positioning
# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = 'Arial'
#
# fig, ax = plt.subplots(figsize=(16, 12))
# squarify.plot(sizes=values, label=companies, alpha=0.7, ax=ax, pad=True, text_kwargs={'fontsize': 15})
# plt.axis('off')
# plt.title('Company Values Tree Map', fontsize=25)
# plt.show()

#######################################################################
# Yes
import matplotlib.pyplot as plt
import squarify

# # 提供的数据
organizations = ["DigiCert Inc", "China Financial Certification Authority",
                 "Beijing Xinchacha Credit Management Co., Ltd.",
                 "Global Digital Cybersecurity Authority Co., Ltd.", "WoTrus CA Limited",
                 "TrustAsia Technologies, Inc.",
                 "GlobalSign nv-sa", "sslTrus", "Sectigo Limited", "UniTrust", "Let's Encrypt", "iTrusChina Co., Ltd.",
                 "CerSign Technology Limited", "Unizeto Technologies S.A.", "DNSPod, Inc.", "Xin Net Technology Corp."]
# # tree map
# counts = [2393, 1528, 1209, 1074, 575, 550, 392, 323, 283, 230, 99, 83, 48, 44, 44, 57]
#
# # 公司名缩写
# organizations_abbr = ["DigiCert", "CFCA", "Beijing Xinchacha Credit Management Co., Ltd.",
#                       "Global Digital Cybersecurity Authority Co., Ltd.", "WoTrus", "TrustAsia", "GlobalSign",
#                       "sslTrus", "Sectigo", "UniTrust",
#                       "Let's Encrypt", "iTrusChina", "CerSign", "Unizeto", "DNSPod", "Xin Net"]
#
# global_size = 30
# # 绘制 TreeMap
# plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': 'Arial'})
# fig, ax = plt.subplots(figsize=(16, 16))
#
# # 对所有公司应用通用设置
# squarify.plot(sizes=counts, label=organizations_abbr, alpha=0.7, text_kwargs={'fontsize': global_size})
#
# # 对特定公司调整文本位置
# special_companies = {"Beijing Xinchacha Credit Management Co., Ltd.": {'fontsize': global_size, 'va': 'bottom'},
#                      "Global Digital Cybersecurity Authority Co., Ltd.": {'fontsize': global_size, 'va': 'top'},
#                      "CerSign": {'fontsize': global_size, 'va': 'bottom'}, "iTrusChina": {'fontsize': global_size, 'va': 'top'}}
# for text in ax.texts:
#     company_name = text.get_text()
#     text_kwargs = {'fontsize': global_size, 'ha': 'center'}
#     if company_name in special_companies:
#         text_kwargs.update(special_companies[company_name])
#     text.set(**text_kwargs)
#
# plt.axis('off')
# plt.tight_layout()
# plt.show()
#
# # tree map
counts = [2393, 1528, 1209, 1074, 575, 550, 392, 323, 283, 230, 99, 83, 48, 44, 44, 57]
organizations_abbr = ["DigiCert", "CFCA", "Beijing Xinchacha",
                      "Global Digital", "WoTrus", "TrustAsia", "GlobalSign",
                      "sslTrus", "Sectigo", "UniTrust",
                      "Let's Encrypt", "iTrusChina", "CerSign", "Unizeto", "DNSPod", "Xin Net"]

# Shuffle the order of the companies and their corresponding counts
data = list(zip(counts, organizations_abbr))
random.shuffle(data)
counts, organizations_abbr = zip(*data)

global_size = 18  # Adjust the font size as needed

# Set up the figure with increased size
fig, ax = plt.subplots(figsize=(12, 12))

# Plot the regular pie chart without labels
wedges, _, autotexts = plt.pie(counts, autopct='%1.1f%%', textprops={'fontsize': global_size},
                                startangle=140)

# Set the font size for special companies in the legend
special_companies = {"Beijing Xinchacha Credit Management Co., Ltd.": {'fontsize': global_size, 'va': 'bottom'},
                     "Global Digital Cybersecurity Authority Co., Ltd.": {'fontsize': global_size, 'va': 'top'},
                     "CerSign": {'fontsize': global_size, 'va': 'bottom'}, "iTrusChina": {'fontsize': global_size, 'va': 'top'}}
for text in autotexts:
    company_name = text.get_text()
    text_kwargs = {'fontsize': global_size}
    if company_name in special_companies:
        text_kwargs.update(special_companies[company_name])
    text.set(**text_kwargs)

# Set the aspect ratio to be equal, making it a circle
ax.axis('equal')

# Create a legend with only company names and set the title font size
legend = plt.legend(organizations_abbr, title="Companies", loc="center left", bbox_to_anchor=(1, 0.5), prop={'size': global_size})
legend.get_title().set_fontsize(global_size)

# plt.title("Distribution of Companies", fontsize=global_size)
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import numpy as np

# 提供的数据
issuer_countries = ["CN", "US", "BE", "GB", "PL"]
counts = [5800, 2492, 392, 283, 44]

# 计算百分比
total_certificates = sum(counts)
percentages = [(count / total_certificates) * 100 for count in counts]

# 颜色映射
colors = plt.cm.viridis(np.linspace(0, 1, len(issuer_countries)))

# 绘制条形图
fig, ax = plt.subplots()
bars = ax.bar(issuer_countries, counts, color=colors)

# 在每个条形上方显示百分比
for bar, percentage in zip(bars, percentages):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 10, f'{percentage:.2f}%', ha='center', va='bottom', fontsize=8,
            color='black')

plt.xlabel('Issuer Country')
plt.ylabel('Count')
plt.savefig('certificate_country.png', dpi=500)

plt.show()

import matplotlib.pyplot as plt

# 提供的数据
tls_versions = ["TLSv1.2", "TLSv1.3", "TLSv1"]
counts = [5875, 3133, 3]

# 计算百分比
total_certificates = sum(counts)
percentages = [(count / total_certificates) * 100 for count in counts]

# 颜色映射
colors = plt.cm.viridis(np.linspace(0, 1, len(tls_versions)))

# 绘制条形图
fig, ax = plt.subplots()
bars = ax.bar(tls_versions, counts, color=colors)

# 在每个条形上方显示百分比
for bar, percentage in zip(bars, percentages):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 10, f'{percentage:.2f}%', ha='center', va='bottom', fontsize=18,
            color='black')

plt.xlabel('TLS Version', fontsize=18)
plt.ylabel('Count', fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.tight_layout()
plt.savefig('certificate_tls_version.png', dpi=500)

plt.show()
