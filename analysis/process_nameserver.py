import socket

from dns import resolver
from qqwry import QQwry

IPDB_FILE = "qqwry.dat"


def get_ip_address_isp(ip):
    q = QQwry()
    q.load_file(IPDB_FILE)
    res = q.lookup(ip.strip())

    return res[0], res[1]


def get_cname_info(domain):
    try:
        answers = resolver.resolve(domain, 'CNAME')
        # 解析CNAME记录，判断是否使用CDN服务以及CDN服务商信息
        # 注意：CDN服务商信息可能需要使用第三方API或数据库进行查询
        print(answers)
        return True, 'CDN服务商信息'
    except resolver.NoAnswer:
        return False, ''


# ip = socket.gethostbyname(domain)

# get_cname_info('www.fengxian.gov.cn')