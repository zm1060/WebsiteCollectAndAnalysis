import random

import whois


def classify_nameserver(domain, ns_domain):
    # Extract the second-level domain (SLD) and top-level domain (TLD) from the domain and NS domain
    domain_parts = domain.split('.')
    ns_parts = ns_domain.split('.')
    domain_sld_tld = '.'.join(domain_parts[-2:])
    ns_sld_tld = '.'.join(ns_parts[-2:])
    print(domain_sld_tld)
    print(ns_sld_tld)
    # Check if the SLD+TLD of the website and NS match
    if domain_sld_tld == ns_sld_tld:
        return "Private"

    # Check if the SLD+TLD of the NS exists in the SAN list of the website
    w = whois.whois(domain)
    print(w)
    if w and 'subject_alt_name' in w:
        san_list = w['subject_alt_name']
        if ns_sld_tld in san_list:
            return "Private"

    # Check if the SOA of the website and NS match
    if w and 'name_servers' in w:
        website_ns = w['name_servers']
        if isinstance(website_ns, list) and ns_domain in website_ns:
            return "Private"

    # Check if the concentration of the NS exceeds 50
    ns_concentration = calculate_nameserver_concentration(domain, ns_domain)
    if ns_concentration > 50:
        return "Third Party"

    return "Unknown"


def calculate_nameserver_concentration(domain, ns_domain):
    # Implement your logic to calculate the concentration of the NS here
    # This could involve querying DNS records and analyzing the results
    # For simplicity, let's assume a random concentration value between 0 and 100
    return random.randint(0, 100)


# Example usage
website_domain = "sh.gov.cn"
ns_domain = "ns2.shanghai.gov.cn"
classification = classify_nameserver(website_domain, ns_domain)
print(f"The nameserver {ns_domain} is classified as: {classification}")
