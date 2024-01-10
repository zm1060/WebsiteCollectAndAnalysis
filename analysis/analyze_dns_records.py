import json
import os
from collections import Counter

# 存储所有统计信息的列表
all_domain_stats = []

# 统计每个记录类型的总数量
total_records_count = Counter()

# 统计每个域名中NS记录数量的分布
ns_records_distribution = Counter()

# 统计每个域名中CNAME记录数量的分布
cname_records_distribution = Counter()

# 统计每个域名中A记录数量的分布
a_records_distribution = Counter()

# 统计每个域名中AAAA记录数量的分布
aaaa_records_distribution = Counter()

# 统计每个域名中DS记录数量的分布
ds_records_distribution = Counter()

# 统计每个域名中NSEC记录数量的分布
nsec_records_distribution = Counter()

# 统计每个域名中NSEC3记录数量的分布
nsec3_records_distribution = Counter()

# 统计每个域名中RRSIG记录数量的分布
rrsig_records_distribution = Counter()

# 统计每个域名中SOA记录数量的分布
soa_records_distribution = Counter()

for filename in os.listdir('./dns_records'):
    file_path = f'./dns_records/{filename}'

    try:
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 统计每个域名的NS、CNAME、A和AAAA记录数量
        domain_records_count = {"NS": {}, "CNAME": {}, "A": {}, "AAAA": {}, "DS": {}, "NSEC": {}, "NSEC3": {}, "RRSIG": {}, "SOA": {}}

        for entry in data:
            if entry is not None:
                try:
                    # 获取记录的URL
                    url = entry['url']

                    # 检查是否存在'records'键
                    if 'records' in entry:
                        ns_count = 0  # 记录每个域名的NS记录数量
                        cname_count = 0
                        a_count = 0
                        aaaa_count = 0
                        soa_count = 0
                        nsec_count = 0
                        nsec3_count = 0
                        rrsig_count = 0
                        ds_count = 0
                        for record in entry['records']:
                            record_type = record['Type']

                            # 处理 CNAME 记录
                            if record_type == 'CNAME':
                                cname_count += 1
                                domain_records_count['CNAME'].setdefault(url, 0)
                                domain_records_count['CNAME'][url] = cname_count
                            elif record_type == 'NS':
                                ns_count += 1
                                domain_records_count['NS'].setdefault(url, 0)
                                domain_records_count['NS'][url] = ns_count
                            elif record_type == 'A':
                                a_count += 1
                                domain_records_count['A'].setdefault(url, 0)
                                domain_records_count['A'][url] = a_count
                            elif record_type == 'AAAA':
                                aaaa_count += 1
                                domain_records_count['AAAA'].setdefault(url, 0)
                                domain_records_count['AAAA'][url] = aaaa_count
                            elif record_type == 'SOA':
                                soa_count += 1
                                domain_records_count['SOA'].setdefault(url, 0)
                                domain_records_count['SOA'][url] = soa_count
                            elif record_type == 'NSEC':
                                nsec_count += 1
                                domain_records_count['NSEC'].setdefault(url, 0)
                                domain_records_count['NSEC'][url] = nsec_count
                            elif record_type == 'NSEC3':
                                nsec3_count += 1
                                domain_records_count['NSEC3'].setdefault(url, 0)
                                domain_records_count['NSEC3'][url] = nsec3_count
                            elif record_type == 'RRSIG':
                                rrsig_count += 1
                                domain_records_count['RRSIG'].setdefault(url, 0)
                                domain_records_count['RRSIG'][url] = rrsig_count
                            elif record_type == 'DS':
                                ds_count += 1
                                domain_records_count['DS'].setdefault(url, 0)
                                domain_records_count['DS'][url] = ds_count
                            else:
                                domain_records_count[record_type].setdefault(url, 0)
                                domain_records_count[record_type][url] += 1

                                # 累加总记录数量
                                total_records_count[record_type] += 1

                    else:
                        print(f"No 'records' found for {url} in {file_path}")
                except KeyError as e:
                    print(f"Error processing entry in {file_path}: {e}")
            else:
                print(f"Found a None entry in {file_path}")

        # 统计每个记录类型下每个URL中记录的数量分布
        records_distribution = {}
        for record_type in domain_records_count:
            record_distribution = Counter()

            for url, count in domain_records_count[record_type].items():
                record_distribution[count] += 1

            records_distribution[record_type] = dict(record_distribution)

        # 存储统计信息
        domain_stats = {"Name": filename.split('.json')[0], **records_distribution}
        all_domain_stats.append(domain_stats)

        # 更新NS记录数量的分布统计
        ns_records_distribution.update(domain_records_count['NS'].values())

        # 更新CNAME记录数量的分布统计
        cname_records_distribution.update(domain_records_count['CNAME'].values())

        # 更新A记录数量的分布统计
        a_records_distribution.update(domain_records_count['A'].values())

        # 更新AAAA记录数量的分布统计
        aaaa_records_distribution.update(domain_records_count['AAAA'].values())

        # 更新DS记录数量的分布统计
        ds_records_distribution.update(domain_records_count['DS'].values())

        # 更新NSEC记录数量的分布统计
        nsec_records_distribution.update(domain_records_count['NSEC'].values())

        # 更新NSEC3记录数量的分布统计
        nsec3_records_distribution.update(domain_records_count['NSEC3'].values())

        # 更新RRSIG记录数量的分布统计
        rrsig_records_distribution.update(domain_records_count['RRSIG'].values())

        # 更新SOA记录数量的分布统计
        soa_records_distribution.update(domain_records_count['SOA'].values())
        # 打印结果
        for record_type, counts in domain_records_count.items():
            for url, count in counts.items():
                print(f"Domain: {url}, {record_type} Records Count: {count}")

        print(f"\nRecords Distribution for {filename}: {records_distribution}")

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading file {file_path}: {e}")

# 打印总记录数量统计
print("\nTotal Records Count:")
for record_type, count in total_records_count.items():
    print(f"{record_type}: {count}")

# 打印NS记录数量的分布统计
print("\nNS Records Distribution:")
for ns_count, count in ns_records_distribution.items():
    print(f"NS Count: {ns_count}, Domains Count: {count}")

# 打印CNAME记录数量的分布统计
print("\nCNAME Records Distribution:")
for cname_count, count in cname_records_distribution.items():
    print(f"CNAME Count: {cname_count}, Domains Count: {count}")

# 打印A记录数量的分布统计
print("\nA Records Distribution:")
for a_count, count in a_records_distribution.items():
    print(f"A Count: {a_count}, Domains Count: {count}")

# 打印AAAA记录数量的分布统计
print("\nAAAA Records Distribution:")
for aaaa_count, count in aaaa_records_distribution.items():
    print(f"AAAA Count: {aaaa_count}, Domains Count: {count}")


# Initialize total counts
total_ns_records = 0
total_cname_records = 0
total_a_records = 0
total_aaaa_records = 0

# Calculate total counts
for ns_count, count in ns_records_distribution.items():
    total_ns_records +=  count

for cname_count, count in cname_records_distribution.items():
    total_cname_records +=  count

for a_count, count in a_records_distribution.items():
    total_a_records += count

for aaaa_count, count in aaaa_records_distribution.items():
    total_aaaa_records += count

# Print total counts
print("\nTotal NS Records:", total_ns_records)
print("Total CNAME Records:", total_cname_records)
print("Total A Records:", total_a_records)
print("Total AAAA Records:", total_aaaa_records)

# # 打印NSEC记录数量的分布统计
# print("\nNSEC Records Distribution:")
# for nsec_count, count in nsec_records_distribution.items():
#     print(f"NSEC Count: {nsec_count}, Domains Count: {count}")
#
# # 打印NSEC3记录数量的分布统计
# print("\nNSEC3 Records Distribution:")
# for nsec3_count, count in nsec3_records_distribution.items():
#     print(f"NSEC3 Count: {nsec3_count}, Domains Count: {count}")
#
# # 打印DS记录数量的分布统计
# print("\nDS Records Distribution:")
# for ds_count, count in ds_records_distribution.items():
#     print(f"DS Count: {ds_count}, Domains Count: {count}")
#
# # 打印SOA记录数量的分布统计
# print("\nSOA Records Distribution:")
# for soa_count, count in soa_records_distribution.items():
#     print(f"SOA Count: {soa_count}, Domains Count: {count}")
#
# # 打印RRSIG记录数量的分布统计
# print("\nRRSIG Records Distribution:")
# for rrsig_count, count in rrsig_records_distribution.items():
#     print(f"RRSIG Count: {rrsig_count}, Domains Count: {count}")


# 将所有统计信息保存为JSON文件
output_file_path = './dns_records_stats.json'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(all_domain_stats, output_file, ensure_ascii=False, indent=2)

print(f"\nStatistics saved to {output_file_path}")
import matplotlib.pyplot as plt
import seaborn as sns

# Replace the placeholders with your actual data
ns_data = [(2, 1839), (4, 192), (6, 35), (1, 76), (3, 90), (8, 1), (5, 1)]
cname_data = [(1, 3528), (2, 1007), (5, 1), (3, 144), (4, 7)]
a_data = [(7, 5496), (9, 96), (2, 1621), (1, 3650), (4, 265), (6, 480), (16, 33), (18, 4), (8, 517), (17, 335),
          (14, 7), (19, 44), (5, 155), (13, 255), (3, 571), (21, 78), (12, 4), (25, 30), (11, 30), (57, 1),
          (10, 2), (22, 1), (23, 32), (24, 1)]
aaaa_data = [(5, 5884), (2, 1116), (13, 4), (1, 246), (7, 102), (6, 3), (8, 4), (10, 27), (4, 76)]


# Set seaborn style with white background
sns.set_style("white")

# Set figure size and resolution
plt.figure(figsize=(14, 10), dpi=500)

# Define colors
colors = sns.color_palette("pastel")

# Plot NS records distribution
plt.subplot(2, 2, 1)
ax1 = sns.barplot(x=[item[0] for item in ns_data], y=[item[1]/sum([i[1] for i in ns_data]) * 100 for item in ns_data], color=colors[0])
plt.xlabel('Number of NS Records', fontsize=14)
plt.ylabel('Percentage of Domains', fontsize=14)
plt.title('Distribution of NS Records in Domains', fontsize=16)

# Add total count label
# ax1.text(0.5, -0.15, f'Total Domains: 2234', ha='center', va='center', transform=ax1.transAxes, fontsize=12)

# Add percentage labels on top of each bar
# for p in ax1.patches:
#     ax1.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
#                 ha='center', va='center', fontsize=10, color='black', xytext=(0, 10),
#                 textcoords='offset points')

# Plot CNAME records distribution
plt.subplot(2, 2, 2)
ax2 = sns.barplot(x=[item[0] for item in cname_data], y=[item[1]/sum([i[1] for i in cname_data]) * 100 for item in cname_data], color=colors[1])
plt.xlabel('Number of CNAME Records', fontsize=14)
plt.ylabel('Percentage of Domains', fontsize=14)
plt.title('Distribution of CNAME Records in Domains', fontsize=16)

# Add total count label
# ax2.text(0.5, -0.15, f'Total Domains: 4687', ha='center', va='center', transform=ax2.transAxes, fontsize=12)

# Add percentage labels on top of each bar
# for p in ax2.patches:
#     ax2.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
#                 ha='center', va='center', fontsize=10, color='black', xytext=(0, 10),
#                 textcoords='offset points')

# Plot A records distribution
plt.subplot(2, 2, 3)
ax3 = sns.barplot(x=[item[0] for item in a_data], y=[item[1]/sum([i[1] for i in a_data]) * 100 for item in a_data], color=colors[2])
plt.xlabel('Number of A Records', fontsize=14)
plt.ylabel('Percentage of Domains', fontsize=14)
plt.title('Distribution of A Records in Domains', fontsize=16)

# Add total count label
# ax3.text(0.5, -0.15, f'Total Domains: 13708', ha='center', va='center', transform=ax3.transAxes, fontsize=12)

# # Add percentage labels on top of each bar
# for p in ax3.patches:
#     ax3.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
#                 ha='center', va='center', fontsize=10, color='black', xytext=(0, 10),
#                 textcoords='offset points')

# Plot AAAA records distribution
plt.subplot(2, 2, 4)
ax4 = sns.barplot(x=[item[0] for item in aaaa_data], y=[item[1]/sum([i[1] for i in aaaa_data]) * 100 for item in aaaa_data], color=colors[3])
# ax4 = sns.barplot(x=[item[0] for item in aaaa_data], y=[item[1]/sum([i[1] for i in aaaa_data]) * 100 for item in aaaa_data], color=colors[3])
plt.xlabel('Number of AAAA Records', fontsize=14)
plt.ylabel('Percentage of Domains', fontsize=14)
plt.title('Distribution of AAAA Records in Domains', fontsize=16)

# Add total count label
# ax4.text(0.5, -0.15, f'Total Domains: 7462', ha='center', va='center', transform=ax4.transAxes, fontsize=12)

# # Add percentage labels on top of each bar
# for p in ax4.patches:
#     ax4.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
#                 ha='center', va='center', fontsize=10, color='black', xytext=(0, 10),
#                 textcoords='offset points')

# Adjust layout
plt.tight_layout()

# Save the plot as a high-resolution image
plt.savefig('records_distribution_percentage.png', dpi=500)

# Show the plot
plt.show()

# # Set seaborn style with white background
#
# sns.set_style("white")
#
# # Set figure size and resolution
# plt.figure(figsize=(14, 10), dpi=500)
#
# # Define colors
# colors = sns.color_palette("pastel")
#
# # Plot NS records distribution
# plt.subplot(2, 2, 1)
# sns.barplot(x=[item[0] for item in ns_data], y=[item[1]/sum([i[1] for i in ns_data]) * 100 for item in ns_data], color=colors[0])
# plt.xlabel('Number of NS Records', fontsize=14)
# plt.ylabel('Percentage of Domains', fontsize=14)
# plt.title('Distribution of NS Records in Domains', fontsize=16)
#
# # Plot CNAME records distribution
# plt.subplot(2, 2, 2)
# sns.barplot(x=[item[0] for item in cname_data], y=[item[1]/sum([i[1] for i in cname_data]) * 100 for item in cname_data], color=colors[1])
# plt.xlabel('Number of CNAME Records', fontsize=14)
# plt.ylabel('Percentage of Domains', fontsize=14)
# plt.title('Distribution of CNAME Records in Domains', fontsize=16)
#
# # Plot A records distribution
# plt.subplot(2, 2, 3)
# sns.barplot(x=[item[0] for item in a_data], y=[item[1]/sum([i[1] for i in a_data]) * 100 for item in a_data], color=colors[2])
# plt.xlabel('Number of A Records', fontsize=14)
# plt.ylabel('Percentage of Domains', fontsize=14)
# plt.title('Distribution of A Records in Domains', fontsize=16)
#
# # Plot AAAA records distribution
# plt.subplot(2, 2, 4)
# sns.barplot(x=[item[0] for item in aaaa_data], y=[item[1]/sum([i[1] for i in aaaa_data]) * 100 for item in aaaa_data], color=colors[3])
# plt.xlabel('Number of AAAA Records', fontsize=14)
# plt.ylabel('Percentage of Domains', fontsize=14)
# plt.title('Distribution of AAAA Records in Domains', fontsize=16)
#
# # Adjust layout
# plt.tight_layout()
#
# # Save the plot as a high-resolution image
# plt.savefig('records_distribution_percentage.png', dpi=500)
#
# # Show the plot
# plt.show()

# 柱状图 显示百分比
# # Set seaborn style with white background
# sns.set_style("white")
#
# # Set figure size and resolution
# plt.figure(figsize=(14, 10), dpi=500)
#
# # Define colors
# colors = sns.color_palette("pastel")
#
# # Plot NS records distribution
# plt.subplot(2, 2, 1)
# ax1 = sns.barplot(x=[item[0] for item in ns_data], y=[item[1]/sum([i[1] for i in ns_data]) * 100 for item in ns_data], color=colors[0])
# plt.xlabel('Number of NS Records', fontsize=14)
# plt.ylabel('Percentage of Domains', fontsize=14)
# plt.title('Distribution of NS Records in Domains', fontsize=16)
#
# # Add percentage labels on top of each bar
# for p in ax1.patches:
#     ax1.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
#                 ha='center', va='center', fontsize=10, color='black', xytext=(0, 10),
#                 textcoords='offset points')
#
# # Plot CNAME records distribution
# plt.subplot(2, 2, 2)
# ax2 = sns.barplot(x=[item[0] for item in cname_data], y=[item[1]/sum([i[1] for i in cname_data]) * 100 for item in cname_data], color=colors[1])
# plt.xlabel('Number of CNAME Records', fontsize=14)
# plt.ylabel('Percentage of Domains', fontsize=14)
# plt.title('Distribution of CNAME Records in Domains', fontsize=16)
#
# # Add percentage labels on top of each bar
# for p in ax2.patches:
#     ax2.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
#                 ha='center', va='center', fontsize=10, color='black', xytext=(0, 10),
#                 textcoords='offset points')
#
# # Plot A records distribution
# plt.subplot(2, 2, 3)
# ax3 = sns.barplot(x=[item[0] for item in a_data], y=[item[1]/sum([i[1] for i in a_data]) * 100 for item in a_data], color=colors[2])
# plt.xlabel('Number of A Records', fontsize=14)
# plt.ylabel('Percentage of Domains', fontsize=14)
# plt.title('Distribution of A Records in Domains', fontsize=16)
#
# # Add percentage labels on top of each bar
# for p in ax3.patches:
#     ax3.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
#                 ha='center', va='center', fontsize=10, color='black', xytext=(0, 10),
#                 textcoords='offset points')
#
# # Plot AAAA records distribution
# plt.subplot(2, 2, 4)
# ax4 = sns.barplot(x=[item[0] for item in aaaa_data], y=[item[1]/sum([i[1] for i in aaaa_data]) * 100 for item in aaaa_data], color=colors[3])
# plt.xlabel('Number of AAAA Records', fontsize=14)
# plt.ylabel('Percentage of Domains', fontsize=14)
# plt.title('Distribution of AAAA Records in Domains', fontsize=16)
#
# # Add percentage labels on top of each bar
# for p in ax4.patches:
#     ax4.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
#                 ha='center', va='center', fontsize=10, color='black', xytext=(0, 10),
#                 textcoords='offset points')
#
# # Adjust layout
# plt.tight_layout()
#
# # Save the plot as a high-resolution image
# plt.savefig('records_distribution_percentage.png', dpi=500)
#
# # Show the plot
# plt.show()
