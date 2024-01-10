# 中文地名及机构到英文的映射字典
import json

import pandas as pd
from matplotlib import pyplot as plt

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
data = []

with open("./dead_active_result.json", "r", encoding='utf-8') as file:
    data = json.load(file)

# Dictionaries to store counts by province for "dead" and "active"
dead_counts = {}
active_counts = {}

for unit in data:
    unit_name = unit['unit_name'].split('.txt')[0]

    # Use unit_name as the province name
    province = unit_name

    # Translate Chinese province name to English
    english_province = location_translation_dict.get(unit_name, unit_name)

    urls = unit["urls"]
    for url in urls:
        status = url["status"]

        # Update count based on status
        if status == 'dead':
            dead_counts[english_province] = dead_counts.get(english_province, 0) + 1
        elif status == 'active':
            active_counts[english_province] = active_counts.get(english_province, 0) + 1

# Create a DataFrame with counts for each province and status
df_counts = pd.DataFrame({'Province': list(dead_counts.keys()) + list(active_counts.keys()),
                          'Dead URLs': list(dead_counts.values()) + [0] * len(active_counts),
                          'Active URLs': [0] * len(dead_counts) + list(active_counts.values())})

# Group by province and calculate total URL count for each status
df_grouped = df_counts.groupby('Province').sum().reset_index()

# Calculate total URLs
df_grouped['Total URLs'] = df_grouped['Dead URLs'] + df_grouped['Active URLs']

# Sort the DataFrame by Total URLs in descending order
df_sorted = df_grouped.sort_values(by='Total URLs', ascending=False)

# Select the top 30 provinces
df_top30 = df_sorted.head(20)
# 在调整字体大小之前获取当前字体大小
current_fontsize = plt.rcParams['font.size']

# 设置新的字体大小
plt.rcParams['font.size'] = 15
# 设置SciPy风格
plt.style.use('_classic_test_patch')

# 画出堆叠条形图
ax = df_top30.plot(kind='bar', x='Province', y=['Dead URLs', 'Active URLs'], stacked=True, figsize=(12, 16))
ax.set_ylabel('Total URL Count')
ax.set_xlabel('Province')
ax.set_title('Top 20 Provinces by Total URLs (Dead and Active)')

# 旋转 x 轴标签
plt.xticks(rotation='vertical')

# 显示图例
plt.legend(["Dead URLs", "Active URLs"], loc='upper right')

# 自动调整图形布局
plt.tight_layout()

# 保存图像为PNG文件
plt.savefig('top30_provinces_by_total_urls_dead_active_stacked_sorted.png', bbox_inches='tight', dpi=500)

# 生成Excel表格
df_top30.to_excel('top30_provinces_by_total_urls_dead_active_stacked_sorted.xlsx', index=False)

# 显示图形
plt.show()
