import os
import json


def process_cdn_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 过滤掉不需要的行
    filtered_lines = [line for line in lines if not line.startswith(('服务器:', 'Address:'))]

    # 组织成JSON格式
    data = []
    current_entry = None

    iterator = iter(filtered_lines)

    for line in iterator:
        if line.startswith('名称:'):
            if current_entry:
                data.append(current_entry)
            current_entry = {'Name': line.split(':')[1].strip(), 'Addresses': [], 'Aliases': []}
        elif line.startswith('Addresses:'):
            # Extract addresses from the current line and subsequent lines
            addresses = []
            while line.startswith('Addresses:') or not line.strip():
                address_part = line.split('Addresses:')[1].strip()
                addresses.extend(addr.strip() for addr in address_part.split())
                try:
                    line = next(iterator)
                except StopIteration:
                    break
            # Continue extracting addresses from subsequent lines until a line without leading whitespace or end of file
            while line.strip() and not line.startswith(('服务器:', 'Address:', 'Aliases:')):
                addresses.extend(addr.strip() for addr in line.split())
                try:
                    line = next(iterator)
                except StopIteration:
                    break
            current_entry['Addresses'].extend(addresses)
        elif line.startswith('Aliases:'):
            # Extract aliases from the current line and subsequent lines
            aliases = []
            while line.startswith('Aliases:') or not line.strip():
                aliases.extend(alias.strip() for alias in line.split()[1:])
                try:
                    line = next(iterator)
                except StopIteration:
                    break
            current_entry['Aliases'].extend(aliases)

    if current_entry:
        data.append(current_entry)

    return data


def process_directory(cdn_directory, output_directory):
    for filename in os.listdir(cdn_directory):
        file_path = os.path.join(cdn_directory, filename)
        file_path = os.path.join(file_path, 'ip_cdn_info.txt')
        province_name = filename

        cdn_data = process_cdn_file(file_path)

        output_file_path = os.path.join(output_directory, f'{province_name}.json')

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(cdn_data, output_file, indent=2)

        print(f'处理完成，结果已保存到 {output_file_path}')


if __name__ == '__main__':
    cdn_directory = './cdn'  # 替换成你的cdn目录路径
    output_directory = './cleaned_cdn'  # 替换成输出文件的目录
    os.makedirs(output_directory, exist_ok=True)
    process_directory(cdn_directory, output_directory)
