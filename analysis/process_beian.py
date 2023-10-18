import os
import json

# 文件夹路径
beian_directory = './beian'

# 存储解析后的数据的字典
province_data = {}


# 辅助函数：安全地将字符串转换为整数
def safe_int(value):
    try:
        return int(value)
    except ValueError:
        return None


# 遍历省份文件
for province_file in os.listdir(beian_directory):
    if province_file.endswith(".txt"):
        if province_file.startswith("不支持") or province_file.startswith("未进行"):
            continue
        province_name = province_file.split('.txt')[0]
        province_path = os.path.join(beian_directory, province_file)

        # 读取文件内容
        with open(province_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 解析文件内容
        data = {}
        for line in lines:
            key, value = map(str.strip, line.split(':'))
            # 将值转换为整数（如果可能）
            int_value = safe_int(value)

            # 更新字典
            data[key] = int_value

        # 将解析后的数据存储到字典中
        province_data[province_name] = data

# 将数据写入 JSON 文件
json_file_path = './beian_analyze/output.json'
os.makedirs('./beian_analyze', exist_ok=True)

with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(province_data, json_file, ensure_ascii=False, indent=2)

print(f"Data has been saved to {json_file_path}")
