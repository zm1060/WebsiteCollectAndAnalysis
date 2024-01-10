import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# Plot 1: Distribution of Certificate Validity Periods
fig, ax1 = plt.subplots(figsize=(8, 6), dpi=500)
sns.countplot(data=df, x='validity_days', color='lightcoral', ax=ax1)
ax1.set_title('Certificate Validity Periods Distribution')
ax1.set_xlabel('Validity Days')
ax1.set_ylabel('Count')
ax1.tick_params(axis='x', rotation=45)  # Rotate x-axis labels
plt.show()

# 计算百分比
total_count = issuer_country_counts.sum()
percentage_values = (issuer_country_counts / total_count) * 100

# 绘制柱状图
fig, ax2 = plt.subplots(figsize=(8, 6), dpi=500)
# 使用'mako'色图进行渐变效果
sns.barplot(x=issuer_country_counts.index, y=percentage_values, palette='mako', ax=ax2)
ax2.set_title('Top Issuer Countries')
ax2.set_xlabel('Country')
ax2.set_ylabel('Percentage (%)')
ax2.tick_params(axis='x', rotation=0)

# 在柱状图上显示百分比值
for i, v in enumerate(percentage_values):
    ax2.text(i, v + 0.5, f'{v:.2f}%', ha='center', va='bottom')

plt.show()

# 计算百分比
total_count_org = issuer_organization_counts.sum()
percentage_values_org = (issuer_organization_counts / total_count_org) * 100

# 使用更加吸引人的颜色调色板，例如 'Set2'
fig, ax3 = plt.subplots(figsize=(12, 10), dpi=500)
sns.barplot(x=percentage_values_org.head(10), y=issuer_organization_counts.head(10).index, palette='Set2', ax=ax3)

# 设置标题和坐标轴标签
ax3.set_title('Top-10 Issuer Organizations', fontsize=16)
ax3.set_xlabel('Percentage (%)', fontsize=14)
ax3.set_ylabel('Organization', fontsize=14)

# 调整y轴标签的旋转角度和字体大小，以提高可读性
ax3.tick_params(axis='y', rotation=0, labelsize=12)
ax3.tick_params(axis='x', labelsize=12)


# 在每个柱形上显示具体的百分比值
for i, v in enumerate(percentage_values_org.head(10)):
    ax3.text(v + 0.5, i, f'{v:.2f}%', ha='left', va='center', fontsize=10, color='black')

plt.tight_layout()
plt.show()


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

# Plot 4: Top Subject Organizations with a rich color palette
fig, ax4 = plt.subplots(figsize=(12, 10), dpi=500)

# Use a rich color palette for all bars
sns.barplot(x='Organization', y='Count', data=df_subject_organization.head(10), palette='deep', ax=ax4)

ax4.set_title('Top Subject Organizations')
ax4.set_xlabel('Organization')
ax4.set_ylabel('Count')
ax4.tick_params(axis='x', rotation=90)  # Adjust rotation angle for better visibility

plt.tight_layout()  # Ensure tight layout to prevent clipping
plt.show()


print(issuer_organization_counts)

import squarify

# Prepare the data
companies = [
    "DigiCert Inc",
    "China Financial Certification Authority",
    "Global Digital Cybersecurity Authority",
    "Beijing Xinchacha Credit Management",
    "WoTrus CA Limited",
    "TrustAsia Technologies, Inc.",
    "GlobalSign",
    "sslTrus",
    "Sectigo Limited",
    "UniTrust"
]
values = [1342, 1278, 1021, 930, 503, 408, 375, 259, 250, 218]

# Create a tree map with improved label positioning
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Arial'

fig, ax = plt.subplots(figsize=(16, 12))
squarify.plot(sizes=values, label=companies, alpha=0.7, ax=ax, pad=True, text_kwargs={'fontsize': 15})
plt.axis('off')
plt.title('Company Values Tree Map', fontsize=25)
plt.show()