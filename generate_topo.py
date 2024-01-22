import json
from urllib.parse import urlparse
import os
import networkx as nx
import matplotlib.pyplot as plt

# 中文地名及机构到英文的映射字典
location_translation_dict = {
    "上海市": "Shanghai",
    "重庆市": "Chongqing",
    "陕西省": "Shaanxi",
    "青海省": "Qinghai",
    "黑龙江省": "Heilongjiang",
    "云南省": "Yunnan",
    "北京市": "Beijing",
    "吉林省": "Jilin",
    "四川省": "Sichuan",
    "天津市": "Tianjin",
    "宁夏回族自治区": "Ningxia",
    "内蒙古自治区": "Inner Mongolia",
    "安徽省": "Anhui",
    "山东省": "Shandong",
    "山西省": "Shanxi",
    "广东省": "Guangdong",
    "江苏省": "Jiangsu",
    "江西省": "Jiangxi",
    "河北省": "Hebei",
    "河南省": "Henan",
    "浙江省": "Zhejiang",
    "海南省": "Hainan",
    "湖北省": "Hubei",
    "湖南省": "Hunan",
    "甘肃省": "Gansu",
    "福建省": "Fujian",
    "贵州省": "Guizhou",
    "辽宁省": "Liaoning",
    "广西壮族自治区": "Guangxi",
    "新疆生产建设兵团": "Xinjiang Production and Construction Corps",
    "新疆维吾尔自治区": "Xinjiang Uygur Autonomous Region",
    "省级门户": "Provincial Government Portal",
    "部委门户": "Government Department Portal",
    "国务院部门所属网站": "State Council",
    "西藏自治区": "Tibet",
}


def analyze_domain_relationships(province_data):
    province_graphs = {}

    for province_info in province_data:
        G = nx.Graph()
        domain_counts = {}

        # Collect unique domains from all links
        unique_domains = set()
        for site_info in province_info['sites']:
            for link_type in ['internal_links', 'external_links']:
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
            for link_type in ['internal_links', 'external_links']:
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


# def plot_province_graph(graph, province_name, output_dir):
#     # pos = nx.kamada_kawai_layout(graph)
#     pos = nx.circular_layout(graph)
#     degree_centrality = nx.degree_centrality(graph)
#     top_nodes = sorted(degree_centrality.keys(), key=lambda x: degree_centrality[x], reverse=True)[:50]
#     subgraph = graph.subgraph(top_nodes)
#
#     node_sizes = [300 * degree_centrality[node] for node in subgraph.nodes]
#     node_colors = ['lightcoral' if '.gov.cn' in node else 'skyblue' for node in subgraph.nodes]
#
#     # Retrieve edge weights directly from the graph's edge attributes
#     edge_weights = [subgraph.nodes[v]['weight'] for u, v in subgraph.edges]
#
#     # Use the edge weights for coloring edges
#     edge_colors = plt.cm.viridis(edge_weights)
#
#     # Plot the domain relationships graph for each province and save it
#     plt.figure(figsize=(15, 15), dpi=500)
#     nx.draw(subgraph, pos, node_size=node_sizes, node_color=node_colors, edge_color=edge_colors,
#             width=2, alpha=0.7, with_labels=True, font_size=18)
#
#     # Add a colorbar for edge weights
#     sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=min(edge_weights), vmax=max(edge_weights)))
#     sm.set_array([])
#     cbar = plt.colorbar(sm, orientation='vertical')
#     cbar.set_label('Edge Weights')
#
#     plt.title(f"Domain Relationships - {province_name}")
#     plt.axis('off')
#     plt.savefig(os.path.join(output_dir, f"{province_name}_domain_relationships_advanced.png"))
#     plt.show()
#     plt.close()


# def plot_province_graph(graph, province_name, output_dir):
#     pos = nx.spring_layout(graph, seed=42)  # Seed for reproducibility
#
#     # Calculate centrality measures
#     degree_centrality = nx.degree_centrality(graph)
#     top_nodes = sorted(degree_centrality.keys(), key=lambda x: degree_centrality[x], reverse=True)[:50]
#
#     # Create a subgraph with the top 100 nodes and their edges
#     subgraph = graph.subgraph(top_nodes)
#
#     # Set node sizes based on the 'weight' attribute
#     node_sizes = [graph.nodes[node].get('weight', 0) * 10 for node in subgraph.nodes]
#
#     # Assign different colors for '.gov.cn' and other domains
#     node_colors = ['lightcoral' if '.gov.cn' in node else 'skyblue' for node in subgraph.nodes]
#
#     # Extract domain names for labeling
#     node_labels = {node: node for node in subgraph.nodes}
#
#     plt.figure(figsize=(15, 15), dpi=500)
#     nx.draw_networkx_nodes(subgraph, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
#     nx.draw_networkx_edges(subgraph, pos, edge_color='gray', alpha=0.5)
#     nx.draw_networkx_labels(subgraph, pos, labels=node_labels, font_size=10, font_color='black')
#
#     plt.title(f"Domain Relationships - {location_translation_dict.get(province_name,  'Unknown')}")
#     plt.axis('off')
#
#     # Save the plot to the "webpage_result" directory
#     output_path = os.path.join(output_dir, f"{province_name}_domain_relationships.png")
#     plt.savefig(output_path)
#     plt.close()
#

import plotly.graph_objects as go


def plot_province_graph(graph, province_name, output_dir):
    pos = nx.kamada_kawai_layout(graph)  # Seed for reproducibility

    # Calculate centrality measures
    degree_centrality = nx.degree_centrality(graph)
    top_nodes = sorted(degree_centrality.keys(), key=lambda x: degree_centrality[x], reverse=True)[:50]

    # Create a subgraph with the top 100 nodes and their edges
    subgraph = graph.subgraph(top_nodes)

    # Set node sizes based on the 'weight' attribute
    node_sizes = [graph.nodes[node].get('weight', 0) * 1 for node in subgraph.nodes]

    # Assign different colors for '.gov.cn' and other domains
    node_colors = ['lightcoral' if '.gov.cn' in node else 'skyblue' for node in subgraph.nodes]

    # Extract domain names for labeling
    node_labels = {node: node for node in subgraph.nodes}

    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in subgraph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=node_sizes,  # Set the node sizes here
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            color=node_colors  # Set the node colors here
        )
    )

    for node in subgraph.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['text'] += (node_labels[node],)

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # Save the plot to the "webpage_result" directory
    output_path = os.path.join(output_dir, f"{province_name}_domain_relationships_interactive.html")
    fig.write_html(output_path)


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
