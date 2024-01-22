import json
import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

count_tls_version = {}
count_issuer_country = {}
count_issuer_organization = {}
count_not_before_after = {}

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

# 将统计结果转换为DataFrame
df_tls_version = pd.DataFrame(list(count_tls_version.items()), columns=['TLS_Version', 'Count'])
df_issuer_country = pd.DataFrame(list(count_issuer_country.items()), columns=['Issuer_Country', 'Count'])
df_issuer_organization = pd.DataFrame(list(count_issuer_organization.items()), columns=['Issuer_Organization', 'Count'])
df_not_before_after = pd.DataFrame(list(count_not_before_after.items()), columns=['NotBefore_NotAfter', 'Count'])



# Your TLS version count dictionary
count_tls_version = {'TLSv1.2': 5875, 'TLSv1.3': 3133, 'TLSv1.1': 3}

# Convert the dictionary to a DataFrame
df_tls_version = pd.DataFrame(list(count_tls_version.items()), columns=['TLS_Version', 'Count'])

# Set SCI style
sns.set_style("white")
sns.set_context("paper")

# Plotting the count of TLS versions
plt.figure(figsize=(10, 6), dpi=500)
tls_plot = sns.barplot(x='TLS_Version', y='Count', data=df_tls_version, palette="viridis")

# Adding labels and title
plt.xlabel('TLS Version', size=16)
plt.ylabel('Count', size=16)
# Customize font size for x-axis and y-axis tick labels
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
# Display percentage on top of each bar
total = 3133 + 3 + 5875
for p in tls_plot.patches:
    height = p.get_height()
    tls_plot.text(p.get_x() + p.get_width() / 2., height + 0.1,
                  '{:.2%}'.format(height/total),
                  ha="center", va="bottom", fontsize=16)

plt.tight_layout()
# Show the plot
plt.show()
# 将DataFrame写入Excel文件
# with pd.ExcelWriter('statistics.xlsx', engine='xlsxwriter') as writer:
#     df_tls_version.to_excel(writer, sheet_name='TLS_Version', index=False)
#     df_issuer_country.to_excel(writer, sheet_name='Issuer_Country', index=False)
#     df_issuer_organization.to_excel(writer, sheet_name='Issuer_Organization', index=False)
#     df_not_before_after.to_excel(writer, sheet_name='NotBefore_NotAfter', index=False)
