# 在目录response下，有很多以省名和单位名的目录，在这些目录下包括了一些域名.txt的文件，这些文件是使用python requests获取的response。
# 忽略文件中的内链，依据出度和入度，绘制全国各省市关系图，在中国地图上画出位置节点。分析哪些类型的节点较为重要。使用python实现。
import json
import os
import re
import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Step 1: 数据准备
response_dir = './class'  # response目录路径

# Step 2: 绘制关系图
graph = nx.DiGraph()  # 创建有向图对象
external_links = set()  # 存储外部链接
govcn_links = set()  # 存储.gov.cn链接

# Set the font properties for displaying Chinese characters
font_path = '../SimHei.ttf'  # Replace with the path to a Chinese font file (.ttf)
font_prop = FontProperties(fname=font_path)

# 遍历每个单位目录
for unit_dir in os.listdir(response_dir):
    unit_path = os.path.join(response_dir, unit_dir)
    unit_name = unit_dir
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
                        print(external_links)
    # Calculate the in-degree and out-degree centrality measures
    in_degree_centrality = nx.in_degree_centrality(graph)
    out_degree_centrality = nx.out_degree_centrality(graph)
    # Sort the nodes by out-degree centrality and select the top 20 nodes
    sorted_nodes = sorted(graph.nodes(), key=in_degree_centrality.get, reverse=True)[:20]
    # Create a subgraph with the top 20 nodes
    subgraph = graph.subgraph(sorted_nodes)
    # Draw the graph with node sizes based on the in-degree and out-degree centrality
    pos = nx.spring_layout(subgraph)
    node_size = [10000 * in_degree_centrality[node] for node in subgraph.nodes()]
    node_color = ['red' if node in govcn_links else 'green' for node in subgraph.nodes()]
    plt.figure(figsize=(12, 8), dpi=300)
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
        edge_color="gray",
        width=0.2,
    )

    plt.title(f"Home Page Relationship Diagram - {unit_name}", fontproperties=font_prop)
    plt.axis("off")
    # Create the subdirectory for the output PNG file if it doesn't exist
    os.makedirs('relationship_result', exist_ok=True)
    # Save the diagram as PNG in the subdirectory with the same name as the subdirectory
    output_filename = os.path.join('relationship_result', f"{unit_name}.png")
    plt.savefig(output_filename, dpi=300)
    graph.clear()
# Step 3: 绘制位置节点

# 获取每个省市的经纬度信息
# ...

# 使用Basemap或Geopandas绘制中国地图
# ...

# 在地图上添加位置节点
# ...

# Step 4: 分析节点重要性

# 计算节点的重要性指标
# ...

# 分析节点重要性
# ...

# 显示关系图和地图

