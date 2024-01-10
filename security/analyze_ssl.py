import os
import json


def preprocess_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()

    # Replace single quotes with double quotes
    data = data.replace("'", "\"")

    # Replace boolean values
    data = data.replace("True", "true").replace("False", "false")

    # Save the modified data back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)


def get_all_ssl(root_folder):
    all_data = []
    grade_count = {}
    for province_folder in os.listdir(root_folder):
        province_path = os.path.join(root_folder, province_folder)

        if os.path.isdir(province_path):
            for json_file in os.listdir(province_path):
                json_file_path = os.path.join(province_path, json_file)

                if os.path.isfile(json_file_path) and json_file.endswith(".txt"):
                    try:
                        # Preprocess the JSON file before loading
                        preprocess_json_file(json_file_path)

                        with open(json_file_path, 'r', encoding='utf-8') as f:
                            json_data = json.load(f)
                            endpoints_data = json_data['endpoints']
                            for endpoint_data in endpoints_data:
                                # print(endpoint_data)
                                grade = endpoint_data.get('grade', '')
                                grade_count[grade] = grade_count.get(grade, 0) + 1
                                break
                            all_data.append(json_data)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in file {json_file_path}: {e}")

    return all_data, grade_count


# 设置你的根目录
root_folder = "./ssl"

# 进行数据分析
all_data, grade_count = get_all_ssl(root_folder)
print(grade_count)
'''
{
    'host': 'credit.fgw.sh.gov.cn', 
    'port': 443, 
    'protocol': 'http', 
    'isPublic': False, 
    'status': 'IN_PROGRESS', 
    'startTime': 1699060195992, 
    'engineVersion': '2.2.0', 
    'criteriaVersion': '2009q', 
    'endpoints': 
        [
            {
                'ipAddress': '2409:8c1e:8f60:3000:0:0:b7c2:f37f', 
                'statusMessage': 'Ready', 
                'grade': 'A', 
                'gradeTrustIgnored': 'A', 
                'hasWarnings': False, 
                'isExceptional': False, 
                'progress': 100, 
                'duration': 162702, 
                'eta': 7, 
                'delegation': 1
            }, 
            {
                'ipAddress': '183.194.243.127', 
                'serverName': '', 
                'statusMessage': 'In progress', 
                'statusDetails': 'TESTING_PROTO_2_0', 
                'statusDetailsMessage': 'Testing SSL 2.0', 
                'progress': -1, 
                'eta': -1, 
                'delegation': 1
            }
        ]
}

{'A': 711, 'A+': 135, 'B': 3619, 'T': 1843, 'F': 439, '': 5899, 'C': 210, 'A-': 1}

'''