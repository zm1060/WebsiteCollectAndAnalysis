from diagrams import Diagram, Cluster, Edge
from diagrams.aws.security import RAM
from diagrams.azure.web import AppServices
from diagrams.ibm.management import ClusterManagement
from diagrams.onprem.client import Users
from diagrams.onprem.network import Internet
from diagrams.gcp.operations import Monitoring
from diagrams.programming.framework import Flask
from diagrams.aws.database import RDS
from diagrams.onprem.compute import Server
from diagrams.alibabacloud.network import Cdn
from diagrams.gcp.network import DNS
from diagrams.azure.analytics import AnalysisServices, StreamAnalyticsJobs
from diagrams.azure.general import Resourcegroups, Managementgroups
from diagrams.azure.integration import EventGridTopics

with Diagram(
    "可视化系统管理与展示功能设计",
    show=True,
    direction='TB',
    filename="diagram",
    outformat="png",
    graph_attr={"width": "8000", "height": "6000"},
    node_attr={"fontsize": "25", "fontname":"Microsoft YaHei"},
    edge_attr={"fontsize": "25", "fontname":"Microsoft YaHei"}
):


    internet = Internet("Internet")
    backend = Server("后端服务")

    with Cluster("数据库"):
        database = RDS("数据库")
        backend >> Edge(label="Query/Update", style="dashed") >> database


    # 可视化与管理模块
    with Cluster("可视化与管理"):
        frontend = AppServices("前端")

        frontend >> Edge(label="HTTP Request", style="dashed") >> internet

        internet >> Edge(label="HTTP Response", style="dashed") >> frontend



        with Cluster("可视化管理模块"):
            policy = EventGridTopics("策略管理")
            domain = Resourcegroups("域名管理")
            data_management = Managementgroups("数据管理")
            security_and_permissions = RAM("安全性和权限控制")

            backend >> policy
            backend >> domain
            backend >> data_management
            backend >> security_and_permissions
        with Cluster("可视化展示模块"):
            overview = Cdn("全局概览")
            server_map = DNS("服务器地图")
            statistics = AnalysisServices("分类统计")
            monitoring = Monitoring("解析结果监测")
            real_time_updates = StreamAnalyticsJobs("实时更新")

            backend >> overview
            backend >> server_map
            backend >> statistics
            backend >> monitoring
            backend >> real_time_updates
    # 用户通过前端界面发起请求
    with Cluster("用户交互"):
        user = Users("用户")

        user >> frontend
    backend >> Edge(label="RESTful API", style="dashed") >> frontend
