import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 读取 CSV 文件
df = pd.read_csv("output_nameserver.csv")

# 提取 Count 列作为特征向量
features = df["Count"].values.reshape(-1, 1)

# 归一化特征向量
scaler = StandardScaler()
features_normalized = scaler.fit_transform(features)

# 定义 k-means 模型并进行聚类
k = 6  # 设置聚类数目
kmeans = KMeans(n_clusters=k, random_state=42)
df["Cluster"] = kmeans.fit_predict(features_normalized)
df.rename(columns={"Second and Top Level Domain": "Domain"}, inplace=True)

# 输出聚类结果
for clusterIndex, group in df.groupby("Cluster"):
    print(f"Cluster {clusterIndex}:\n{group['Domain'].tolist()}\n")
