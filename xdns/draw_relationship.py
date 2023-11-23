import os
import pickle
import re

import mpldatacursor
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import plotly.graph_objects as go

response_dir = './class'  # response目录路径

# Step 2: 绘制关系图
graph = nx.DiGraph()  # 创建有向图对象
external_links = set()  # 存储外部链接
govcn_links = set()  # 存储.gov.cn链接

# Set the font properties for displaying Chinese characters
font_path = '../SimHei.ttf'  # Replace with the path to a Chinese font file (.ttf)
font_prop = FontProperties(fname=font_path)

# ToDO
# 使用 Apache Spark Graphx
# 遍历每个单位目录

# 遍历每个单位目录
for unit_dir in os.listdir(response_dir):
    unit_path = os.path.join(response_dir, unit_dir)
    unit_name = unit_dir

    graph_filename = os.path.join('graph_result', f"{unit_name}.pkl")
    if os.path.exists(graph_filename):
        # 如果文件存在，直接加载图对象并进行绘制
        with open(graph_filename, 'rb') as file:
            graph = pickle.load(file)
    else:
        # 确保当前项是一个目录
        if os.path.isdir(unit_path):
            # 遍历单位目录中的txt文件
            for file_name in os.listdir(unit_path):
                file_path = os.path.join(unit_path, file_name)
                existing_node = file_name.split('.txt')[0]
                # 确保当前项是一个文件
                if os.path.isfile(file_path):
                    if file_name.endswith('.txt'):
                        file_path = os.path.normpath(file_path)  # Normalize the path

                        with open(file_path, 'r', encoding='utf-8') as file:
                            # 读取文件中的链接列表
                            links = re.findall(
                                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                file.read())
                            # print(links)
                            # 处理链接并添加节点到关系图
                            for url in links:
                                url_match = re.search(r"https?://([^/?]+)", url)
                                if url_match:
                                    url_domain = url_match.group(1)
                                    url_path = url.split('/', 3)[-1]  # Extract the path after the domain
                                    # domain_with_path = f"{url_domain}/{url_path}"
                                    # Add an edge to the graph connecting the domain to the home page URL
                                    if url_domain.endswith('.gov.cn'):
                                        govcn_links.add(url_domain)  # 添加.gov.cn链接到集合
                                        graph.add_node(url_domain, type='govcn')  # 添加.gov.cn链接节点
                                    else:
                                        external_links.add(url_domain)  # 添加外部链接到集合
                                        graph.add_node(url_domain, type='external')  # 添加外部链接节点
                                    graph.add_edge(existing_node, url_domain)  # 连接现有节点和链接节点
    # Calculate the in-degree and out-degree centrality measures
    in_degree_centrality = nx.in_degree_centrality(graph)
    out_degree_centrality = nx.out_degree_centrality(graph)

    # Sort the nodes by out-degree centrality and select the top 10 nodes
    sorted_nodes = sorted(graph.nodes(), key=out_degree_centrality.get, reverse=True)[:20]

    # Create a subgraph with the top 10 nodes
    subgraph = graph.subgraph(sorted_nodes)

    # Draw the graph with node sizes based on the in-degree and out-degree centrality
    pos = nx.spring_layout(subgraph)
    node_size = [10000 * in_degree_centrality[node] for node in subgraph.nodes()]
    node_color = [out_degree_centrality[node] for node in subgraph.nodes()]
    # clustering_coefficients = nx.clustering(graph)
    # betweenness_centralities = nx.betweenness_centrality(graph)
    # # 接下来的步骤和您之前的绘图逻辑一样
    # # 排序节点根据介数中心系数，而不是出度中心性
    # sorted_nodes = sorted(graph.nodes(), key=betweenness_centralities.get, reverse=True)[:50]
    # subgraph = graph.subgraph(sorted_nodes)
    # pos = nx.spring_layout(subgraph)
    # # 使用介数中心系数和聚集系数调整节点大小
    # node_size = [
    #     5000 * (clustering_coefficients[node] + betweenness_centralities[node])
    #     for node in subgraph.nodes()
    # ]

    # node_color = ['red' if node in govcn_links else 'green' for node in subgraph.nodes()]
    plt.figure(figsize=(12, 12), dpi=800)
    nx.draw_networkx(
        subgraph,
        pos=pos,
        with_labels=True,
        node_size=node_size,
        node_color=node_color,
        cmap=plt.cm.Blues,
        alpha=0.7,
        font_size=8,
        font_color="black",
        edge_color="black",
        width=0.2,
    )

    plt.title(f"Home Page Relationship Diagram - {unit_name}", fontproperties=font_prop)
    plt.axis("off")
    # Create the subdirectory for the output PNG file if it doesn't exist
    os.makedirs('relationship_result', exist_ok=True)
    # Save the diagram as PNG in the subdirectory with the same name as the subdirectory
    output_filename = os.path.join('relationship_result', f"{unit_name}.png")
    plt.savefig(output_filename, dpi=800)

    os.makedirs('graph_result', exist_ok=True)
    graph_filename = os.path.join('graph_result', f"{unit_name}.pkl")
    with open(graph_filename, 'wb') as file:
        pickle.dump(graph, file)
    graph.clear()

#
#     # Create lists to store node and edge trace data
#     node_trace = go.Scatter(
#         x=[pos[node][0] for node in subgraph.nodes()],
#         y=[pos[node][1] for node in subgraph.nodes()],
#         text=[node for node in subgraph.nodes()],
#         mode='markers',
#         hoverinfo='text',
#         marker=dict(
#             size=[10000 * in_degree_centrality[node] for node in subgraph.nodes()],
#             color=['red' if node in govcn_links else 'green' for node in subgraph.nodes()],
#         )
#     )
#
#     edge_trace = go.Scatter(
#         x=[pos[edge[0]][0] for edge in subgraph.edges()],
#         y=[pos[edge[0]][1] for edge in subgraph.edges()],
#         line=dict(width=0.5, color='gray'),
#         hoverinfo='none',
#         mode='lines'
#     )
#
#     # Create the figure and add the traces
#     fig = go.Figure(data=[edge_trace, node_trace])
#
#     # Customize theApologies for the incomplete response. Here's the continuation of the code:
#
#     # Customize the layout
#     fig.update_layout(
#         title=f"Home Page Relationship Diagram - {unit_name}",
#         showlegend=False,
#         hovermode='closest',
#         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#         font=dict(family=font_path),
#     )
#
#     # Show the interactive plot in a web browser
#     fig.show()
