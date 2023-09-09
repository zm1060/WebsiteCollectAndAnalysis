# 在目录下有两个csv文件，csv的第四列是域名，可能包含http://或http://，也可能没有，如果有则全部去掉，然后对于非.gov.cn的域名，获取它们的WHOIS注册信息，分析以下内容：注册公司，注册人姓名，注册商，注册地点，联系方式
# - IPv4和IPv6
#   - IP地址数量和运营商，冗余角度分析
#   - IPv6的部署规模
#   - IP地址的地理位置，省市级别的网站的IP是否是在特定区域，使访问更快
#   - 托管商是本地服务商，还是云服务商
# - CNAME
#   - 是否使用CDN服务
#   - CDN服务商
# - NS (参考文献[2])
# 平均水平、全国各省市横向对比，分析NS的情况
#   - 权威服务商特点，是否集中，可绘图展示
#   - 权威服务器数量，冗余角度分析
#   - 权威服务器是否隶属多个服务商
#   - 权威服务器是第三方，还是自建
# - PTR记录？为什么有，普及率呢？

import csv
import json
import os
from datetime import datetime
from time import sleep

import dns
import whois
import socket
from dns import resolver
import ipaddress

from qqwry import QQwry
from qqwry import updateQQwry

IPDB_FILE = "qqwry.dat"


# 读取CSV文件
def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            data.append(row)
    return data


# 去掉URL中的'http://'或'https://'
def clean_url(url):
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]
    return url


class WHOISEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


# 获取WHOIS注册信息
def get_whois_info(domain):
    try:

        # 解析WHOIS信息，获取注册公司、注册人姓名、注册商、注册地点、联系方式等
        # 注意：不同的WHOIS服务器返回的信息可能有所不同，你可能需要根据实际情况进行解析

        # Write 'w' into a JSON file
        filename = os.path.join('whois_result', domain + '.json')
        if os.path.isfile(filename):
            print(filename, ' already exisits!')
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            temp = data.get('domain_name', '')
            if temp is None:
                print(temp, ' skipped!')
                w = whois.whois(domain)
                whois._cachefile = None
                whois._cachetime = None
                whois._whois_cache = {}
                return
            return

        w = whois.whois(domain)
        whois._cachefile = None
        whois._cachetime = None
        whois._whois_cache = {}

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(w, file, ensure_ascii=False, indent=4, cls=WHOISEncoder)

        domain_name = w.get('domain_name', '')
        registrar = w.get('registrar', '')
        creation_date = w.get('creation_date', '')
        expiration_date = w.get('expiration_date', '')
        name_servers = w.get('name_servers', '')
        status = w.get('status', '')
        dnssec = w.get('dnssec', '')
        emails = w.get('emails', '')
        name = w.get('name', '')
        if domain_name is None:
            print(domain_name, ' skipped!')
            with open('failed_domain.txt', 'a', encoding='utf-8') as file:
                file.write(domain + '\n')
            return

        print(filename, ' new created!')
        sleep(1)
        return domain_name, registrar, creation_date, expiration_date, name_servers, status, dnssec, emails, name
    except Exception as e:
        print("Failed to get whois info about ", domain)


# 解析IP地址信息
def get_ip_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        ip_version = ipaddress.ip_address(ip).version
        # 获取IP地址数量和运营商信息
        # 注意：IP地址数量和运营商信息可能需要使用第三方API或数据库进行查询
        # 对于IPv6的部署规模、地理位置等信息，也可以使用第三方服务进行查询
        return ip, ip_version
    except socket.gaierror:
        return '', ''


# 解析CNAME记录
def get_cname_info(domain):
    try:
        answers = resolver.resolve(domain, 'CNAME')
        # 解析CNAME记录，判断是否使用CDN服务以及CDN服务商信息
        # 注意：CDN服务商信息可能需要使用第三方API或数据库进行查询
        return True, 'CDN服务商信息'
    except resolver.NoAnswer:
        return False, ''


# 解析IP获取地址,运营商信息
# return value: (归属地,运营商)
def get_ip_address_isp(ip):
    q = QQwry()
    q.load_file(IPDB_FILE)
    res = q.lookup(ip.strip())

    return res[0], res[1]


# 判断目标是否存在CDN
def detectCDN(domain):
    parm = 'nslookup ' + domain
    result = os.popen(parm).read()
    print(result)
    return result


# 解析NS记录
def get_ns_info(domain):
    try:
        answers = resolver.resolve(domain, 'NS')
        # 解析NS记录，分析权威服务商特点、权威服务器数量、是否隶属多个服务商等信息
        ns_servers = [str(rdata) for rdata in answers]
        # 注意：你可能需要进一步处理NS记录，例如提取权威服务商的名称并进行统计分析
        return ns_servers
    except resolver.NoAnswer:
        return []


# 解析PTR记录
def get_ptr_info(ip):
    try:
        ptr = socket.gethostbyaddr(ip)[0]
        # 解析PTR记录，判断普及率等信息
        return ptr
    except socket.herror:
        return ''


# 处理CSV文件中的数据
def process_csv_data(data):
    for row in data:
        domain = clean_url(row[3]).split('/')[0]
        get_whois_info(domain)
        # ip, ip_version, isp = get_ip_info(domain)
        # has_cdn, cdn_provider = get_cname_info(domain)
        # ns_servers = get_ns_info(domain)
        # ptr = get_ptr_info(ip)

        # 在这里进行数据分析和统计


# 主函数
def main():
    # 设置DNS解析器的名称服务器
    # resolver = dns.resolver.Resolver()
    # resolver.nameservers = ['223.5.5.5', '1.2.4.8', '180.76.76.76', '101.226.4.6', '114.114.114.114', '172.26.26.3']  # 替换为你的名称服务器列表
    ####################################################################################################################
    #  Get Whois Information
    ####################################################################################################################
    # file_path = 'total.csv'  # 替换为你的CSV文件路径
    # # 读取CSV文件数据
    # data = read_csv_file(file_path)
    # # 处理CSV数据
    # process_csv_data(data)
    #
    #
    # with open('failed_domain.txt', 'r', encoding='utf-8') as file:
    #     domains = file.read().splitlines()
    #
    # for domain in domains:
    #     get_whois_info(domain)
    ####################################################################################################################
    #  ISP  and Address information collection
    ####################################################################################################################
    # root_directory = '../xdns/class'
    # ip_address_info_list = []
    #
    # for province_directory in os.listdir(root_directory):
    #     # province_directory_path = os.path.join(root_directory, '/'+province_directory)
    #     province_directory_path = f"{root_directory}/{province_directory}"
    #     if not os.path.isdir(province_directory_path):
    #         continue
    #
    #     count_ipv4 = 0
    #     count_ipv6 = 0
    #
    #     for filename in os.listdir(province_directory_path):
    #         if not filename.endswith('.txt'):
    #             continue
    #         domain = filename.split('.txt')[0]
    #         # file_path = os.path.join(province_directory_path, filename)
    #         # with open(file_path, 'r', encoding='utf-8') as file:
    #         #     response = file.read().strip()  # Assuming the response is stored as text in the file
    #
    #         try:
    #             ip, version = get_ip_info(domain)
    #             address, isp = get_ip_address_isp(ip)
    #             ip_address_info_list.append((domain, ip, version, address, isp))
    #             if version == 4:
    #                 count_ipv4 += 1
    #             elif version == 6:
    #                 count_ipv6 += 1
    #
    #         except Exception:
    #             print(f"Failed to resolve IP address for domain: {domain}")
    #             with open('./failed_ip.txt', 'w', encoding='utf-8') as file:
    #                 file.write(f"{domain}\n")
    #             continue
    #
    #     with open(os.path.join(province_directory_path, 'ip_address_info.txt'), 'w', encoding='utf-8') as file:
    #         for info in ip_address_info_list:
    #             file.write(f"{info}\n")
    #         file.write("\n")
    #
    #         file.write(f"Province: {province_directory}")
    #         file.write(f"IPv4 count: {count_ipv4}")
    #         file.write(f"IPv6 count: {count_ipv6}")
    #     ip_address_info_list = []
    ####################################################################################################################
    #  Check   CDN
    ####################################################################################################################
    root_directory = '../xdns/class'
    result_list = []
    for province_directory in os.listdir(root_directory):
        province_directory_path = f"{root_directory}/{province_directory}"
        if not os.path.isdir(province_directory_path):
            continue
        cdn_count = 0
        ncdn_count = 0
        for filename in os.listdir(province_directory_path):
            if not filename.endswith('.txt'):
                continue
            domain = filename.split('.txt')[0]

            try:
                cdn_info = detectCDN(domain)
                if cdn_info.count(".") > 10:
                    print(domain + " 存在CDN")
                    cdn_count += 1
                else:
                    print(domain + " 不存在CDN")
                    ncdn_count += 1
                result_list.append(cdn_info)
            except Exception:
                print(f"Failed to run nslookup for domain: {domain}")
                with open('./failed_nslookup.txt', 'w', encoding='utf-8') as file:
                    file.write(f"{domain}\n")
                continue

        with open(os.path.join(province_directory_path, 'ip_cdn_info.txt'), 'w', encoding='utf-8') as file:
            for info in result_list:
                file.write(f"{info}\n")
            file.write("\n")

            file.write(f"Province: {province_directory}")
            file.write(f"CDN count: {cdn_count}")
            file.write(f"NoneCDN count: {ncdn_count}")
        result_list = []


# 运行主函数
if __name__ == '__main__':
    main()
