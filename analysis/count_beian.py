# in '../xdns/class' directory, has a lot of directories named with provience name, under the directory of it, has a lot of reponse file of request domain, which is .txt file,
# 统计备案信息，公安备案信息(通过是否有<a href="http://beian.miit.gov.cn/">判断ICP备案 和是否有<a href="https://www.beian.gov.cn/>和公安备案号字段判读是否公安备案  )
# 统计结果以省为单位输出为txt文件。文件以省命名，放在当前目录下 /beian 目录中。
import os
import re
import time
from telnetlib import EC
from urllib.parse import urlparse

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def process_domain(domain):
    domain = domain.lower()
    # Add "http://" to domain names that don't have it
    if not domain.startswith("http"):
        domain = "http://" + domain

    # Parse the URL and extract the base domain
    parsed_url = urlparse(domain)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc
    if not parsed_url.scheme or not parsed_url.netloc:
        return
    return base_url


def check_beian_info(url):
    driver = webdriver.Chrome()

    try:
        # 加载网站
        driver.get(url)
        # Wait for the page to load completely
        time.sleep(5)

        # 获取整个页面的源代码
        page_source = driver.page_source

        # 在源代码中搜索 ICP备案信息和公安备案信息
        icp_beian_info_present = 'http://beian.miit.gov.cn' in page_source or 'ICP' in page_source
        police_beian_info_present = 'https://www.beian.gov.cn' in page_source or '公网安备' in page_source
        free_present = '无障碍' in page_source or '关怀版' in page_source or '无障碍浏览' in page_source
        # 返回检查结果
        data = [
            icp_beian_info_present,
            police_beian_info_present,
            free_present
        ]
        return data
    except Exception:
        return

    finally:
        # 关闭WebDriver
        driver.quit()


def get_domain():
    directory = '../domain_txt'
    output_dir = './beian'
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    all_domain = []
    failed_domains = []

    for filename in os.listdir(directory):
        province_result = {
            'ICP备案': 0,
            '公安备案': 0,
            '无障碍': 0,
        }


        if filename.endswith('.txt'):
            unit_name = filename.split('.txt')[0]
            if os.path.isfile(f'{unit_name}.txt'):
                print(f"File already exists: f{unit_name}.txt")
                continue

            urls = []
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                urls = file.readlines()
            for url in urls:
                url = url.strip()  # Remove leading/trailing whitespace and newlines
                if url:
                    sdomain = process_domain(url)
                    if sdomain:

                        content = check_beian_info(sdomain)

                        # 判断是否有ICP备案信息
                        if content[0] is True:
                            province_result['ICP备案'] += 1
                            print(sdomain, " 完成ICP备案!")
                        else:
                            print(sdomain, " 未进行ICP备案!")
                            with open(os.path.join(output_dir, '未进行ICP备案.txt'), 'w', encoding='utf-8') as out_file:
                                out_file.write(f'{sdomain}\n')

                        # 判断是否有公安备案信息
                        if content[1] is True:
                            province_result['公安备案'] += 1
                            print(sdomain, " 完成公安备案!")
                        else:
                            print(sdomain, " 未完成公安备案!")
                            with open(os.path.join(output_dir, '未进行公安备案.txt'), 'a',
                                      encoding='utf-8') as out_file:
                                out_file.write(f'{sdomain}\n')

                        # 判断是否有无障碍模式
                        if content[2] is True:
                            province_result['无障碍'] += 1
                            print(sdomain, " 支持无障碍模式!")
                        else:
                            print(sdomain, " 不支持无障碍模式!")
                            with open(os.path.join(output_dir, '不支持无障碍模式.txt'), 'a',
                                      encoding='utf-8') as out_file:
                                out_file.write(f'{sdomain}\n')

                        # 将统计结果写入省份的txt文件
                        output_file_path = os.path.join(output_dir, f'{unit_name}.txt')
                        with open(output_file_path, 'w', encoding='utf-8') as output_file:
                            for key, value in province_result.items():
                                output_file.write(f'{key}: {value}\n')

    return all_domain
#
# def process_files():
#     base_dir = '../xdns/class'
#     output_dir = './beian'
#     csv_files = [file for file in os.listdir(base_dir) if file.endswith('.csv')]
#
#     # 创建输出目录
#     os.makedirs(output_dir, exist_ok=True)
#
#     all_domain = []
#     # 遍历csv
#     for file in csv_files:
#         file_path = os.path.join(base_dir, file)
#         province_name = file.split('.csv')[0]
#         df = pd.read_csv(file_path, skiprows=0)
#
#         domain_column = df.iloc[:, 3]
#
#         province_result = {
#             'ICP备案': 0,
#             '公安备案': 0,
#             '无障碍': 0,
#         }
#         # Process each domain name
#         for domain in domain_column:
#             processed_domain = process_domain(domain)
#             # all_domain.append(processed_domain)
#
#             print(processed_domain)
#             all_domain.append(processed_domain)
#
#             content = check_beian_info(processed_domain)
#
#             # 判断是否有ICP备案信息
#             if content[0] is True:
#                 province_result['ICP备案'] += 1
#                 print(domain, " 完成ICP备案!")
#             else:
#                 print(domain, " 未进行ICP备案!")
#                 with open(os.path.join(output_dir, '未进行ICP备案.txt'), 'w', encoding='utf-8') as out_file:
#                     out_file.write(f'{domain}\n')
#
#             # 判断是否有公安备案信息
#             if content[1] is True:
#                 province_result['公安备案'] += 1
#                 print(domain, " 完成公安备案!")
#             else:
#                 print(domain, " 未完成公安备案!")
#                 with open(os.path.join(output_dir, '未进行公安备案.txt'), 'a', encoding='utf-8') as out_file:
#                     out_file.write(f'{domain}\n')
#
#             # 判断是否有无障碍模式
#             if content[2] is True:
#                 province_result['无障碍'] += 1
#                 print(domain, " 支持无障碍模式!")
#             else:
#                 print(domain, " 不支持无障碍模式!")
#                 with open(os.path.join(output_dir, '不支持无障碍模式.txt'), 'a', encoding='utf-8') as out_file:
#                     out_file.write(f'{domain}\n')
#
#             # 将统计结果写入省份的txt文件
#             output_file_path = os.path.join(output_dir, f'{province_name}.txt')
#             with open(output_file_path, 'w', encoding='utf-8') as output_file:
#                 for key, value in province_result.items():
#                     output_file.write(f'{key}: {value}\n')
#
#
# # 运行处理文件函数
# process_files()

get_domain()