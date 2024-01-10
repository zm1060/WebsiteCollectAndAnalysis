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

# 中文地名及机构到英文的映射字典
location_translation_dict = {
    "上海市": "Shanghai",
    "重庆市": "Chongqing",
    "陕西省": "Shaanxi Province",
    "青海省": "Qinghai Province",
    "黑龙江省": "Heilongjiang Province",
    "云南省": "Yunnan Province",
    "中医药管理局": "State Administration of Traditional Chinese Medicine",
    "中科院": "Chinese Academy of Sciences",
    "乡村振兴局": "Rural Revitalization Bureau",
    "北京市": "Beijing",
    "吉林省": "Jilin Province",
    "四川省": "Sichuan Province",
    "天津市": "Tianjin",
    "宁夏回族自治区": "Ningxia Hui Autonomous Region",
    "内蒙古自治区": "Inner Mongolia Autonomous Region",
    "安徽省": "Anhui Province",
    "山东省": "Shandong Province",
    "山西省": "Shanxi Province",
    "广东省": "Guangdong Province",
    "江苏省": "Jiangsu Province",
    "江西省": "Jiangxi Province",
    "河北省": "Hebei Province",
    "河南省": "Henan Province",
    "浙江省": "Zhejiang Province",
    "海南省": "Hainan Province",
    "湖北省": "Hubei Province",
    "湖南省": "Hunan Province",
    "甘肃省": "Gansu Province",
    "福建省": "Fujian Province",
    "贵州省": "Guizhou Province",
    "辽宁省": "Liaoning Province",
    "广西壮族自治区": "Guangxi Zhuang Autonomous Region",
    "新疆生产建设兵团": "Xinjiang Production and Construction Corps",
    "新疆维吾尔自治区": "Xinjiang Uygur Autonomous Region",
    "省级门户": "Provincial Government Portal",
    "部委门户": "Government Department Portal",
    "国务院部门所属网站": "Websites of State Council Departments",
    "交通运输部": "Ministry of Transport",
    "人力资源社会保障部": "Ministry of Human Resources and Social Security",
    "人民银行": "People's Bank of China",
    "住房城乡建设部": "Ministry of Housing and Urban-Rural Development",
    "体育总局": "General Administration of Sport",
    "信访局": "State Bureau for Letters and Calls",
    "公安部": "Ministry of Public Security",
    "农业农村部": "Ministry of Agriculture and Rural Affairs",
    "医保局": "Healthcare Security Administration",
    "卫生健康委": "National Health Commission",
    "参事室": "General Office of the State Council",
    "发展改革委": "National Development and Reform Commission",
    "发展研究中心": "Development Research Center of the State Council",
    "司法部": "Ministry of Justice",
    "商务部": "Ministry of Commerce",
    "国家民委": "State Ethnic Affairs Commission",
    "国管局": "State-owned Assets Supervision and Administration Commission",
    "国资委": "State-owned Assets Supervision and Administration Commission",
    "国防科工局": "State Administration of Science, Technology and Industry for National Defense",
    "国际发展合作署": "China International Development Cooperation Agency",
    "地震局": "China Earthquake Administration",
    "外交部": "Ministry of Foreign Affairs",
    "外汇局": "State Administration of Foreign Exchange",
    "安全部": "Ministry of Public Security",
    "审计署": "National Audit Office",
    "工业和信息化部": "Ministry of Industry and Information Technology",
    "工程院": "Chinese Academy of Engineering",
    "市场监管总局": "State Administration for Market Regulation",
    "广电总局": "National Radio and Television Administration",
    "应急管理部": "Ministry of Emergency Management",
    "教育部": "Ministry of Education",
    "文化和旅游部": "Ministry of Culture and Tourism",
    "文物局": "State Administration of Cultural Heritage",
    "林草局": "State Forestry and Grassland Administration",
    "民政部": "Ministry of Civil Affairs",
    "民航局": "Civil Aviation Administration of China",
    "气象局": "China Meteorological Administration",
    "水利部": "Ministry of Water Resources",
    "海关总署": "General Administration of Customs",
    "港澳办": "Hong Kong and Macau Affairs Office",
    "烟草局": "State Tobacco Monopoly Administration",
    "生态环境部": "Ministry of Ecology and Environment",
    "知识产权局": "State Intellectual Property Office",
    "矿山安监局": "State Administration of Work Safety",
    "社科院": "Chinese Academy of Social Sciences",
    "科技部": "Ministry of Science and Technology",
    "移民局": "National Immigration Administration",
    "税务总局": "State Taxation Administration",
    "粮食和物资储备局": "State Administration of Grain and Material Reserves",
    "统计局": "National Bureau of Statistics",
    "能源局": "National Energy Administration",
    "自然基金会": "National Natural Science Foundation of China",
    "自然资源部": "Ministry of Natural Resources",
    "药监局": "National Medical Products Administration",
    "西藏自治区": "Tibet Autonomous Region",
    "证监会": "China Securities Regulatory Commission",
    "财政部": "Ministry of Finance",
    "退役军人事务部": "Ministry of Veterans Affairs",
    "邮政局": "State Post Bureau",
    "铁路局": "China Railway Corporation",
    "银保监会": "China Banking and Insurance Regulatory Commission",
}


def translate_province_name(chinese_name):
    return location_translation_dict.get(chinese_name, chinese_name)


# Specify the directory path where your JSON files are located
directory_path = './http_https'
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# Initialize lists to store data from all files
province_data = []

# Iterate through the files in the directory
# Iterate through the files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        file_path = os.path.join(directory_path, filename)
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Access the data from the JSON object
        province = translate_province_name(data['province'])
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

# Plotting total, valid, and invalid links for the first 32 provinces
fig, ax = plt.subplots(figsize=(15, 8), dpi=500)

bar_width = 0.4
index = np.arange(20)  # Adjusted to display only the first 32 provinces

bar1 = ax.bar(index, total_links[:20], bar_width, label='Total Links')
bar2 = ax.bar(index, valid_links[:20], bar_width, label='Valid Links', bottom=invalid_links[:32])

ax.set_xlabel('Province')
ax.set_ylabel('Number of Links')
ax.set_title('Total Links Status by Province')
ax.set_xticks(index)
ax.set_xticklabels(provinces[:20], rotation=45, ha='right')  # Adjusted to display only the first 32 provinces
ax.legend()
plt.tight_layout()
plt.savefig('total_links_plot_top-20.png')
plt.show()

# Plotting internal vs external links for the first 32 provinces
fig, ax = plt.subplots(figsize=(15, 8), dpi=500)

bar_width = 0.4
bottom_bar = np.zeros(20)  # Adjusted to display only the first 32 provinces

bar3 = ax.bar(index, internal_links[:20], bar_width, label='Internal Links', bottom=bottom_bar)
bottom_bar += internal_links[:20]

bar4 = ax.bar(index, external_links[:20], bar_width, label='External Links', bottom=bottom_bar)

ax.set_xlabel('Province')
ax.set_ylabel('Number of Links')
ax.set_title('Internal vs External Links by Province')
ax.set_xticks(index)
ax.set_xticklabels(provinces[:20], rotation=45, ha='right')  # Adjusted to display only the first 32 provinces
ax.legend()
plt.tight_layout()
plt.savefig('internal_external_links_plot_top-20.png')
plt.show()
