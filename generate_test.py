from diagrams import Diagram, Cluster, Edge

with Diagram("全局概览子模块", show=True):
    # 定义节点
    global_overview = Cluster("全局概览子模块")

    linkage_effect = Diagram("联动效果")
    navigation = Diagram("导航功能")
    timeline = Diagram("时间轴功能")
    health_indicator = Diagram("系统总体健康状况指示灯")
    dns_distribution_map = Diagram("全球DNS服务器分布地图")
    survival_trend_chart = Diagram("存活率趋势图")
    coverage_statistics = Diagram("探测覆盖率统计")

    # 连接节点
    global_overview >> Edge() >> linkage_effect
    global_overview >> Edge() >> timeline
    global_overview >> Edge() >> health_indicator
    global_overview >> Edge() >> dns_distribution_map
    global_overview >> Edge() >> survival_trend_chart
    global_overview >> Edge() >> coverage_statistics

    # 描述各个子模块的关系
    linkage_effect >> Edge("通过仪表板上的联动功能") >> navigation
    navigation >> Edge("从全局视图到具体细节") >> timeline
    timeline >> Edge("用于解析结果监测") >> health_indicator
    dns_distribution_map >> Edge("通过交互式地图展示") >> survival_trend_chart
    survival_trend_chart >> Edge("帮助用户追踪变化趋势") >> coverage_statistics
