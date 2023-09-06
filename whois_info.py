# import dnspython

# import dns.resolver
# from ipwhois import IPWhois

import whois

def get_whois_information(domain_name):
    domain = whois.query(domain_name)
    print(domain.__dict__)

get_whois_information('www.360.com')