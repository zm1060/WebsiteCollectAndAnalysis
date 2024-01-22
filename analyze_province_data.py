import json

import numpy as np
from matplotlib import pyplot as plt

# 中文地名及机构到英文的映射字典
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


with open('./province_data.json', 'r', encoding='utf-8') as f:
    province_data = json.load(f)

# 创建一个字典用于存储每个省的链接信息
province_links_data = {}



for data in province_data:
    province_name = data['province']
    province_sites = data['sites']

    # 初始化省的链接信息
    province_links_data[province_name] = {
        'internal_links_count': 0,
        'external_links_count': 0,
        'potential_threat_links_count': 0,
        'total_links_count': 0,
    }

    # 遍历每个站点，累加链接数量
    for site in province_sites:
        province_links_data[province_name]['internal_links_count'] += site['internal_links_count']
        province_links_data[province_name]['external_links_count'] += site['external_links_count']
        province_links_data[province_name]['potential_threat_links_count'] += site['potential_threat_links_count']
        province_links_data[province_name]['total_links_count'] += site['total_links_count']


#
# # 创建一个堆叠图
# fig, ax = plt.subplots(figsize=(10, 6), dpi=500)
#
# # 遍历每个省的链接信息
# for province, links_info in province_links_data.items():
#     # 将中文省份名替换为英文名
#     english_province_name = location_translation_dict.get(province, province)
#
#     # 获取链接信息
#     internal_links_count = links_info['internal_links_count']
#     external_links_count = links_info['external_links_count']
#     potential_threat_links_count = links_info['potential_threat_links_count']
#
#     # 绘制堆叠图
#     ax.bar(english_province_name, internal_links_count, label='Internal Links')
#     ax.bar(english_province_name, external_links_count, bottom=internal_links_count, label='External Links')
#     ax.bar(english_province_name, potential_threat_links_count, bottom=internal_links_count + external_links_count,
#            label='Potential Threat Links')
#
# # 设置图形标题和标签
# ax.set_title('Links Information by Province')
# ax.set_xlabel('Province')
# ax.set_ylabel('Links Count')
#
# # 添加图例
# ax.legend()
#
# # 显示图形
# plt.show()



# 创建一个堆叠图
fig, ax = plt.subplots(figsize=(10, 6), dpi=500)

# 定义颜色
# 第三种组合
internal_color = 'green'
external_color = 'lightblue'
potential_threat_color = 'orange'
# 遍历每个省的链接信息
for i, (province, links_info) in enumerate(province_links_data.items()):
    # 获取链接信息
    internal_links_count = links_info['internal_links_count']
    external_links_count = links_info['external_links_count']
    potential_threat_links_count = links_info['potential_threat_links_count']

    # 绘制堆叠图
    bottom = np.zeros_like(internal_links_count)  # 初始高度为0
    ax.bar(i, internal_links_count, color=internal_color, label='Internal Links', bottom=bottom)
    bottom += internal_links_count
    ax.bar(i, external_links_count, color=external_color, label='External Links', bottom=bottom)
    bottom += external_links_count
    ax.bar(i, potential_threat_links_count, color=potential_threat_color, label='Potential Threat Links', bottom=bottom)

    # 在堆叠图旁边显示省份名称
    ax.text(i, bottom.max(), location_translation_dict.get(province, province), ha='center', va='center', color='black', fontweight='bold', fontsize=8)

# 设置图形标题和标签
# ax.set_title('Links Information by Province')
ax.set_xlabel('Province')
ax.set_ylabel('Links Count')

# 将图例放到图外，并设置合适的位置和顺序
handles, labels = ax.get_legend_handles_labels()
order = [0, 1, 2]  # 按照Internal, External, Potential的顺序排列
ax.legend([handles[idx] for idx in order], [labels[idx] for idx in order], bbox_to_anchor=(1, 1))

# 设置x轴标签
ax.set_xticks(np.arange(len(province_links_data)))
ax.set_xticklabels(np.arange(1, len(province_links_data) + 1))  # 使用1-based编号

# 显示图形
plt.show()
