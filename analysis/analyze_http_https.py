# import os
# import json
# import matplotlib.pyplot as plt
#
# # Specify the directory path where your JSON files are located
# directory_path = './http_https'
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
# plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题
#
# # Initialize lists to store data from all files
# total_links_data = []
# invalid_links_data = []
# internal_links_data = []
# external_links_data = []
# http_links_data = []
# https_links_data = []
#
# # Iterate through the files in the directory
# for filename in os.listdir(directory_path):
#     if filename.endswith('.json'):
#         file_path = os.path.join(directory_path, filename)
#         unit_name = filename.split('.json')[0]
#         # Read the JSON file
#         with open(file_path, 'r', encoding='utf-8') as file:
#             data = json.load(file)
#
#         # Access the data from the JSON object
#         total_links = data['total_links']
#         invalid_links = data['invalid_links']
#         internal_links = data['internal_links']
#         external_links = data['external_links']
#         http_links = data['http_links']
#         https_links = data['https_links']
#
#         # Append data to the lists for the total figure
#         total_links_data.append(total_links)
#         invalid_links_data.append(invalid_links)
#         internal_links_data.append(internal_links)
#         external_links_data.append(external_links)
#         http_links_data.append(http_links)
#         https_links_data.append(https_links)
#
#         # Plot figures for each file
#         plt.figure(figsize=(10, 6))
#
#         # Bar chart for link counts
#         plt.subplot(2, 2, 1)
#         categories = ['Total Links', 'Invalid Links', 'Internal Links', 'External Links']
#         values = [total_links, invalid_links, internal_links, external_links]
#         plt.bar(categories, values)
#         plt.title(f'Link Analysis for {unit_name}')
#         plt.xlabel('Categories')
#         plt.ylabel('Number of Links')
#
#         # Pie chart for invalid link ratio
#         plt.subplot(2, 2, 2)
#         labels = ['Valid Links', 'Invalid Links']
#         sizes = [total_links - invalid_links, invalid_links]
#         explode = (0, 0.1)
#         plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
#         plt.title(f'Invalid Link Ratio for {unit_name}')
#
#         # Bar chart for HTTP and HTTPS links
#         plt.subplot(2, 2, 3)
#         categories = ['HTTP Links', 'HTTPS Links']
#         values = [http_links, https_links]
#         plt.bar(categories, values)
#         plt.title(f'HTTP vs HTTPS Links for {unit_name}')
#         plt.xlabel('Link Types')
#         plt.ylabel('Number of Links')
#
#         # Show all subplots
#         plt.tight_layout()
#
#         # Save the figure with the corresponding filename
#         save_filename = f'{unit_name}.png'
#         os.makedirs(f'{directory_path}/figure', exist_ok=True)
#         save_path = f'{directory_path}/figure/{save_filename}'
#         plt.savefig(save_path)
#
#
# # Plot a total figure combining all the data
# plt.figure()
# categories = ['Total Links', 'Invalid Links', 'Internal Links', 'External Links']
# values = [sum(total_links_data), sum(invalid_links_data), sum(internal_links_data), sum(external_links_data)]
# plt.bar(categories, values)
# plt.title('Total Link Analysis')
# plt.xlabel('Categories')
# plt.ylabel('Number of Links')
# os.makedirs(f'{directory_path}/figure', exist_ok=True)
# # Save the total figure
# total_save_filename = 'total_figure.png'
# total_save_path = f'{directory_path}/figure/{total_save_filename}'
# plt.savefig(total_save_path)
#
# plt.show()


##########################################################

import os
import json
import matplotlib.pyplot as plt
import numpy as np

# Specify the directory path where your JSON files are located
directory_path = './http_https'
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# Initialize lists to store data from all files
province_data = []

# Iterate through the files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        file_path = os.path.join(directory_path, filename)
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Access the data from the JSON object
        province = data['province']
        total_links = data['total_links']
        valid_links = total_links - data['invalid_links']
        invalid_links = data['invalid_links']
        internal_links = data['internal_links']
        external_links = data['external_links']

        # Append data to the list for the total figure
        province_data.append({
            'province': province,
            'total_links': total_links,
            'valid_links': valid_links,
            'invalid_links': invalid_links,
            'internal_links': internal_links,
            'external_links': external_links
        })

# Sort the data by total links in descending order
province_data.sort(key=lambda x: x['total_links'], reverse=True)

# Extract data for plotting
provinces = [entry['province'] for entry in province_data]
total_links = [entry['total_links'] for entry in province_data]
valid_links = [entry['valid_links'] for entry in province_data]
invalid_links = [entry['invalid_links'] for entry in province_data]
internal_links = [entry['internal_links'] for entry in province_data]
external_links = [entry['external_links'] for entry in province_data]

# Plotting
fig, ax = plt.subplots(figsize=(30, 8))

# Bar chart for total, valid, and invalid links
bar_width = 0.4
index = np.arange(len(provinces))
bar1 = ax.bar(index, total_links, bar_width, label='Total Links')
bar2 = ax.bar(index, valid_links, bar_width, label='Valid Links', bottom=invalid_links)

ax.set_xlabel('Province')
ax.set_ylabel('Number of Links')
ax.set_title('Link Analysis by Province')
ax.set_xticks(index)
ax.set_xticklabels(provinces, rotation=45, ha='right')
ax.legend()

# Stacked bar chart for internal and external links
fig, ax = plt.subplots(figsize=(30, 8))

bar_width = 0.8
bottom_bar = np.zeros(len(provinces))

bar3 = ax.bar(index, internal_links, bar_width, label='Internal Links', bottom=bottom_bar)
bottom_bar += internal_links

bar4 = ax.bar(index, external_links, bar_width, label='External Links', bottom=bottom_bar)

ax.set_xlabel('Province')
ax.set_ylabel('Number of Links')
ax.set_title('Internal vs External Links by Province')
ax.set_xticks(index)
ax.set_xticklabels(provinces, rotation=45, ha='right')
ax.legend()

plt.tight_layout()
plt.show()

