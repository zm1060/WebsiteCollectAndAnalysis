import json
import os
from collections import Counter
from urllib.parse import urlparse

from matplotlib import pyplot as plt

# Initialize dictionaries to store counts
a_records_counts = {}
aaaa_records_counts = {}
cname_records_counts = {}
ns_records_counts = {}
has_cname_no_a_count = 0
has_aaaa_no_a_count = 0
has_cname_no_aaaa_count = 0
has_a_no_aaaa_count = 0
has_cname_no_ns_count = 0
for filename in os.listdir('./dns_records'):
    file_path = f'./dns_records/{filename}'

    try:
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for entry in data:
                if entry is not None:
                    try:
                        # 获取记录的URL
                        url = entry.get('url', '')  # Use get method to handle missing 'url'

                        if 'records' in entry:
                            # Initialize counts for each domain
                            a_records_count = 0
                            aaaa_records_count = 0
                            cname_records_count = 0
                            ns_records_count = 0

                            for record in entry['records']:
                                if 'Type' in record:
                                    record_type = record['Type']
                                    record_name = record['Name']
                                    if url in record_name and (record_type == 'A' or record_type == 'AAAA'):
                                        if record_type == 'A':
                                            a_records_count += 1
                                        elif record_type == 'AAAA':
                                            aaaa_records_count += 1
                                        continue
                                    # Count different record types
                                    if record_type == 'CNAME':
                                        cname_records_count += 1
                                    elif record_type == 'NS':
                                        ns_records_count += 1

                            # Update counts in dictionaries
                            a_records_counts.setdefault(a_records_count, 0)
                            a_records_counts[a_records_count] += 1

                            aaaa_records_counts.setdefault(aaaa_records_count, 0)
                            aaaa_records_counts[aaaa_records_count] += 1

                            cname_records_counts.setdefault(cname_records_count, 0)
                            cname_records_counts[cname_records_count] += 1

                            ns_records_counts.setdefault(ns_records_count, 0)
                            ns_records_counts[ns_records_count] += 1

                            if a_records_count == 0 and cname_records_count != 0:
                                has_cname_no_a_count += 1
                            if a_records_count == 0 and aaaa_records_count != 0:
                                has_aaaa_no_a_count += 1
                            if aaaa_records_count == 0 and cname_records_count != 0:
                                has_cname_no_aaaa_count += 1
                            if a_records_count == 0 and aaaa_records_count != 0:
                                has_a_no_aaaa_count += 1
                            if ns_records_count == 0:
                                if cname_records_count != 0:
                                    has_cname_no_ns_count += 1
                                    print(url)
                    except KeyError as e:
                        print(f"Error processing entry: {e}")

            # 打印结果 (Print results outside the loop for each file)
            print(f"Domain: {url}, A Records Count: {a_records_count}")
            print(f"Domain: {url}, AAAA Records Count: {aaaa_records_count}")
            print(f"Domain: {url}, CNAME Records Count: {cname_records_count}")
            print(f"Domain: {url}, NS Records Count: {ns_records_count}")

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading file {file_path}: {e}")

# Print distributions for all files
print("\nDistribution of A Records Counts:")
for count, frequency in a_records_counts.items():
    print(f"Count: {count}, Frequency: {frequency}")

print("\nDistribution of AAAA Records Counts:")
for count, frequency in aaaa_records_counts.items():
    print(f"Count: {count}, Frequency: {frequency}")

print("\nDistribution of CNAME Records Counts:")
for count, frequency in cname_records_counts.items():
    print(f"Count: {count}, Frequency: {frequency}")

print("\nDistribution of NS Records Counts:")
for count, frequency in ns_records_counts.items():
    print(f"Count: {count}, Frequency: {frequency}")

import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# Set Seaborn style
sns.set(style="white")


def autolabel(rects, percentages):
    for rect, percentage in zip(rects, percentages):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, f'{percentage:.2f}%', ha='center', va='bottom',
                 fontsize=16)


def plot_distribution(title, records_counts, total_domains, dpi=500):
    counts, frequencies = zip(*sorted(records_counts.items()))

    # Calculate percentages
    percentages = [freq / total_domains * 100 for freq in frequencies]

    # Create a figure with specified DPI
    plt.figure(dpi=dpi, figsize=(12, 8))

    # Use a different color palette (e.g., 'viridis')
    bars = sns.barplot(x=counts, y=frequencies, palette='viridis')

    plt.xlabel('Count', fontsize=16)
    plt.ylabel('Frequency', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    # plt.title(title, fontsize=16)

    # 在绘制条形图后调用autolabel函数，传递percentages
    autolabel(bars.patches, percentages)

    # 调整整体的字体大小
    plt.rcParams.update({'font.size': 16})
    plt.savefig(title, dpi=500)
    plt.show()


# Calculate total domains
total_domains_a = sum(a_records_counts.values())
total_domains_aaaa = sum(aaaa_records_counts.values())
total_domains_cname = sum(cname_records_counts.values())
total_domains_ns = sum(ns_records_counts.values())

# Plot distributions with percentages on bars and set DPI to 500 without legend
# plot_distribution('Distribution_of_A', a_records_counts, total_domains_a, dpi=500)
# plot_distribution('Distribution_of_AAAA', aaaa_records_counts, total_domains_aaaa, dpi=500)
# plot_distribution('Distribution_of_CNAME', cname_records_counts, total_domains_cname, dpi=500)
plot_distribution('Distribution_of_NS', ns_records_counts, total_domains_ns, dpi=500)
