import json
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 中英文地名映射字典
location_translation_dict = {
    "上海市": "Shanghai",
    "重庆市": "Chongqing",
    "陕西省": "Shaanxi",
    "青海省": "Qinghai",
    "黑龙江省": "Heilongjiang",
    "云南省": "Yunnan",
    "北京市": "Beijing",
    "吉林省": "Jilin",
    "四川省": "Sichuan",
    "天津市": "Tianjin",
    "宁夏回族自治区": "Ningxia",
    "内蒙古自治区": "Inner Mongolia",
    "安徽省": "Anhui",
    "山东省": "Shandong",
    "山西省": "Shanxi",
    "广东省": "Guangdong",
    "江苏省": "Jiangsu",
    "江西省": "Jiangxi",
    "河北省": "Hebei",
    "河南省": "Henan",
    "浙江省": "Zhejiang",
    "海南省": "Hainan",
    "湖北省": "Hubei",
    "湖南省": "Hunan",
    "甘肃省": "Gansu",
    "福建省": "Fujian",
    "贵州省": "Guizhou",
    "辽宁省": "Liaoning",
    "广西壮族自治区": "Guangxi",
    "新疆生产建设兵团": "Xinjiang Production and Construction Corps",
    "新疆维吾尔自治区": "Xinjiang Uygur Autonomous Region",
    "省级门户": "Provincial Government Portal",
    "部委门户": "Government Department Portal",
    "国务院部门所属网站": "State Council",
    "西藏自治区": "Tibet",
}

# 结果数据初始化
province_data = []
overall_active_count = 0
overall_dead_count = 0
overall_total_count = 0
overall_elapsed_times = []

# 遍历结果文件夹
for filename in os.listdir('new_webpage_result'):
    province = filename.split('_')[0]
    if filename.endswith('.json'):
        with open('./new_webpage_result/' + filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 提取省级数据
        province_active_url_count = data['active_url_count']
        province_dead_url_count = data['dead_url_count']
        province_total_url_count = data['total_url_count']

        overall_active_count += province_active_url_count
        overall_dead_count += province_dead_url_count
        overall_total_count += province_total_url_count

        # 提取域名数据
        domain_data = data['domains']
        province_elapsed_times = [domain['response_info'].get('elapsed_time', 0.0) for domain in domain_data
                                  if domain['status'] == 'active' and 'response_info' in domain]
        overall_elapsed_times.extend(province_elapsed_times)

        # 存储省级数据
        province_data.append({
            'province': location_translation_dict.get(province,'Unknown'),
            'active_url_count': province_active_url_count,
            'dead_url_count': province_dead_url_count,
            'total_url_count': province_total_url_count,
            'elapsed_times': province_elapsed_times
        })

provinces = [entry['province'] for entry in province_data]
active_counts = [entry['active_url_count'] for entry in province_data]
dead_counts = [entry['dead_url_count'] for entry in province_data]
total_counts = [entry['total_url_count'] for entry in province_data]


fig, ax = plt.subplots(figsize=(10, 6), dpi=500)
bar_width = 0.8

# 绘制 Active URLs
bar1 = ax.bar(range(len(provinces)), active_counts, width=bar_width, label='Active URLs', align='center')

# 绘制 Dead URLs，使用 active_counts 作为底部
bar2 = ax.bar(range(len(provinces)), dead_counts, width=bar_width, label='Dead URLs',
              bottom=active_counts, align='center')


ax.set_xlabel('Province Index')
ax.set_ylabel('URL Counts')
ax.set_xticks(range(len(provinces)))
ax.set_xticklabels(range(1, len(provinces) + 1))  # 使用数字编号
ax.legend()

# 在每个柱状图上方显示英文省名
for i, province in enumerate(provinces):
    y_offset = 10 if i not in [13, 23] else 30  # Adjust the offset for specific cases
    ax.text(i, sum([active_counts[i], dead_counts[i]]) + y_offset, province,
            ha='center', va='bottom')


plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Specify bin edges
bins = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

# Generate gradient colors
colors = np.linspace(0, 1, len(bins)-1)
hist_colors = plt.cm.viridis(colors)

# Create histogram with adjusted bar width and spacing
fig, ax = plt.subplots(figsize=(10, 6), dpi=500)
n, bins, patches = ax.hist(overall_elapsed_times, bins=bins, edgecolor='black', alpha=0.5, rwidth=1.0)

# Set color and labels for each bar
for count, (patch, color) in zip(n, zip(patches, hist_colors)):
    patch.set_facecolor(color)
    height = patch.get_height()
    percentage = count / len(overall_elapsed_times)
    ax.text(patch.get_x() + patch.get_width() / 2, height, f'{percentage:.2%}', ha='center', va='bottom')

ax.set_xlabel('Elapsed Time (s)')
ax.set_ylabel('Frequency')

# Set x-axis labels with bin edges
ax.set_xticks(bins)
plt.tight_layout()
plt.show()


from statistics import mean

# 计算每个省份的elapsed_times平均值
for entry in province_data:
    elapsed_times = entry['elapsed_times']
    entry['average_elapsed_time'] = round(mean(elapsed_times), 4) if elapsed_times else 0

# 创建DataFrame
df = pd.DataFrame(province_data)

# 写入Excel文件
df.to_excel('url_counts_by_province.xlsx', index=False)
