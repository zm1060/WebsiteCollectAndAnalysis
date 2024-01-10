# import json
# from urllib.parse import urlparse
#
# import networkx as nx
# import matplotlib.pyplot as plt
#
#
# def analyze_domain_relationships(province_data):
#     domain_counts = {}
#     G = nx.Graph()
#
#     for province_info in province_data:
#         for site_info in province_info['sites']:
#             url = site_info['url']
#             domain = urlparse(url).netloc
#
#             if domain not in domain_counts:
#                 domain_counts[domain] = 1
#             else:
#                 domain_counts[domain] += 1
#
#     # Add nodes and edges to the graph
#     for province_info in province_data:
#         for site_info in province_info['sites']:
#             url = site_info['url']
#             domain = urlparse(url).netloc
#
#             if domain_counts[domain] > 1:  # Only add nodes with more than one occurrence
#                 G.add_node(domain, weight=domain_counts[domain])
#
#                 for link in site_info['internal_links'] + site_info['external_links']:
#                     linked_domain = urlparse(link).netloc
#
#                     if linked_domain != domain and linked_domain in domain_counts:
#                         G.add_edge(domain, linked_domain)
#
#     return G
#
#
# def plot_graph(graph):
#     pos = nx.spring_layout(graph)
#     node_sizes = [graph.nodes[node]['weight'] * 50 for node in graph.nodes]
#
#     plt.figure(figsize=(12, 12))
#     nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, node_color='skyblue')
#     nx.draw_networkx_edges(graph, pos, edge_color='gray', alpha=0.5)
#     nx.draw_networkx_labels(graph, pos, font_size=10, font_color='black')
#
#     plt.title("Domain Relationships")
#     plt.axis('off')
#     plt.show()
#
#
# if __name__ == "__main__":
#     # Load province_data from the saved JSON file
#     with open('province_data.json', 'r', encoding='utf-8') as json_file:
#         province_data = json.load(json_file)
#
#     # Analyze domain relationships
#     domain_graph = analyze_domain_relationships(province_data)
#
#     # Plot the domain relationships graph
#     plot_graph(domain_graph)

#######################################################################################
# import json
# from urllib.parse import urlparse
#
# import networkx as nx
# import matplotlib.pyplot as plt
#
# def analyze_domain_relationships(province_data):
#     domain_counts = {}
#     G = nx.Graph()
#
#     for province_info in province_data:
#         for site_info in province_info['sites']:
#             url = site_info['url']
#             domain = urlparse(url).netloc
#
#             if domain not in domain_counts:
#                 domain_counts[domain] = 1
#             else:
#                 domain_counts[domain] += 1
#
#     # Add nodes and edges to the graph
#     for province_info in province_data:
#         for site_info in province_info['sites']:
#             url = site_info['url']
#             domain = urlparse(url).netloc
#
#             if domain_counts[domain] > 1:  # Only add nodes with more than one occurrence
#                 G.add_node(domain, weight=domain_counts[domain])
#
#                 for link in site_info['internal_links'] + site_info['external_links']:
#                     linked_domain = urlparse(link).netloc
#
#                     if linked_domain != domain and linked_domain in domain_counts:
#                         G.add_edge(domain, linked_domain)
#
#     return G
#
# def plot_graph(graph):
#     pos = nx.spring_layout(graph)
#     node_sizes = [graph.nodes[node]['weight'] * 50 for node in graph.nodes]
#
#     plt.figure(figsize=(12, 12))
#     nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, node_color='skyblue')
#     nx.draw_networkx_edges(graph, pos, edge_color='gray', alpha=0.5)
#     nx.draw_networkx_labels(graph, pos, font_size=10, font_color='black')
#
#     plt.title("Domain Relationships")
#     plt.axis('off')
#     plt.show()
#
# def analyze_advanced(graph):
#     # Calculate centrality measures
#     degree_centrality = nx.degree_centrality(graph)
#     betweenness_centrality = nx.betweenness_centrality(graph)
#     closeness_centrality = nx.closeness_centrality(graph)
#
#     # Identify communities using Louvain algorithm
#     communities = nx.community.best_partition(graph)
#
#     print("\nDegree Centrality:")
#     for node, centrality in sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
#         print(f"{node}: {centrality}")
#
#     print("\nBetweenness Centrality:")
#     for node, centrality in sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
#         print(f"{node}: {centrality}")
#
#     print("\nCloseness Centrality:")
#     for node, centrality in sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
#         print(f"{node}: {centrality}")
#
#     print("\nCommunities:")
#     for community_id, nodes in nx.connected_components(graph):
#         print(f"Community {community_id}: {nodes}")
#
# if __name__ == "__main__":
#     # Load province_data from the saved JSON file
#     with open('province_data.json', 'r', encoding='utf-8') as json_file:
#         province_data = json.load(json_file)
#
#     # Analyze domain relationships
#     domain_graph = analyze_domain_relationships(province_data)
#
#     # Plot the domain relationships graph
#     plot_graph(domain_graph)
#
#     # Perform advanced analysis
#     analyze_advanced(domain_graph)

import json
from urllib.parse import urlparse
import os
import networkx as nx
import matplotlib.pyplot as plt

def analyze_domain_relationships(province_data):
    province_graphs = {}

    for province_info in province_data:
        G = nx.Graph()
        domain_counts = {}

        # Collect unique domains from all links
        unique_domains = set()
        for site_info in province_info['sites']:
            for link_type in ['internal_links', 'external_links', 'potential_threat_links']:
                for link in site_info[link_type]:
                    linked_domain = urlparse(link).netloc
                    unique_domains.add(linked_domain)

        # Add nodes based on unique domains with initial weight set to 0
        for domain in unique_domains:
            G.add_node(domain, weight=0)

        # Add edges based on all links for the current site
        for site_info in province_info['sites']:
            site_url = site_info['url']

            # Update domain counts based on the current site's domain
            domain = urlparse(site_url).netloc
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

            # Update the weight of the node if it exists
            if domain in G.nodes:
                G.nodes[domain]['weight'] += domain_counts[domain]

            # Add edges based on all links for the current site
            for link_type in ['internal_links', 'external_links', 'potential_threat_links']:
                for link in site_info[link_type]:
                    linked_domain = urlparse(link).netloc

                    if linked_domain != domain:
                        # Update the weight of the linked_domain node if it exists
                        if linked_domain in G.nodes:
                            G.nodes[linked_domain]['weight'] += 1
                            # Add the edge between domain and linked_domain
                            G.add_edge(domain, linked_domain)

        province_graphs[province_info['province']] = G

    return province_graphs


def plot_province_graph(graph, province_name, output_dir):
    pos = nx.kamada_kawai_layout(graph)
    degree_centrality = nx.degree_centrality(graph)
    top_nodes = sorted(degree_centrality.keys(), key=lambda x: degree_centrality[x], reverse=True)[:100]
    subgraph = graph.subgraph(top_nodes)

    node_sizes = [100 * degree_centrality[node] for node in subgraph.nodes]
    node_colors = ['lightcoral' if '.gov.cn' in node else 'skyblue' for node in subgraph.nodes]

    # Retrieve edge weights directly from the graph's edge attributes
    edge_weights = [subgraph.nodes[v]['weight'] for u, v in subgraph.edges]

    # Use the edge weights for coloring edges
    edge_colors = plt.cm.viridis(edge_weights)

    # Plot the domain relationships graph for each province and save it
    plt.figure(figsize=(15, 15), dpi=500)
    nx.draw(subgraph, pos, node_size=node_sizes, node_color=node_colors, edge_color=edge_colors,
            width=2, alpha=0.7, with_labels=True, font_size=8)

    # Add a colorbar for edge weights
    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=min(edge_weights), vmax=max(edge_weights)))
    sm.set_array([])
    cbar = plt.colorbar(sm, orientation='vertical')
    cbar.set_label('Edge Weights')

    plt.title(f"Domain Relationships - {province_name}")
    plt.axis('off')
    plt.savefig(os.path.join(output_dir, f"{province_name}_domain_relationships_advanced.png"))
    plt.show()
    plt.close()


if __name__ == "__main__":
    # Load province_data from the saved JSON file
    with open('province_data.json', 'r', encoding='utf-8') as json_file:
        province_data = json.load(json_file)

    # Create the "webpage_result" directory if it doesn't exist
    output_directory = 'webpage_result'
    os.makedirs(output_directory, exist_ok=True)

    # Analyze domain relationships per province
    province_graphs = analyze_domain_relationships(province_data)

    # Perform advanced analysis per province and save results
    for province_name, graph in province_graphs.items():
        plot_province_graph(graph, province_name, output_directory)

    print("\nResults saved in the 'webpage_result' directory.")




# def plot_province_graph(graph, province_name, output_dir):
#     pos = nx.spring_layout(graph, seed=42)  # Seed for reproducibility
#
#     # Calculate centrality measures
#     degree_centrality = nx.degree_centrality(graph)
#     top_nodes = sorted(degree_centrality.keys(), key=lambda x: degree_centrality[x], reverse=True)[:100]
#
#     # Create a subgraph with the top 100 nodes and their edges
#     subgraph = graph.subgraph(top_nodes)
#
#     # Set node sizes based on the 'weight' attribute
#     node_sizes = [graph.nodes[node].get('weight', 0) * 1000 for node in subgraph.nodes]
#
#     # Assign different colors for '.gov.cn' and other domains
#     node_colors = ['lightcoral' if '.gov.cn' in node else 'skyblue' for node in subgraph.nodes]
#
#     # Extract domain names for labeling
#     node_labels = {node: urlparse(node).netloc for node in subgraph.nodes}
#
#     plt.figure(figsize=(15, 15), dpi=500)
#     nx.draw_networkx_nodes(subgraph, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
#     nx.draw_networkx_edges(subgraph, pos, edge_color='gray', alpha=0.5)
#     nx.draw_networkx_labels(subgraph, pos, labels=node_labels, font_size=10, font_color='black')
#
#     plt.title(f"Domain Relationships - {province_name}")
#     plt.axis('off')
#
#     # Save the plot to the "webpage_result" directory
#     output_path = os.path.join(output_dir, f"{province_name}_domain_relationships.png")
#     plt.savefig(output_path)
#     plt.close()
