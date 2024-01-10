import os
import json


def process_cdn_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 过滤掉不需要的行
    filtered_lines = [line for line in lines if not line.startswith(('服务器:  UnKnown', 'Address:  172.26.26.3'))]
    filtered_lines = [line.replace('Address:', 'Addresses:') for line in filtered_lines]

    # 组织成JSON格式
    data = []
    current_entry = None

    line_index = 0
    total_lines = len(filtered_lines)

    while line_index < total_lines:
        line = filtered_lines[line_index]

        if line.startswith('名称:'):
            if current_entry:
                data.append(current_entry)
            current_entry = {'Name': line.split(':')[1].strip(), 'Addresses': [], 'Aliases': []}
            if line.split(':')[1].strip() == 'xy.mdj.gov.cn':
                print('I am going')
        elif line.startswith('Addresses:'):
            # Extract addresses from the current line and subsequent lines
            addresses = []
            while line.startswith('Addresses:') or not line.strip():
                if 'Addresses:' in line:
                    address_part = line.split('Addresses:')[1].strip()
                    addresses.extend(addr.strip() for addr in address_part.split())
                # print(address_part)
                if address_part == '218.10.148.62':
                    print('***********')

                line_index += 1
                if line_index < total_lines:
                    line = filtered_lines[line_index]
                    if line.startswith(('名称:', 'Aliases:', 'Addresses:')):
                        line_index -= 1
                else:
                    break
            # Continue extracting addresses from subsequent lines until a line without leading whitespace, end of file, or a line starting with 'Addresses:', 'Aliases:', or '名称:'
            while line.strip() and not line.startswith(('Addresses:', '名称:')):
                # Skip lines starting with 'Aliases:' in the 'Addresses' extraction loop
                if not line.startswith('Aliases:'):
                    addresses.extend(addr.strip() for addr in line.split())
                    line_index += 1
                    if line_index < total_lines:
                        line = filtered_lines[line_index]
                        if line.startswith(('名称:', 'Aliases:', 'Addresses:')):
                            line_index -= 1
                    else:
                        break
                else:
                    # print('befor: ', filtered_lines[line_index])
                    # line_index -= 1
                    # print('after: ', filtered_lines[line_index])
                    break
            current_entry['Addresses'].extend(addresses)
        elif line.startswith('Aliases:'):
            aliases = []
            while line.startswith('Aliases:') or not line.strip():
                if 'Aliases:' in line:
                    aliases_part = line.split('Aliases:')[1].strip()
                    aliases.extend(addr.strip() for addr in aliases_part.split())
                line_index += 1
                if line_index < total_lines:
                    line = filtered_lines[line_index]
                    if line.startswith(('名称:', 'Aliases:', 'Addresses:')):
                        line_index -= 1
                else:
                    break
            while line.strip() and not line.startswith(('服务器:', '名称:', 'Aliases:', 'Addresses:')):
                aliases.extend(addr.strip() for addr in line.split())
                line_index += 1
                if line_index < total_lines:
                    line = filtered_lines[line_index]
                    if line.startswith(('名称:', 'Aliases:', 'Addresses:')):
                        line_index -= 1
                else:
                    break
            current_entry['Aliases'].extend(aliases)

        line_index += 1

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
