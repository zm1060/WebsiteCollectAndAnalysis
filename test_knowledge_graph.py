import json

from py2neo import Graph, Node, Relationship

# 连接到Neo4j数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# 从文件中加载JSON报告
with open('ZAP_Result.json', 'r', encoding='utf-8') as report_file:
    zap_report = json.load(report_file)

json_data = zap_report

# 创建程序节点
program_node = Node("Program", name=json_data["@programName"], version=json_data["@version"])
graph.create(program_node)

# 遍历站点信息并创建站点节点以及站点和程序之间的关系
for site_data in json_data["site"]:
    site_node = Node("Site", name=site_data["@name"], host=site_data["@host"], port=site_data["@port"],
                     ssl=site_data["@ssl"])
    exists_in_program_relation = Relationship(program_node, "EXISTS_IN", site_node)
    graph.create(site_node)
    graph.create(exists_in_program_relation)

    # 遍历站点的漏洞信息并创建漏洞节点以及站点和漏洞之间的关系
    for alert_data in site_data.get("alerts", []):
        alert_node = Node(
            alert=alert_data.get("alert", ""),
            alertRef=alert_data.get("alertRef", ""),
            riskcode=alert_data.get("riskcode", ""),
            confidence=alert_data.get("confidence", ""),
            count=alert_data.get("count", ""),
            riskdesc=alert_data.get("riskdesc", ""),
            desc=alert_data.get("desc", ""),
            cweid=alert_data.get("cweid", ""),
            wascid=alert_data.get("wascid", ""),
            sourceid=alert_data.get("sourceid", "")
        )
        exists_in_site_relation = Relationship(site_node, "HAS_ALERT", alert_node)
        graph.create(alert_node)
        graph.create(exists_in_site_relation)

        # 添加漏洞节点与解决方案之间的关系（示例关系）
        if alert_data.get("solution"):
            solution_node = Node(
                "Solution",
                solution=alert_data["solution"]
            )
            has_solution_relation = Relationship(alert_node, "HAS_SOLUTION", solution_node)
            graph.create(solution_node)
            graph.create(has_solution_relation)

        # 添加漏洞节点与参考信息之间的关系（示例关系）
        if alert_data.get("reference"):
            reference_node = Node(
                "Reference",
                reference=alert_data["reference"]
            )
            has_reference_relation = Relationship(alert_node, "HAS_REFERENCE", reference_node)
            graph.create(reference_node)
            graph.create(has_reference_relation)

        # 添加漏洞节点与其他信息之间的关系（示例关系）
        if alert_data.get("otherinfo"):
            otherinfo_node = Node(
                "OtherInfo",
                otherinfo=alert_data["otherinfo"]
            )
            has_otherinfo_relation = Relationship(alert_node, "HAS_OTHERINFO", otherinfo_node)
            graph.create(otherinfo_node)
            graph.create(has_otherinfo_relation)

        for instance_data in alert_data.get("instances", []):
            instances_node = Node(
                "Instances",
                uri=instance_data.get("uri", ""),
                method=instance_data.get("method", ""),
                param=instance_data.get("param", ""),
                otherinfo=instance_data.get("otherinfo", "")
            )
            has_instance_relation = Relationship(alert_node, "HAS_INSTANCES", instances_node)
            graph.create(instances_node)
            graph.create(has_instance_relation)

            if instance_data.get("evidence"):
                evidence_node = Node(
                    "Evidence",
                    evidence=instance_data.get("evidence", "")
                )
                has_evidence_relation = Relationship(instances_node, "HAS_EVIDENCE", evidence_node)
                graph.create(evidence_node)
                graph.create(has_evidence_relation)



#
#
# import json
# from py2neo import Graph, Node, Relationship
#
# # 连接到Neo4j数据库
# graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
#
# # 从文件中加载JSON报告
# with open('Guizhou.json', 'r', encoding='utf-8') as report_file:
#     zap_report = json.load(report_file)
#
# json_data = zap_report
#
# # 创建程序节点
# if "@programName" in json_data and "@version" in json_data:
#     program_node = Node("Program", name=json_data["@programName"], version=json_data["@version"])
#     graph.merge(program_node, "Program", "name")
#
#     for site_data in json_data.get("site", []):
#         if all(k in site_data for k in ["@name", "@host", "@port", "@ssl"]):
#             site_node = Node("Site",
#                              name=site_data["@name"],
#                              host=site_data["@host"],
#                              port=site_data["@port"],
#                              ssl=site_data["@ssl"])
#             graph.merge(site_node, "Site", "name")
#             exists_in_program_relation = Relationship(program_node, "EXISTS_IN", site_node)
#             graph.merge(exists_in_program_relation)
#
#             for alert_data in site_data.get("alerts", []):
#                 if "alert" in alert_data:
#                     alert_node = Node(
#                         "Alert",
#                         alert=alert_data.get("alert", ""),
#                         alertRef=alert_data.get("alertRef", ""),
#                         riskcode=alert_data.get("riskcode", ""),
#                         confidence=alert_data.get("confidence", ""),
#                         riskdesc=alert_data.get("riskdesc", ""),
#                         desc=alert_data.get("desc", ""),
#                         cweid=alert_data.get("cweid", ""),
#                         wascid=alert_data.get("wascid", ""),
#                         sourceid=alert_data.get("sourceid", "")
#                     )
#                     graph.merge(alert_node, "Alert", "alertRef")
#                     exists_in_site_relation = Relationship(site_node, "HAS_ALERT", alert_node)
#                     graph.merge(exists_in_site_relation)
#
#                     if "solution" in alert_data:
#                         solution_node = Node("Solution", solution=alert_data["solution"])
#                         graph.merge(solution_node, "Solution", "solution")
#                         has_solution_relation = Relationship(alert_node, "HAS_SOLUTION", solution_node)
#                         graph.merge(has_solution_relation)
#
#                     if "reference" in alert_data:
#                         reference_node = Node("Reference", reference=alert_data["reference"])
#                         graph.merge(reference_node, "Reference", "reference")
#                         has_reference_relation = Relationship(alert_node, "HAS_REFERENCE", reference_node)
#                         graph.merge(has_reference_relation)
#
#                     if "otherinfo" in alert_data:
#                         otherinfo_node = Node("OtherInfo", otherinfo=alert_data["otherinfo"])
#                         graph.merge(otherinfo_node, "OtherInfo", "otherinfo")
#                         has_otherinfo_relation = Relationship(alert_node, "HAS_OTHERINFO", otherinfo_node)
#                         graph.merge(has_otherinfo_relation)
#
#                     for instance_data in alert_data.get("instances", []):
#                         if all(k in instance_data for k in ["uri", "method", "param"]):
#                             instances_node = Node(
#                                 "Instance",
#                                 uri=instance_data["uri"],
#                                 method=instance_data["method"],
#                                 param=instance_data["param"]
#                             )
#                             graph.merge(instances_node, "Instance", "uri")
#                             has_instance_relation = Relationship(alert_node, "HAS_INSTANCE", instances_node)
#                             graph.merge(has_instance_relation)
#
#                             if "evidence" in instance_data:
#                                 evidence_node = Node("Evidence", evidence=instance_data["evidence"])
#                                 graph.merge(evidence_node, "Evidence", "evidence")
#                                 has_evidence_relation = Relationship(instances_node, "HAS_EVIDENCE", evidence_node)
#                                 graph.merge(has_evidence_relation)
#
#
#
# # MATCH (n)
# # DETACH DELETE n
#
#
# # CALL gds.graph.project(
# #     'myGraph',  // 图的名称
# #     '*',
# #     '*'
# # )
# #
# # 介数中心性
# # CALL gds.betweenness.stream('myGraph')
# # YIELD nodeId, score
# # RETURN gds.util.asNode(nodeId).name AS nodeName, score
# # ORDER BY score DESC
# #
# # 聚集系数
# # CALL gds.alpha.clusteringCoefficient.stream('myGraph')
# # YIELD nodeId, coefficient
# # RETURN gds.util.asNode(nodeId).name AS nodeName, coefficient
# # ORDER BY coefficient DESC
