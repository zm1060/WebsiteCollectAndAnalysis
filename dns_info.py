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
import whois
import socket
import dns.resolver
import ipaddress

# 读取CSV文件
def read_csv_file(file_path):
    data = []
    with open(file_path, 'r') as file:
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

# 获取WHOIS注册信息
def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        # 解析WHOIS信息，获取注册公司、注册人姓名、注册商、注册地点、联系方式等
        # 注意：不同的WHOIS服务器返回的信息可能有所不同，你可能需要根据实际情况进行解析
        company = w.get('org', '')
        registrant_name = w.get('name', '')
        registrar = w.get('registrar', '')
        location = w.get('address', '')
        contact = w.get('phone', '')
        return company, registrant_name, registrar, location, contact
    except whois.exceptions.WhoisLookupError:
        return '', '', '', '', ''

# 解析IP地址信息
def get_ip_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        ip_version = ipaddress.ip_address(ip).version
        # 获取IP地址数量和运营商信息
        # 注意：IP地址数量和运营商信息可能需要使用第三方API或数据库进行查询
        # 对于IPv6的部署规模、地理位置等信息，也可以使用第三方服务进行查询
        return ip, ip_version, '运营商信息'
    except socket.gaierror:
        return '', '', ''

# 解析CNAME记录
def get_cname_info(domain):
    try:
        answers = dns.resolver.query(domain, 'CNAME')
        # 解析CNAME记录，判断是否使用CDN服务以及CDN服务商信息
        # 注意：CDN服务商信息可能需要使用第三方API或数据库进行查询
        return True, 'CDN服务商信息'
    except dns.resolver.NoAnswer:
        return False, ''

# 解析NS记录
def get_ns_info(domain):
    try:
        answers = dns.resolver.query(domain, 'NS')
        # 解析NS记录，分析权威服务商特点、权威服务器数量、是否隶属多个服务商等信息
        ns_servers = [str(rdata) for rdata in answers]
        # 注意：你可能需要进一步处理NS记录，例如提取权威服务商的名称并进行统计分析
        return ns_servers
    except dns.resolver.NoAnswer:
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
        domain = clean_url(row[3])
        company, registrant_name, registrar, location, contact = get_whois_info(domain)
        ip, ip_version, isp = get_ip_info(domain)
        has_cdn, cdn_provider = get_cname_info(domain)
        ns_servers = get_ns_info(domain)
        ptr = get_ptr_info(ip)

        # 在这里进行数据分析和统计

# 主函数
def main():
    file_path = 'data.csv'  # 替换为你的CSV文件路径

    # 读取CSV文件数据
    data = read_csv_file(file_path)

    # 处理CSV数据
    process_csv_data(data)

# 运行主函数
if __name__ == '__main__':
    main()