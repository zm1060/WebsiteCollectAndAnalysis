import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data
from py2neo import Graph

# 连接Neo4j
graph_db = Graph("neo4j://localhost:7687", auth=("neo4j", "password"))

# 查询获取节点特征和标签的信息
query = """
MATCH (a)
OPTIONAL MATCH (a)-[:HAS_SOLUTION]->(s:Solution)
OPTIONAL MATCH (a)-[:HAS_REFERENCE]->(r:Reference)
WHERE a.alert IS NOT NULL AND a.riskcode IS NOT NULL AND a.confidence IS NOT NULL 
RETURN id(a) as node_id, a.alert as alert, a.riskcode as riskcode, 
       a.confidence as confidence, coalesce(s.solution, "") as solution, coalesce(r.reference, "") as reference
"""

results = graph_db.run(query).data()

# 提取节点特征和标签的信息
node_features = []
node_labels = []


def hash_string(s):
    return hash(s)


for result in results:
    # 需要进一步处理和编码特征
    features = [
        0 if result['alert'] is None else hash_string(result['alert']),
        0 if result['riskcode'] is None else result['riskcode'],
        0 if result['confidence'] is None else result['confidence'],
        0 if result['solution'] is None else hash_string(result['solution']),
        0 if result['reference'] is None else hash_string(result['reference'])
    ]
    label = 0 if result['confidence'] is None else result['confidence']  # 假设我们使用confidence作为标签

    node_features.append(features)
    node_labels.append(label)

# 将节点特征和标签转换为PyTorch张量
# 这可能需要进一步处理，特别是如果特征是分类或文本数据
x = torch.tensor(node_features, dtype=torch.float32)
y = torch.tensor(node_labels, dtype=torch.long)

# 查询获取边的信息
query_edges = """
MATCH (a)-[r]->(b)
RETURN id(a) as source_id, id(b) as target_id
"""

edges_results = graph_db.run(query_edges).data()

edges = [(res['source_id'], res['target_id']) for res in edges_results]
edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

# 创建PyTorch Geometric数据对象
data = Data(x=x, edge_index=edge_index, y=y)


# 创建和训练模型

class GCNModel(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super(GCNModel, self).__init__()
        self.conv1 = GCNConv(num_features, 16)
        self.conv2 = GCNConv(16, num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)

        x = self.conv2(x, edge_index)

        return F.log_softmax(x, dim=1)


print(data)
# 初始化模型
num_features = data.x.size(1)
num_classes = 2  # 或者根据你的数据设置
model = GCNModel(num_features, num_classes)

# 定义损失函数和优化器
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 训练模型
model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data)
    loss = criterion(out, data.y)
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f'Epoch: {epoch}, Loss: {loss.item()}')

# 评估模型
model.eval()
_, pred = model(data).max(dim=1)
correct = float(pred[data.y == data.y].sum().item())
accuracy = correct / data.y.size(0)
print(f'Accuracy: {accuracy:.4f}')
