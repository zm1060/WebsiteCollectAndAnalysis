import networkx as nx
import matplotlib.pyplot as plt

# 创建有向图
G = nx.DiGraph()
G.add_edges_from([(1, 2), (1, 3), (2, 1), (3, 2), (3, 4), (4, 1)])

# 设置初始PageRank值
initial_pagerank = {node: 1 / G.number_of_nodes() for node in G.nodes}

# 存储每一步的PageRank值
pagerank_values = [initial_pagerank]

# 运行PageRank算法，迭代10次
for _ in range(10):
    new_pagerank = {}
    for node in G.nodes:
        new_pagerank[node] = 0.15 / G.number_of_nodes() + 0.85 * sum(
            pagerank_values[-1][neighbor] / G.out_degree(neighbor)
            for neighbor in G.predecessors(node)
        )
    pagerank_values.append(new_pagerank)

# 保存每一步的图形
for i, pagerank in enumerate(pagerank_values):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))

    current_node = max(pagerank, key=pagerank.get)  # 选择PageRank值最高的节点作为当前节点
    neighbors = list(G.neighbors(current_node))

    # 绘制图形
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='skyblue', font_color='black')

    nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='red')
    nx.draw_networkx_labels(G, pos, labels={current_node: current_node}, font_color='red', font_size=12)

    for neighbor in neighbors:
        nx.draw_networkx_nodes(G, pos, nodelist=[neighbor], node_color='green')
        nx.draw_networkx_labels(G, pos, labels={neighbor: neighbor}, font_color='green', font_size=12)

    plt.title(f'PageRank Iteration {i + 1}')
    plt.savefig(f'pagerank_iteration_{i + 1}.png')
    plt.close()
