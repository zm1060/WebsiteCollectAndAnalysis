
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 设置字体
plt.rcParams['font.sans-serif'] = 'SimHei'

# 创建有向图
G = nx.DiGraph()

# 添加节点
nodes = ['北京', '上海', '广州', '深圳', '成都', '重庆', '杭州', '武汉', '南京']
G.add_nodes_from(nodes)

# 添加边（省份之间的关系）
edges = [('北京', '上海'), ('北京', '广州'), ('上海', '深圳'),
         ('上海', '南京'), ('广州', '深圳'), ('广州', '杭州'),
         ('深圳', '成都'), ('成都', '重庆'), ('成都', '武汉'),
         ('重庆', '武汉'), ('重庆', '南京'), ('杭州', '南京')]
G.add_edges_from(edges)

# 绘制图形
plt.figure(figsize=(10, 8))  # 调整图形大小
pos = nx.spring_layout(G, k=0.3, iterations=20)  # 调整布局算法参数
nx.draw_networkx(G, pos, with_labels=False, node_color='lightblue', node_size=800, edge_color='gray', arrowsize=12)

# 绘制节点的出度和入度
out_degrees = G.out_degree()
in_degrees = G.in_degree()
node_sizes_out = [2000 * out_degrees[node] for node in G.nodes()]
node_sizes_in = [2000 * in_degrees[node] for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=node_sizes_out, alpha=0.7)
nx.draw_networkx_nodes(G, pos, node_color='pink', node_size=node_sizes_in, alpha=0.7)

# 添加节点标签
labels = {node: node for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=10, font_family='SimHei')

# 显示图形
plt.axis('off')
plt.show()

# 输出节点的出度和入度信息
print("节点的出度：", out_degrees)
print("节点的入度：", in_degrees)