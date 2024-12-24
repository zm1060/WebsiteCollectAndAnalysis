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


#
def parse_output(dns_output):
    # Split the DNS output into sections
    sections = [section.strip() for section in re.split(r'\n\s*;;\s*', dns_output)]

    # Define a regular expression pattern to extract information from each entry
    entry_pattern = re.compile(r'(\S+)\s+(\d+)\s+IN\s+(\w+)\s+(\S+)')

    # Create a set to store unique records based on "Name", "Type", and "Value"
    unique_records = set()

    # Create a dictionary to store the TTL for each unique record
    ttl_dict = {}

    # Parse and organize entries into records for ANSWER SECTION and ADDITIONAL SECTION
    for section in sections:
        if not section:
            continue
        section_lines = section.split('\n')

        # Check if the section is ANSWER SECTION or ADDITIONAL SECTION
        if section_lines[0].startswith("ANSWER SECTION") or section_lines[0].startswith("ADDITIONAL SECTION") or \
                section_lines[0].startswith("AUTHORITY SECTION"):
            entries = entry_pattern.findall('\n'.join(section_lines[1:]))

            for entry in entries:
                name, ttl, record_type, value = entry
                if name == '.' or name == 'cn.' or name == 'com.':
                    continue

                # Check if the record is unique based on "Name", "Type", and "Value"
                record_key = (name, record_type, value)
                if record_key not in unique_records or int(ttl) > ttl_dict[record_key]:
                    unique_records.add(record_key)
                    ttl_dict[record_key] = int(ttl)

    # Convert the set of unique records back to a list for further processing or printing
    unique_records_list = [{"Name": name, "TTL": ttl, "Type": record_type, "Value": value} for
                           (name, record_type, value), ttl in ttl_dict.items()]

    # Print the organized unique records
    for record in unique_records_list:
        print(f"Name: {record['Name']}, TTL: {record['TTL']}, Type: {record['Type']}, Value: {record['Value']}")

    return unique_records_list


def count_dns_records(url):
    url = url.strip()
    sdomain = process_domain(url)
    if sdomain:
        dns_info = {'url': sdomain}

        # Use subprocess to call dig command
        try:
            # Basic query
            # output = subprocess.check_output(['dig', '+noident', sdomain], text=True)
            # output += subprocess.check_output(['dig', '+noident', sdomain, 'A'], text=True)
            # output += subprocess.check_output(['dig', '+noident', sdomain, 'AAAA'], text=True)
            # output += subprocess.check_output(['dig', '+noident', sdomain, 'NS'], text=True)
            # output += subprocess.check_output(['dig', '+noident', sdomain, 'CNAME'], text=True)
            # output += subprocess.check_output(['dig', '+noident', sdomain, 'SRV'], text=True)
            # output += subprocess.check_output(['dig', '+noident', sdomain, 'SPF'], text=True)
            # output += subprocess.check_output(['dig', '+noident', sdomain, 'PTR'], text=True)
            # output += subprocess.check_output(['dig', '+noident', sdomain, 'MX'], text=True)
            # output += subprocess.check_output(['dig', '+noident', sdomain, 'TXT'], text=True)
            output = subprocess.check_output(['dig', '+noident', '+dnssec', sdomain, '@8.8.8.8'], text=True)

            parsed_output = parse_output(output)
            dns_info['records'] = parsed_output
            return dns_info
        except subprocess.CalledProcessError as e:
            return {'url': sdomain, 'error': str(e)}


def process_txt_file(filename, directory):
    unit_name = filename.split('.txt')[0]
    output_filename = f"./new_dns_records/{unit_name}.json"
    if os.path.exists(output_filename):
        return
    urls = []
    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
        urls = file.readlines()

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(count_dns_records, urls))

    os.makedirs('./new_dns_records', exist_ok=True)
    # Save results to a JSON file named after the province
    output_filename = f"./new_dns_records/{unit_name}.json"
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)


def main(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            process_txt_file(filename, directory)


# Example usage
# main('../domain_txt')


# result = count_dns_records('bj.gov.cn')
# print(result)

# trace_output = subprocess.check_output(['dig', '+noident', 'www.sh.gov.cn'], text=True)
# parsed_trace_result = parse_output(trace_output)
# print(parsed_trace_result)


# Example usage:
# url_to_check = "baidu.com"
# result = count_dns_records(url_to_check)
#
# # Print or use the results as needed
# for record_type, record_info in result['records'].items():
#     print(f"Record Type: {record_type}")
#     if 'error' in record_info:
#         print(f"Error: {record_info['error']}")
#     else:
#         for record in record_info:
#             if record['Name']:
#                 print(f"Name: {record['Name']}, TTL: {record['TTL']}, Type: {record['Type']}, Value: {record['Value']}")

# Example usage:
# url_to_check = "sh.gov.cn"
# result = count_dns_records(url_to_check)
#
# # Print or use the results as needed
# for record_type, record_data in result['records'].items():
#     print(f"{record_type} Records:")
#     if 'error' in record_data:
#         print(f"Error: {record_data['error']}")
#     else:
#         for section_name, section_records in record_data.items():
#             print(f"{section_name} SECTION:")
#             for item in section_records:
#                 print(f"Name: {item.get('Name', 'N/A')}, TTL: {item.get('TTL', 'N/A')}, Type: {item.get('Type', 'N/A')}, Value: {item.get('Value', 'N/A')}")


# dig: couldn't get address for 'dns1.dazhou.gov.cn': no more
def extract_domain_part(value):
    # Extract the part between the last two dots
    parts = value.split('.')
    if len(parts) >= 3:
        return parts[-3] + '.' + parts[-2]


def analyze_dns_data(json_data):
    # Filter records with Type "CNAME" and extract the desired domain part
    cname_values = [
        extract_domain_part(record['Value'])
        # record['Value']
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
    total_count = 0
    for cname_value, count in sorted_results:
        total_count += count
    print(total_count)
    with open('dns_analysis_results_sorted.json', 'w', encoding='utf-8') as json_output_file:
        json.dump(results, json_output_file, ensure_ascii=False, indent=4)


def analyze_all():
    all_records = []
    for json_filename in os.listdir('./new_dns_records'):
        with open(f'./new_dns_records/{json_filename}', 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            all_records.extend(json_data)  # Use extend to add records from the list
    print(len(all_records))
    analyze_dns_data(all_records)

    return all_records


#
analyze_all()


company_map = {
    'qaxcloudwaf.com': 'Qi-Anxin Legendsec Information Technology (Beijing) Inc.',
    '365cyd.cn': 'Beijing Knownsec Information Technology Co., Ltd.',
    'saaswaf.com': 'Hangzhou Dbappsecurity Co., Ltd.',
    'glvs.com': 'eName Technology Co., Ltd',
    'gov.cn': 'China Government Self-Operated',
    'v6lvs.com': 'Fujian Wanwu Yilian Network Technology Co., Ltd.',
    'wswebpic.com': 'Wangsu Technology Co., Ltd. Beijing Branch',
    'jiashule.com': 'Beijing Knownsec Information Technology Co., Ltd.',
    'rednetdns.com': 'Changsha Zhiwei Information Technology Co.,Ltd.',
    'jiasule.org': 'Beijing Knownsec Information Technology Co., Ltd.',
    'damddos.com': 'China Telecom Corporation Limited Network Security Product Operation Center',
    'wsssec.com': 'Wangsu Science&Technology Co.,Ltd.',
    'jx163-cname.com': 'Zhongqi Power Technology Co.,Ltd.',
    'icloudv6.com': 'Yundun Intelligent Security Technology Co., Ltd.',
    'allsafeip.com': "Shenzhen Zhi'an Network Co., Ltd.",
    'cdnhwc1.com': 'Huawei Cloud Computing Technologies Co., Ltd.',
    'icloudwaf.com': 'Yundun Intelligent Security Technology Co., Ltd.',
    'bsgslb.cn': 'Beijing Baishanyun Technology Co.,Ltd.',
    'nelcisp.cn': 'THE THIRD RESEARCH INSTITUTE OF THE MINISTRY OF PUBLIC SECURITY',
    'xfsec.net': "Xi'an Xunfeng Technology Co., Ltd.",
    'ctdns.cn': 'Tianyi Cloud Technology Co., Ltd.',
    '360panyun.com': 'Tianjin 360 Security Technology Co., Ltd.',
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
    'yunduncdns.com': 'Shanghai Yundun Information Technology Co., Ltd.',
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
    'cdn300.cn': 'Zhongqi Power Technology Co.,Ltd.',
}

# data = {
#     "qaxcloudwaf.com": 722,
#     "365cyd.cn": 657,
#     "saaswaf.com": 966,
#     "glvs.com": 409,
#     "gov.cn": 238,
#     "v6lvs.com": 222,
#     "wswebpic.com": 175,
#     "jiashule.com": 159,
#     "rednetdns.com": 140,
#     "jiasule.org": 140,
#     "damddos.com": 120,
#     "wsssec.com": 95,
#     "jx163-cname.com": 81,
#     "icloudv6.com": 76,
#     "allsafeip.com": 68,
#     "cdnhwc1.com": 65,
#     "icloudwaf.com": 53,
#     "bsgslb.cn": 53,
#     "nelcisp.cn": 52,
#     "xfsec.net": 52,
#     "ctdns.cn": 51,
#     "360panyun.com": 50,
#     "ctacdn.cn": 50,
#     "aicdn.com": 47,
#     "cdn30.com": 46,
#     "wswebcdn.com": 42,
#     "bzwaf.com": 40,
#     "ddnsec.cn": 38,
#     "chinamobile.com": 20,
#     "qaxanyuv6.com": 19,
#     "bsclink.cn": 18,
#     "cmecloud.cn": 16,
#     "yunduncname.com": 15,
#     "zwyfh.cn": 14,
#     "qtlcdn.com": 13,
#     "trpcdn.net": 12,
#     "igtm-b101.com": 10,
#     "bdydns.com": 9,
#     "yjs-cdn.com": 9,
#     "pywqdns.cn": 9,
#     "kunlunaq.com": 8,
#     "sangfordns.com": 8,
#     "igtm-d101.com": 8,
#     "igtm-a101.com": 8,
#     "igtm-e101.com": 8,
#     "cdn20.com": 7,
#     "nscloudwaf.com": 7,
#     "kunlunca.com": 6,
#     "kunluncan.com": 6,
#     "hwwsdns.cn": 6,
#     "jdcloudwaf.com": 6,
#     "wsglb0.com": 5,
#     "wscvip.cn": 5,
#     "ctadns.cn": 5,
#     "yunduncdns.com": 5,
#     "wjgslb.com": 4,
#     "jcloudgslb.com": 4,
#     "igtm-c101.com": 4,
#     "racetec.cn": 3,
#     "com.cn": 3,
#     "dolfincdnx.com": 3,
#     "aliyunddos1026.com": 3,
#     "yundunwaf5.com": 3,
#     "cmictonecity.cn": 3,
#     "qcloudzygj.com": 3,
#     "wscdns.com": 3,
#     "7cname.com": 3,
#     "xacnnic.com": 3,
#     "cas.cn": 2,
#     "huaweicloudwaf.com": 2,
#     "cdnhwc8.cn": 2,
#     "sfndns.cn": 2,
#     "yunjiasu-cdn.net": 2,
#     "kunlungr.com": 2,
#     "dayugslb.com": 2,
#     "gotocdn.com": 2,
#     "cugslb.cn": 2,
#     "cdnhwc9.com": 2,
#     "t-0p.cn": 2,
#     "yundunwaf4.com": 2,
#     "jx163.com": 2,
#     "thefastcdns.com": 2,
#     "kunlunpi.com": 1,
#     "gfcname.com": 1,
#     "ioiosafe.com": 1,
#     "cmccsecuritywaf.cn": 1,
#     "technames.com": 1,
#     "yundunwaf1.com": 1,
#     "yundunwaf2.com": 1,
#     "faipod.com": 1,
#     "wsdvs.com": 1,
#     "jiexidizhi.top": 1,
#     "365960.com": 1,
#     "tongdanet.com": 1,
#     "kld.wang": 1,
#     "cloudvhost.cn": 1,
#     "yundunwaf3.com": 1,
#     "bestv6.com": 1,
#     "17986.net": 1,
#     "hcnamecdns.com": 1,
#     "mcnamedns.com": 1,
#     "upln.cn": 1,
#     "gotoip4.com": 1,
#     "datasky360.cn": 1,
#     "cdn300.cn": 1
# }
data = {
    "saaswaf.com": 966,
    "qaxcloudwaf.com": 794,
    "v6lvs.com": 710,
    "365cyd.cn": 633,
    "glvs.com": 407,
    "gov.cn": 300,
    "icloudwaf.com": 173,

    # "dbappwaf.cn": 173,
    "allsafeip.com": 140,
    "rednetdns.com": 131,
    "damddos.com": 131,
    "wswebpic.com": 117,
    "jiashule.com": 110,
    "wsssec.com": 91,
    "aicdn.com": 79,
    "jiasule.org": 78,
    "icloudv6.com": 73,
    "wswebcdn.com": 70,
    "jx163-cname.com": 61,
    "cdn20.com": 55,
    "cdnhwc1.com": 52,
    # "360panyun.com": 61,
    # "bdydns.com": 61,
    # "jomodns.com": 61,
    # "ctacdn.cn": 52,
    # "nelcisp.cn": 52,
    # "xfsec.net": 52,
    # "ctdns.cn": 51,
    # "bsgslb.cn": 50,
    # "chinamobile.com": 50,
    # "cdn30.com": 44,
    # "bzwaf.com": 40,
    # "ddnsec.cn": 40,
    # "cloudcsp.com": 23,
    # "bsclink.cn": 18,
    # "cmecloud.cn": 18,
    # "pywqdns.cn": 17,
    # "qaxanyuv6.com": 16,
    # "yunduncname.com": 15,
    # "qtlcdn.com": 13,
    # "yjs-cdn.com": 10,
    # "trpcdn.net": 10,
    # "igtm-b101.com": 10,
    # "kunlunaq.com": 9,
    # "igtm-d101.com": 8,
    # "igtm-a101.com": 8,
    # "igtm-e101.com": 8,
    # "cdnhwcpsd13.com": 7,
    # "cdnhwcprh113.com": 7,
    # "ctadns.cn": 7,
    # "kunluncan.com": 6,
    # "jdcloudwaf.com": 6,
    # "yunduncdns.com": 5,
    # "kunlunca.com": 4,
    # "qcloudzygj.com": 4,
    # "hwwsdns.cn": 4,
    # "igtm-c101.com": 4,
    # "kunlunpi.com": 3,
    # "huaweicloudwaf.com": 3,
    # "wsglb0.com": 3,
    # "racetec.cn": 3,
    # "sangfordns.com": 3,
    # "nscloudwaf.com": 3,
    # "xacnnic.com": 3,
    # "ioiosafe.com": 2,
    # "yunjiasu-cdn.net": 2,
    # "qcloudwzgj.com": 2,
    # "wjgslb.com": 2,
    # "vvipcdn.com": 2,
    # "wscvip.cn": 2,
    # "dolfincdnx.com": 2,
    # "jcloudgslb.com": 2,
    # "jx163.com": 2,
    # "thefastcdns.com": 2,
    # "qcloudcdn.cn": 2,
    # "tdnsv12.com": 2,
    # "7cname.com": 2,
    # "cdnhwc2.com": 2,
    # "cmictonecity.cn": 2,
    # "cdngslb.com": 1,
    # "gfcname.com": 1,
    # "yundunwaf5.com": 1,
    # "cmccsecuritywaf.cn": 1,
    # "aliyunddos1026.com": 1,
    # "alikunlun.com": 1,
    # "queniuqy.com": 1,
    # "com.cn": 1,
    # "tdnsstic1.cn": 1,
    # "ho-wan.cn": 1,
    # "cdnhwc8.cn": 1,
    # "cdnhwcibv122.com": 1,
    # "cd23f.com": 1,
    # "kunlungr.com": 1,
    # "dayugslb.com": 1,
    # "cugslb.cn": 1,
    # "cdnhwc9.com": 1,
    # "cdnhwctnm107.com": 1,
    # "cas.cn": 1,
    # "wscdns.com": 1,
    # "cdnhwcbqs106.com": 1,
    # "sfndns.cn": 1,
    # "yourpage.cn": 1,
    # "t-0p.cn": 1,
    # "technames.com": 1,
    # "yundunwaf1.com": 1,
    # "yundunwaf4.com": 1,
    # "faipod.com": 1,
    # "ourwscs.cn": 1,
    # "wsdvs.com": 1,
    # "jiexidizhi.top": 1,
    # "365960.com": 1,
    # "tongdanet.com": 1,
    # "kld.wang": 1,
    # "cloudvhost.cn": 1,
    # "yundunwaf3.com": 1,
    # "bestv6.com": 1,
    # "17986.net": 1,
    # "hcnamecdns.com": 1,
    # "mcnamedns.com": 1,
    # "upln.cn": 1,
    # "gotoip4.com": 1,
    # "abc188.com": 1,
    # "vhostgo.com": 1,
    # "datasky360.cn": 1
}
#
# 柱状图    数字
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
#
# # Create a DataFrame
# df = pd.DataFrame(list(company_map.items()), columns=['Company', 'Company Name'])
# df['Domain Count'] = df['Company'].map(data.get)  # Use get method with a default value of 0
#
# # Sort DataFrame by Domain Count in descending order
# df = df.sort_values(by='Domain Count', ascending=False).reset_index(drop=True)
#
# # Save to Excel
# df.to_excel('company_data.xlsx', index=False)
#
# # Take only the top 20 companies
# df_top20 = df.head(20)
#
# # Set Seaborn style
# sns.set(style="whitegrid")
#
# # Plot the bar chart for the top 20 companies
# plt.figure(figsize=(12, 8), dpi=500)
# ax = sns.barplot(x=df_top20.index+ 1, y='Domain Count', data=df_top20, palette="viridis")
#
# # Customize the plot
# plt.xlabel('Company Index', fontsize=14)
# plt.ylabel('Domain Counts', fontsize=14)
# plt.title('Domain Counts per Company (Top 20)', fontsize=16)
# plt.xticks(rotation=0, ha='right', fontsize=10)
# plt.yticks(fontsize=12)
#
# # Add data labels
# for p in ax.patches:
#     ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
#                 ha='center', va='center', fontsize=8, color='black', xytext=(0, 5),
#                 textcoords='offset points')
#
# # Show the plot
# plt.tight_layout()
# plt.show()
##########################################################################
# Yes
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
# from matplotlib.ticker import FuncFormatter
#
# # Create a DataFrame
# df = pd.DataFrame(list(company_map.items()), columns=['Company', 'Company Name'])
# df['Domain Count'] = df['Company'].map(data.get)  # Use get method with a default value of 0
#
# # Sort DataFrame by Domain Count in descending order
# df = df.sort_values(by='Domain Count', ascending=False).reset_index(drop=True)
#
# # Save to Excel
# df.to_excel('company_data.xlsx', index=False)
#
# # Take only the top 20 companies
# df_top20 = df.head(20)
#
# # Set Seaborn style
# sns.set(style="white")
#
# # Define a function for formatting y-axis labels as percentages
# def percentage_formatter(x, pos):
#     return f'{(x / 5441) * 100:.2f}%'
#
# # Define a function for adding percentage labels above each bar
# def add_percentage_labels(ax):
#     for p in ax.patches:
#         height = p.get_height()
#         ax.annotate(f'{height / 5441 * 100:.2f}%',
#                     (p.get_x() + p.get_width() / 2., height),
#                     ha='center', va='center', fontsize=14, color='black', xytext=(0, 5),
#                     textcoords='offset points')
#
# # Create the formatter
# formatter = FuncFormatter(percentage_formatter)
#
# # Plot the bar chart for the top 20 companies
# plt.figure(figsize=(12, 8), dpi=500)
# ax = sns.barplot(x=df_top20.index + 1, y='Domain Count', data=df_top20, palette="viridis")
#
# # Set y-axis label format
# ax.yaxis.set_major_formatter(formatter)
#
# # Customize the plot
# plt.xlabel('Company Index', fontsize=18)
# plt.ylabel('Domain Counts (%)', fontsize=18)
# plt.xticks(rotation=0, ha='right', fontsize=18)
# plt.yticks(fontsize=18)
#
# # Add data labels above each bar
# add_percentage_labels(ax)
#
# # Show the plot
# plt.tight_layout()
# plt.show()
