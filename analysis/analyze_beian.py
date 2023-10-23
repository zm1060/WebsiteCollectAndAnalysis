import json

import matplotlib.pyplot as plt
import numpy as np

data = json.load(open('./beian_analyze/output.json', 'r', encoding='utf-8'))

# 中文到英文的映射字典
translation_dict = {
    "总数": "Total",
    "ICP备案": "ICP filing",
    "公安备案": "Police filing",
    "无障碍": "Accessibility",
    "SRI支持": "SRI support",
    "CSP支持": "CSP support",
}

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


# 将中文键转换为英文
data_english = {location_translation_dict.get(key, key): {translation_dict.get(sub_key, sub_key): sub_value for sub_key, sub_value in value.items()} for key, value in data.items()}

# 存储到新的JSON文件
with open('./beian_analyze/new_output.json', 'w', encoding='utf-8') as f:
    json.dump(data_english, f, ensure_ascii=False, indent=2)
#
# categories = list(data_english.keys())
# total_values = [entry["Total"] for entry in data_english.values()]
# icp_values = [entry["ICP filing"] for entry in data_english.values()]
# police_values = [entry["Police filing"] for entry in data_english.values()]
# accessibility_values = [entry["Accessibility"] for entry in data_english.values()]
# sri_values = [entry["SRI support"] for entry in data_english.values()]
# csp_values = [entry["CSP support"] for entry in data_english.values()]
#
# plt.style.use('ggplot')
#
# # Bar chart
# fig, ax = plt.subplots(figsize=(10, 6))
# bar_width = 0.15
# index = np.arange(len(categories))
# bar1 = ax.bar(index, total_values, bar_width, label='Total')
# bar2 = ax.bar(index + bar_width, icp_values, bar_width, label='ICP filing')
# bar3 = ax.bar(index + 2 * bar_width, police_values, bar_width, label='Police filing')
# bar4 = ax.bar(index + 3 * bar_width, accessibility_values, bar_width, label='Accessibility')
# bar5 = ax.bar(index + 4 * bar_width, sri_values, bar_width, label='SRI support')
# bar6 = ax.bar(index + 5 * bar_width, csp_values, bar_width, label='CSP support')
#
# ax.set_xlabel('Region/Organization')
# ax.set_ylabel('Count')
# ax.set_title('Statistics for Different Regions/Organizations')
# ax.set_xticks(index + 3 * bar_width / 2)
# ax.set_xticklabels(categories)
# ax.legend()
#
# plt.tight_layout()
# plt.show()
#
# # Line chart
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.plot(categories, total_values, marker='o', label='Total')
# ax.plot(categories, icp_values, marker='o', label='ICP filing')
# ax.plot(categories, police_values, marker='o', label='Police filing')
# ax.plot(categories, accessibility_values, marker='o', label='Accessibility')
# ax.plot(categories, sri_values, marker='o', label='SRI support')
# ax.plot(categories, csp_values, marker='o', label='CSP support')
#
# ax.set_xlabel('Region/Organization')
# ax.set_ylabel('Count')
# ax.set_title('Statistics for Different Regions/Organizations')
# ax.legend()
#
# plt.tight_layout()
# plt.show()
#
# # Pie chart
# fig, ax = plt.subplots(figsize=(8, 8))
# ax.pie(total_values, labels=categories, autopct='%1.1f%%', startangle=90)
#
# ax.set_title('Proportion of Total Count for Different Regions/Organizations')
#
# plt.show()
