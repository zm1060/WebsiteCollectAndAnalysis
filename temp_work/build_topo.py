# from urllib.parse import urlparse
#
# import networkx as nx
# import requests
# from bs4 import BeautifulSoup
# from matplotlib import pyplot as plt
#
#
# def get_domain(url):
#     parsed_url = urlparse(url)
#     return parsed_url.netloc
#
#
# def get_website_links(url, base_url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     links = [a['href'] for a in soup.find_all('a', href=True) if
#              urlparse(a['href']).netloc != '' and get_domain(a['href']) != base_url]
#     return links
#
#
# def build_domain_topology(start_url, depth=1):
#     G = nx.Graph()
#     visited_urls = set()
#     base_domain = get_domain(start_url)
#
#     def explore_url(url, current_depth):
#         if current_depth > depth or url in visited_urls:
#             return
#
#         visited_urls.add(url)
#         links = get_website_links(url, base_domain)
#
#         for link in links:
#             G.add_edge(base_domain, get_domain(link))
#             explore_url(link, current_depth + 1)
#
#     explore_url(start_url, 1)
#     return G
#
#
# def visualize_topology(graph):
#     pos = nx.spring_layout(graph)
#     nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=800, node_color='skyblue', font_size=8,
#             edge_color='gray', linewidths=0.5)
#     plt.show()
#
#
# if __name__ == "__main__":
#     # 请替换为你要分析的网站首页
#     start_url = "https://www.twnic.tw/"
#
#     domain_topology = build_domain_topology(start_url, depth=1)
#     visualize_topology(domain_topology)


import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import networkx as nx
from matplotlib import pyplot as plt
from geopy.geocoders import Nominatim


def get_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc


def get_website_links(url, base_url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True) if
             urlparse(a['href']).netloc != '' and get_domain(a['href']) != base_url]
    return links


def build_domain_topology(start_url, depth=1):
    G = nx.Graph()
    visited_urls = set()
    base_domain = get_domain(start_url)

    def explore_url(url, current_depth):
        if current_depth > depth or url in visited_urls:
            return

        visited_urls.add(url)
        links = get_website_links(url, base_domain)

        for link in links:
            target_domain = get_domain(link)
            G.add_edge(base_domain, target_domain)
            explore_url(link, current_depth + 1)

    explore_url(start_url, 1)
    return G


def get_location_info(domain):
    geolocator = Nominatim(user_agent="geo_locator", timeout=10)  # Adjust the timeout value
    location = geolocator.geocode(domain)
    if location:
        return (location.latitude, location.longitude)
    return None


def visualize_topology(graph, location_info):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=800, node_color='skyblue', font_size=8,
            edge_color='gray', linewidths=0.5)

    for domain, location in location_info.items():
        if location:
            plt.scatter(location[1], location[0], c='red', marker='o')
            plt.text(location[1], location[0], domain, fontsize=8, ha='left')

    plt.show()


if __name__ == "__main__":
    start_url = input("Enter a website URL: ")
    domain_topology = build_domain_topology(start_url, depth=1)

    # Get location information for domains
    location_info = {}
    for node in domain_topology.nodes:
        location_info[node] = get_location_info(node)

    visualize_topology(domain_topology, location_info)
