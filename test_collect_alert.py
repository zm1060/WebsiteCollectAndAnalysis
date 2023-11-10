# 从文件中加载JSON报告
import json

with open('Guizhou.json', 'r', encoding='utf-8') as report_file:
    zap_report = json.load(report_file)

json_data = zap_report

# 创建一个字典来存储不同的alert值和它们的出现次数
alert_counts = {}

# 遍历站点信息并统计alert字段的值
for site_data in json_data["site"]:
    for alert_data in site_data.get("alerts", []):
        alert_value = alert_data.get("alert", "")

        # 如果alert值已经在字典中，增加计数，否则将其添加到字典中
        if alert_value in alert_counts:
            alert_counts[alert_value] += 1
        else:
            alert_counts[alert_value] = 1

# 打印不同alert值的出现次数
for alert, count in alert_counts.items():
    print(f"Alert: {alert}, Count: {count}")
