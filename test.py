import matplotlib.pyplot as plt
import numpy as np

# 数据
labels_population = ['城镇人口', '乡村人口']
sizes_population = [66.2, 33.8]

labels_employment = ['城镇就业人员', '乡村就业人员']
sizes_employment = [63.5, 36.5]

income_labels = ['城镇人均收入', '乡村人均收入']
income_values = [51821, 21691]

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']

# 高级图1：人口分布
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    sizes_population, labels=labels_population, autopct='%1.1f%%', startangle=90,
    colors=['#4CAF50', '#FFC107'], textprops=dict(color="w"), explode=[0.1, 0]
)
ax.set_title('中国城乡人口分布（2023年）', fontsize=16, weight='bold')
plt.setp(autotexts, size=12, weight='bold')
plt.show()

# 高级图2：就业分布
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    sizes_employment, labels=labels_employment, autopct='%1.1f%%', startangle=90,
    colors=['#2196F3', '#FF5722'], textprops=dict(color="w"), explode=[0.1, 0]
)
ax.set_title('中国城乡就业分布（2023年）', fontsize=16, weight='bold')
plt.setp(autotexts, size=12, weight='bold')
plt.show()

# 高级图3：城乡人均收入比较
x = np.arange(len(income_labels))
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(x, income_values, color=['#673AB7', '#FF9800'], alpha=0.85)
ax.set_title('中国城乡人均收入比较（2023年）', fontsize=16, weight='bold')
ax.set_ylabel('人均收入（元）', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(income_labels, fontsize=12)
ax.bar_label(bars, fmt='%.0f', padding=3, fontsize=10, weight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
