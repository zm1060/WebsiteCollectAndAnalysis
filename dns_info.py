import dns
from dns import resolver


def get_dns_info(url_input):
    result = resolver.resolve(url_input, 'MX')
    for rdata in result:
        # print('IP', ipval.to_text())
        print('Host', rdata.exchange, 'has preference', rdata.preference)


get_dns_info('baidu.com')
