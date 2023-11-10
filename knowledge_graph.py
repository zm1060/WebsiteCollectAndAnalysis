import os
from urllib.parse import urlparse

import networkx as nx
import whois
import socket
import ssl

from matplotlib import pyplot as plt

# 创建一个空的图谱
knowledge_graph = nx.Graph()

# 添加域名节点
def add_domain_node(graph, domain_name):
    graph.add_node(domain_name, type="domain")

# 获取并添加IP地址节点
def get_and_add_ip_address(graph, domain_name):
    try:
        ip_address = socket.gethostbyname(domain_name)
        graph.add_node(ip_address, type="ip_address")
        graph.add_edge(domain_name, ip_address, relationship="resolved_to")
        return ip_address
    except socket.gaierror as e:
        print(f"Error resolving domain: {e}")
        return None

# 获取并添加SSL证书信息节点
def get_and_add_ssl_certificate(graph, domain_name):
    try:
        ssl_info = ssl.get_server_certificate((domain_name, 443))
        graph.add_node("SSL Certificate", type="ssl_certificate")
        graph.add_edge(domain_name, "SSL Certificate", relationship="has_certificate")
        return ssl_info
    except Exception as e:
        print(f"Error retrieving SSL certificate: {e}")
        return None

# 获取并添加WHOIS信息节点
def get_and_add_whois_info(graph, domain_name):
    try:
        domain_info = whois.whois(domain_name)
        graph.add_node("WHOIS Info", type="whois_info")
        graph.add_edge(domain_name, "WHOIS Info", relationship="has_info")
        return domain_info
    except Exception as e:
        print(f"Error retrieving WHOIS info: {e}")
        return None

def process_url(url):
    parsed_url = urlparse(url)
    domains = parsed_url.netloc
    return domains


def get_domain():
    directory = './domain_txt'
    all_domain = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt') and filename == "教育部.txt":
            unit_name = filename.split('.txt')[0]
            urls = []
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                urls = file.readlines()
            for url in urls:
                url = url.strip()  # Remove leading/trailing whitespace and newlines
                if url:
                    sdomain = process_domain(url)
                    if sdomain:
                        all_domain.append(sdomain)
                        print(sdomain)
    return all_domain


def process_domain(domain):
    # Add "http://" to domain names that don't have it
    if not domain.startswith("http"):
        domain = "http://" + domain

    # Parse the URL and extract the base domain
    parsed_url = urlparse(domain)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    if  not parsed_url.scheme or not parsed_url.netloc:
        return
    return base_url


all_domains = get_domain()
# 遍历域名列表并处理
for domain_name in all_domains:
    if not domain_name:
        continue
    domain = urlparse(domain_name).netloc
    # 添加域名节点
    add_domain_node(knowledge_graph, domain)

    # 获取并添加IP地址节点
    ip_address = get_and_add_ip_address(knowledge_graph, domain_name)

    # 获取并添加SSL证书信息节点
    ssl_info = get_and_add_ssl_certificate(knowledge_graph, domain_name)

    # 获取并添加WHOIS信息节点
    domain_info = get_and_add_whois_info(knowledge_graph, domain_name)

# 打印图谱的节点和边
print("Nodes:", knowledge_graph.nodes())
print("Edges:", knowledge_graph.edges())
# Create a layout for the graph (you can choose different layouts as needed)
layout = nx.spring_layout(knowledge_graph)

# Draw the graph
nx.draw(knowledge_graph, pos=layout, with_labels=True, node_size=500, node_color='lightblue')

# Display the graph
plt.show()