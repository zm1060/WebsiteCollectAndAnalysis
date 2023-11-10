import os
from collections import Counter
from urllib.parse import urlparse
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor
import re

from matplotlib import pyplot as plt


def process_url(url):
    parsed_url = urlparse(url)
    domains = parsed_url.netloc
    return domains


def process_domain(domain):
    # Add "http://" to domain names that don't have it
    if not domain.startswith("http"):
        domain = "http://" + domain

    # Parse the URL and extract the base domain
    parsed_url = urlparse(domain)
    # base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    if not parsed_url.scheme or not parsed_url.netloc:
        return
    return parsed_url.netloc


def parse_output(dns_output):
    # Split the DNS output into sections
    sections = [section.strip() for section in re.split(r'\n\s*;;\s*', dns_output)]

    # Define a regular expression pattern to extract information from each entry
    entry_pattern = re.compile(r'(\S+)\s+(\d+)\s+IN\s+(\w+)\s+(\S+)')

    # Create a dictionary to store records
    records = []

    # Parse and organize entries into records
    for section in sections:
        if not section:
            continue

        section_lines = section.split('\n')
        entries = entry_pattern.findall('\n'.join(section_lines[1:]))

        for entry in entries:
            name, ttl, record_type, value = entry
            if name == '.' or name == 'cn.' or name == 'com.':
                continue


            records.append({
                "Name": name,
                "TTL": ttl,
                "Type": record_type,
                "Value": value
            })

    # Print the organized records
    for record in records:
        print(f"Name: {record['Name']}, TTL: {record['TTL']}, Type: {record['Type']}, Value: {record['Value']}")
    return records


def count_dns_records(url):
    url = url.strip()
    sdomain = process_domain(url)
    if sdomain:
        dns_info = {'url': sdomain}

        # Use subprocess to call dig command
        try:
            # Basic query
            output = subprocess.check_output(['dig', '+trace', '+noident', sdomain], text=True)
            parsed_output = parse_output(output)
            dns_info['records'] = parsed_output
            return dns_info
        except subprocess.CalledProcessError as e:
            return {'url': sdomain, 'error': str(e)}


def process_txt_file(filename, directory):
    unit_name = filename.split('.txt')[0]
    urls = []
    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
        urls = file.readlines()

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(count_dns_records, urls))

    os.makedirs('./dns_records', exist_ok=True)
    # Save results to a JSON file named after the province
    output_filename = f"./dns_records/{unit_name}.json"
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)


# def parse_output(dns_output):
#     # Split the DNS output into sections
#     sections = [section.strip() for section in re.split(r'\n\s*;;\s*', dns_output)]
#
#     # Define a regular expression pattern to extract information from each entry
#     entry_pattern = re.compile(r'(\S+)\s+(\d+)\s+IN\s+(\w+)\s+(\S+)')
#
#     # Create a dictionary to store records
#     records = {}
#
#     # Parse and organize entries into records
#     for section in sections:
#         if not section:
#             continue
#
#         section_lines = section.split('\n')
#         section_name = section_lines[0].strip(':')
#
#         records[section_name.lower()] = []
#
#         entries = entry_pattern.findall('\n'.join(section_lines[1:]))
#
#         for entry in entries:
#             name, ttl, record_type, value = entry
#             records[section_name.lower()].append({
#                 "Name": name,
#                 "TTL": ttl,
#                 "Type": record_type,
#                 "Value": value
#             })
#
#     # Print the organized records
#     for section_name, entries in records.items():
#         print(section_name)
#         print('-' * 60)
#
#         for entry in entries:
#             print(f"Name: {entry['Name']}, TTL: {entry['TTL']}, Type: {entry['Type']}, Value: {entry['Value']}")
#         print('-' * 60)
#         print('\n')
#     return records


def main(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            process_txt_file(filename, directory)


# Example usage
# main('../domain_txt')

# 示例用法
# trace_output = subprocess.check_output(['dig', '+trace', '+noident', 'cgzf.sh.gov.cn'], text=True)
# # print(trace_output)
# parsed_trace_result = parse_output(trace_output)
# print(parsed_trace_result)


# dig: couldn't get address for 'dns2.dazhou.gov.cn': no more
# dig: couldn't get address for 'dns1.dazhou.gov.cn': no more
def extract_domain_part(value):
    # Extract the part between the last two dots
    parts = value.split('.')
    if len(parts) >= 3:
        return parts[-3]+'.'+parts[-2]

def analyze_dns_data(json_data):
    # Filter records with Type "CNAME" and extract the desired domain part
    cname_values = [
        extract_domain_part(record['Value'])
        for entry in json_data
        if entry is not None
        for record in entry.get('records', [])
        if record.get('Type') == 'CNAME'
    ]

    # Remove None values (when the extraction fails)
    cname_values = [value for value in cname_values if value is not None]

    # Count occurrences of each domain part
    cname_value_counts = Counter(cname_values)

    # Sort the results by count in descending order
    sorted_results = sorted(cname_value_counts.items(), key=lambda x: x[1], reverse=True)

    # Print or analyze the sorted results as needed
    for cname_value, count in sorted_results:
        print(f"CNAME Domain Part: {cname_value}, Count: {count}")

    # Save sorted results to a JSON file
    results = {
        'CNAME_Domain_Parts': {cname_value: count for cname_value, count in sorted_results}
    }

    with open('dns_analysis_results_sorted.json', 'w', encoding='utf-8') as json_output_file:
        json.dump(results, json_output_file, ensure_ascii=False, indent=4)

def analyze_all():
    all_records = []
    for json_filename in os.listdir('./dns_records'):
        with open(f'./dns_records/{json_filename}', 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            all_records.extend(json_data)  # Use extend to add records from the list
    analyze_dns_data(all_records)

    return all_records

analyze_all()


map = {
    'qaxcloudwaf.com':'Qi-Anxin Legendsec Information Technology (Beijing) Inc.',
    '365cyd.cn':'Beijing Knownsec Information Technology Co., Ltd.',
    'saaswaf.com':'Hangzhou Dbappsecurity Co., Ltd.',
    'glvs.com':'eName Technology Co., Ltd',
    'gov.cn':'China Government Self-Operated',
    'v6lvs.com':'Fujian Wanwu Yilian Network Technology Co., Ltd.',
    'wswebpic.com':'Wangsu Technology Co., Ltd. Beijing Branch',
    'jiashule.com':'Beijing Knownsec Information Technology Co., Ltd.',
    'rednetdns.com':'Changsha Zhiwei Information Technology Co.,Ltd.',
    'jiasule.org':'Beijing Knownsec Information Technology Co., Ltd.',
    'damddos.com':'China Telecom Corporation Limited Network Security Product Operation Center',
    'wsssec.com':'Wangsu Science&Technology Co.,Ltd.',
    'jx163-cname.com':'Zhongqi Power Technology Co.,Ltd.',
    'icloudv6.com':'Yundun Intelligent Security Technology Co., Ltd.',
    'allsafeip.com':"Shenzhen Zhi'an Network Co., Ltd.",
    'cdnhwc1.com':'Huawei Cloud Computing Technologies Co., Ltd.',
    'icloudwaf.com':'Yundun Intelligent Security Technology Co., Ltd.',
    'bsgslb.cn':'Beijing Baishanyun Technology Co.,Ltd.',
    'nelcisp.cn':'THE THIRD RESEARCH INSTITUTE OF THE MINISTRY OF PUBLIC SECURITY',
    'xfsec.net':"Xi'an Xunfeng Technology Co., Ltd.",
    'ctdns.cn':'Tianyi Cloud Technology Co., Ltd.',
    '360panyun.com':'Tianjin 360 Security Technology Co., Ltd.',
    'ctacdn.cn': 'Tianyi Cloud Technology Co., Ltd.',
    'aicdn.com': 'Hangzhou Dianzhilian Technology Co., Ltd.',
    'cdn30.com': 'Wangsu Science&Technology Co.,Ltd.',
    'wswebcdn.com': 'Wangsu Science&Technology Co.,Ltd.',
    'bzwaf.com': 'Chengdu West Dimension Digital Technology Co.,Ltd.',
    'ddnsec.cn': 'Changsha Zhiwei Information Technology Co.,Ltd.',
    'chinamobile.com': 'China Mobile Communication Company Limited',
    'qaxanyuv6.com': 'Qi-Anxin Legendsec Information Technology (Beijing) Inc.',
    'bsclink.cn': 'Beijing Baishanyun Technology Co.,Ltd.',
    'cmecloud.cn': 'China Mobile(SuZhou)Software Technology Co.,Ltd.',
    'yunduncname.com': 'Shanghai Yundun Information Technology Co., Ltd.',
    'zwyfh.cn': "Xi'an Xunfeng Technology Co., Ltd.",
    'qtlcdn.com': 'Wangsu Science&Technology Co.,Ltd.',
    'trpcdn.net': 'Beijing Baishanyun Technology Co.,Ltd.',
    'igtm-b101.com': 'DNSPod,Inc.',
    'bdydns.com': 'Beijing Baidu Netcom Science and Technology Co.,Ltd.',
    'yjs-cdn.com': 'Beijing Baidu Netcom Science and Technology Co.,Ltd.',
    'pywqdns.cn': 'DNSPod,Inc.',
    'kunlunaq.com': 'Zhejiang Queniu Network Technology Co., Ltd.',
    'sangfordns.com': 'Sangfor Technologies Inc.',
    'igtm-d101.com': 'DNSPod,Inc.',
    'igtm-a101.com': 'DNSPod,Inc.',
    'igtm-e101.com': 'DNSPod,Inc.',
    'cdn20.com': 'Wangsu Science&Technology Co.,Ltd.',
    'nscloudwaf.com': 'NSFOCUS TECHNOLOGIES, INC.',
    'kunlunca.com': 'Zhejiang Queniu Network Technology Co., Ltd.',
    'kunluncan.com': 'Zhejiang Queniu Network Technology Co., Ltd.',
    'hwwsdns.cn': 'Shanghai Yundun Information Technology Co., Ltd.',
    'jdcloudwaf.com': 'Beijing Jingdong 360 Degree Electric Commerce Co., Ltd.',
    'wsglb0.com': 'Wangsu Science&Technology Co.,Ltd.',
    'wscvip.cn': 'Wangsu Science&Technology Co.,Ltd.',
    'ctadns.cn': 'Tianyi Cloud Technology Co., Ltd.',
    'yunduncdns.com,': 'Shanghai Yundun Information Technology Co., Ltd.',
    'wjgslb.com': 'Shenzhen Wangjuyunlian Technology Co., Ltd.',
    'jcloudgslb.com': 'Beijing Jingdong 360 Degree Electric Commerce Co., Ltd.',
    'igtm-c101.com': 'DNSPod,Inc.',
    'racetec.cn': 'Ruixi Technology (Beijing) Co., Ltd.',
    'com.cn': 'xxxx',
    'dolfincdnx.com': 'Guizhou Baishan Cloud Technology Co., Ltd.',
    'aliyunddos1026.com': 'Zhejiang Alibaba Cloud Computing Co., Ltd.',
    'yundunwaf5.com': 'Shanghai Yundun Information Technology Co., Ltd.',
    'cmictonecity.cn': 'Zhong Yi System Integration Co., Ltd',
    'qcloudzygj.com': 'Tencent Cloud Computing(Beijing) Company Limited',
    'wscdns.com': 'Wangsu Science&Technology Co.,Ltd.',
    '7cname.com': 'Pine wisdom (Beijing) technology co., Ltd.',
    'xacnnic.com': 'Xian RongTian Information Tech. CO., LTD.',
    'cas.cn': 'Chinese Academy Of Sciences',
    'huaweicloudwaf.com': 'Huawei Cloud Computing Technologies Co., Ltd.',
    'cdnhwc8.cn': 'Huawei Cloud Computing Technologies Co., Ltd.',
    'sfndns.cn': 'Beijing Sanfront Information Technology Co.,Ltd.',
    'yunjiasu-cdn.net': 'Beijing Baidu Netcom Science and Technology Co.,Ltd.',
    'kunlungr.com': 'Zhejiang Queniu Network Technology Co., Ltd.',
    'dayugslb.com': 'Shenzhen Tencent Computer System Co., Ltd.',
    'gotocdn.com': 'Personal',
    'cugslb.cn': 'China Unicom Cloud Data Co.,Ltd.',
    'cdnhwc9.com': 'Huawei Cloud Computing Technologies Co., Ltd.',
    't-0p.cn': 'Beijing Tianrongxin Software Co., Ltd.',
    'yundunwaf4.com': 'Shanghai Yundun Information Technology Co., Ltd.',
    'jx163.com': 'JiangXi Telecom Information Industry Co.,Ltd.',
    'thefastcdns.com': 'Zhongqi Power Technology Co.,Ltd.',
    'kunlunpi.com': 'Zhejiang Queniu Network Technology Co., Ltd.',
    'gfcname.com': 'Guangdong Chenyun Network Technology Co., Ltd.',
    'ioiosafe.com': 'Alibaba Cloud Computing (Beijing) Co.,Ltd.',
    'cmccsecuritywaf.cn': 'China Mobile IOT Company Limited',
    'technames.com': 'Alibaba Cloud Computing (Beijing) Co.,Ltd.',
    'yundunwaf1.com': 'Shanghai Yundun Information Technology Co., Ltd.',
    'yundunwaf2.com': 'Shanghai Yundun Information Technology Co., Ltd.',
    'faipod.com': 'Guangzhou Faisco Internet And Technology Company Limited',
    'wsdvs.com': 'Wangsu Science&Technology Co.,Ltd.',
    'jiexidizhi.top': 'Zhengzhou Gainet Network Technology Co.,Ltd.',
    '365960.com': 'Beijing Agricultural information technology Co..Ltd.',
    'tongdanet.com': 'Puyang Tongda Network Technology Service Co., Ltd.',
    'kld.wang': 'Gongyi Claude Network Technology Service Co., Ltd.',
    'cloudvhost.cn': 'Zhengzhou Gainet Network Technology Co.,Ltd.',
    'yundunwaf3.com': 'Shanghai Yundun Information Technology Co., Ltd.',
    'bestv6.com': 'Shenzhen Wanwuyunlian Technology Co., Ltd.',
    '17986.net': 'eName Technology Co.,Ltd.',
    'hcnamecdns.com': 'Amazon Registrar,Inc.',
    'mcnamedns.com': 'Amazon Registrar,Inc.',
    'upln.cn': 'China Medical University',
    'gotoip4.com': '***Personal***',
    'datasky360.cn': 'Beijing Hongtu Jiadu Communication Equipment Co.,Ltd.',
    'cdn300.cn': 'Zhongqi Power Technology Co.,Ltd.'
}