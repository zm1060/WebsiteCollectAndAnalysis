from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.azure.storage import StorsimpleDataManagers
from diagrams.generic.network import Firewall
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.compute import Server
from diagrams.aws.general import Users
from diagrams.aws.security import RAM
from diagrams.gcp.operations import Monitoring
from diagrams.aws.analytics import Analytics
from diagrams.azure.analytics import StreamAnalyticsJobs
from diagrams.ibm.applications import Visualization
from diagrams.azure.general import Managementgroups
from diagrams.azure.network import ApplicationGateway
from diagrams.azure.web import AppServices

with Diagram("可视化系统管理与展示功能设计", show=False, direction='TB'):
    # 用户通过前端界面发起请求
    with Cluster("用户交互"):
        user = Users("用户")
        frontend = AppServices("前端")
        user >> frontend

    # 前端处理模块将请求发送给后端服务
    with Cluster("前端处理"):
        frontend_processing = ApplicationGateway("前端处理")
        frontend << Edge() >> frontend_processing

    # 所有服务模块共用一个数据库集群
    with Cluster("数据库"):
        database = [RDS("DB1"),RDS("DB2")]

    # 后端服务根据请求调用相应的模块
    with Cluster("后端服务"):
        backend = Server("后端")
        frontend_processing << Edge() >> backend

        # 数据存储模块负责存储大规模域名解析服务的数据
        with Cluster("数据存储模块"):
            data_storage = StorsimpleDataManagers("数据存储")
            backend << Edge() >> data_storage
            data_storage << Edge() >> database

        # 数据管理模块处理用户对数据的管理请求，更新数据库中的数据
        with Cluster("数据管理模块"):
            data_management = Managementgroups("数据管理")
            backend << Edge() >> data_management
            data_management << Edge() >> data_storage

        # 数据分析模块从数据库中提取数据，进行分析，生成图表数据
        with Cluster("数据分析模块"):
            data_analysis = Analytics("数据分析")
            backend >> data_analysis
            data_analysis << Edge() >> data_storage

        # 可视化模块接收图表数据，设计并展示可视化图表
        with Cluster("可视化模块"):
            visualization = Visualization("可视化")
            visualization << Edge() >> backend

        # 实时更新模块定期或实时采集DNS数据，更新数据库
        with Cluster("实时更新模块"):
            real_time_update = StreamAnalyticsJobs("实时更新")
            backend >> real_time_update
            real_time_update >> data_storage

        # 安全性与权限控制模块验证用户身份和权限
        with Cluster("安全性与权限控制模块"):
            security_control = RAM("安全控制")
            backend >> security_control
            security_control >> Firewall("防火墙")

        # 通知与报警模块监测系统运行状态，发现异常时触发通知
        with Cluster("通知与报警模块"):
            notification_alert = Monitoring("通知和报警")
            notification_alert << Edge() >> backend
    # 系统整体
    user >> frontend
