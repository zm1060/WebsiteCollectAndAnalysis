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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Use a context manager to ensure the driver is properly closed
    with webdriver.Chrome(options=chrome_options) as driver:
        try:
            # Load the website
            driver.get(url)
            # Wait for the page to load completely
            time.sleep(8)
            # Get the page source
            page_source = driver.page_source

            # Check for ICP备案信息 and 公安备案信息
            icp_beian_info_present = 'http://beian.miit.gov.cn' in page_source or 'ICP' in page_source or 'icp' in page_source
            police_beian_info_present = 'https://www.beian.gov.cn' in page_source or '网安' in page_source
            free_present = '无障碍' in page_source or '关怀版' in page_source or '无障碍浏览' in page_source

            # Check for SRI support
            sri_support = 'integrity=' in page_source

            # Check for CSP support
            csp_support = 'Content-Security-Policy' in page_source

            # Return the check results
            data = [
                icp_beian_info_present,
                police_beian_info_present,
                free_present,
                sri_support,
                csp_support,
            ]
            return data
        except Exception:
            return None

def get_domain():
    directory = '../domain_txt'
    output_dir = './beian'
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    all_domain = []
    failed_domains = []

    for filename in os.listdir(directory):
        province_result = {
            '总数': 0,
            'ICP备案': 0,
            '公安备案': 0,
            '无障碍': 0,
            'SRI支持': 0,
            'CSP支持': 0,
        }


        if filename.endswith('.txt'):
            unit_name = filename.split('.txt')[0]
            if os.path.isfile(f'./beian/{unit_name}.txt'):
                print(f"File already exists: {unit_name}.txt")
                continue

            urls = []
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                urls = file.readlines()
            for url in urls:
                url = url.strip()  # Remove leading/trailing whitespace and newlines
                if url:
                    sdomain = process_domain(url)
                    if sdomain:
                        province_result['总数'] += 1
                        content = check_beian_info(sdomain)
                        if content is None:
                            continue
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
                            with open(os.path.join(output_dir, '支持无障碍模式.txt'), 'a',
                                      encoding='utf-8') as out_file:
                                out_file.write(f'{sdomain}\n')
                        else:
                            print(sdomain, " 不支持无障碍模式!")
                            with open(os.path.join(output_dir, '不支持无障碍模式.txt'), 'a',
                                      encoding='utf-8') as out_file:
                                out_file.write(f'{sdomain}\n')
                        # 判断是否支持SRI
                        if content[3] is True:
                            province_result['SRI支持'] += 1
                            print(sdomain, " 支持SRI!")
                            with open(os.path.join(output_dir, '支持SRI.txt'), 'a',
                                      encoding='utf-8') as out_file:
                                out_file.write(f'{sdomain}\n')
                        else:
                            print(sdomain, " 不支持SRI!")
                            with open(os.path.join(output_dir, '不支持SRI.txt'), 'a',
                                      encoding='utf-8') as out_file:
                                out_file.write(f'{sdomain}\n')

                        # 判断是否支持CSP
                        if content[4] is True:
                            province_result['CSP支持'] += 1
                            print(sdomain, " 支持CSP!")
                            with open(os.path.join(output_dir, '支持CSP.txt'), 'a',
                                      encoding='utf-8') as out_file:
                                out_file.write(f'{sdomain}\n')
                        else:
                            print(sdomain, " 不支持CSP!")
                            with open(os.path.join(output_dir, '不支持CSP.txt'), 'a',
                                      encoding='utf-8') as out_file:
                                out_file.write(f'{sdomain}\n')
            # 将统计结果写入省份的txt文件
            output_file_path = os.path.join(output_dir, f'{unit_name}.txt')
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                for key, value in province_result.items():
                    output_file.write(f'{key}: {value}\n')

    return all_domain


get_domain()