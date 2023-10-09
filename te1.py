import matplotlib.pyplot as plt
import networkx as nx

# 创建一个有向图
G = nx.DiGraph()

# 添加节点和边
G.add_nodes_from(['总体统计', '境内外服务器数量统计', '时延分类雷达图', '功能分类饼图', '加密协议分布图',
                  '境内', '境外', '时延分类', '功能分类', '加密协议',
                  '柱状图', '饼图', '雷达图', '分布图'])

G.add_edges_from([('总体统计', '境内外服务器数量统计'), ('总体统计', '时延分类雷达图'), ('总体统计', '功能分类饼图'), ('总体统计', '加密协议分布图'),
                  ('境内外服务器数量统计', '境内'), ('境内外服务器数量统计', '境外'), ('时延分类雷达图', '时延分类'), ('功能分类饼图', '功能分类'),
                  ('加密协议分布图', '加密协议'), ('境内', '柱状图'), ('境外', '柱状图'), ('时延分类', '雷达图'), ('功能分类', '饼图'),
                  ('加密协议', '分布图')])

# 绘制图
pos = nx.spring_layout(G, seed=42)  # 设定seed以保证每次运行的布局一致
nx.draw(G, pos, with_labels=True, font_size=8, node_size=2000, node_color='lightblue', font_weight='bold', arrowsize=20)

plt.title('功能关系图')
plt.show()
