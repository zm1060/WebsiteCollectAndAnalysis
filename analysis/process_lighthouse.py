import os
import json
from collections import defaultdict

# Specify the main directory containing all folders
main_directory = "./lighthouse"

# Store relevant information in a list
audit_data_list = []

# Store relevant JavaScript library information and count in a dictionary
js_libraries_data_dict = defaultdict(lambda: {"count": 0, "versions": defaultdict(int)})

province_scores = defaultdict(lambda: {
    "performance": [],
    "accessibility": [],
    "best_practices": [],
    "seo": [],
    "pwa": []
})

# Define the target audits
target_audits = [
    # Security
    "http-status-code",
    "uses-http2",
    "is-on-https",
    # "third-party-summary",
    # "csp-xss",
    # "js-libraries",
    "geolocation-on-start",
    "notification-on-start",

    # SEO
    "meta-description",  # SEO
    "is-crawlable",  # SEO
    "robots-txt",  # SEO
    "link-text",
    "crawlable-anchors",
    "hreflang",
    "plugins",
    "viewport",  # mobile user
    "document-title",
    "meta-description",

    # Accessibility
    "aria-allowed-attr",
    "aria-allowed-role",
    "aria-hidden-body",
    "aria-required-attr",
    "aria-valid-attr-value",
    "aria-valid-attr",
    "color-contrast",
    "duplicate-id-active",
    "image-alt",
    "input-button-name",
    "meta-viewport",  # very important for mobile user!
    "content-width",
    "tap-targets",
    "uses-passive-event-listeners",
    "link-name",
    "paste-preventing-inputs",
    "font-display",
    "bf-cache",

    # Performance
    "uses-text-compression",
    "interactive",
    "redirects",
    "total-blocking-time",
    "first-contentful-paint",
    "largest-contentful-paint",
    "first-meaningful-paint",
    "cumulative-layout-shift",
    "speed-index",
    "max-potential-fid",
    "unused-javascript",

]

# Traverse all folders in the main directory
for folder_name in os.listdir(main_directory):
    folder_path = os.path.join(main_directory, folder_name)

    # Check if it's a folder
    if os.path.isdir(folder_path):
        province_name = folder_name
        # Traverse all files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                # Build the full file path
                file_path = os.path.join(folder_path, filename)

                # Parse the JSON report
                with open(file_path, 'r', encoding='utf-8') as file:
                    report = json.load(file)
                category = report.get('categories', {})

                # Ensure required keys exist in the 'category' dictionary
                performance_score = category.get('performance', {}).get('score', 0)
                accessibility_score = category.get('accessibility', {}).get('score', 0)
                best_practice_score = category.get('best-practices', {}).get('score', 0)
                seo_score = category.get('seo', {}).get('score', 0)
                pwa_score = category.get('pwa', {}).get('score', 0)

                # Append scores to province_scores dictionary
                province_scores[province_name]["performance"].append(performance_score)
                province_scores[province_name]["accessibility"].append(accessibility_score)
                province_scores[province_name]["best_practices"].append(best_practice_score)
                province_scores[province_name]["seo"].append(seo_score)
                province_scores[province_name]["pwa"].append(pwa_score)

                # Extract information for target audits
                for audit_name in target_audits:
                    audit_data = report.get("audits", {}).get(audit_name, {})
                    score = audit_data.get("score")
                    requested_url = report.get("requestedUrl")
                    final_displayed_url = report.get("finalDisplayedUrl")

                    # Extract information from the "js-libraries" section
                    js_libraries_data_audit = audit_data
                    if audit_name == "js-libraries" and js_libraries_data_audit:
                        js_libraries_name = js_libraries_data_audit.get("details", {}).get("items", [])
                        for library_info in js_libraries_name:
                            name = library_info.get("name")
                            version = library_info.get("version")

                            # Update count and versions in the dictionary
                            js_libraries_data_dict[name]["count"] += 1
                            js_libraries_data_dict[name]["versions"][version] += 1

                    # Analyze redirection information
                    is_redirect = requested_url != final_displayed_url
                    redirects_to_https = requested_url.startswith("http://") and final_displayed_url.startswith(
                        "https://")

                    # Add information to the list
                    audit_data_list.append({
                        "audit_name": audit_name,
                        "score": score,
                        "requested_url": requested_url,
                        "final_displayed_url": final_displayed_url,
                        "is_redirect": is_redirect,
                        "redirects_to_https": redirects_to_https
                    })

# Save audit data as JSON
with open("audit_data.json", "w", encoding="utf-8") as audit_file:
    json.dump(audit_data_list, audit_file, ensure_ascii=False, indent=2)

# Convert sets to lists in js_libraries_data_dict
js_libraries_data_dict_serializable = {}
for name, data in js_libraries_data_dict.items():
    js_libraries_data_dict_serializable[name] = {
        "count": data["count"],
        "versions": dict(data["versions"])  # Convert defaultdict to regular dict
    }

# Save js_libraries_data_dict as JSON
with open("js_libraries_data.json", "w", encoding="utf-8") as js_libraries_dict_file:
    json.dump(js_libraries_data_dict_serializable, js_libraries_dict_file, indent=2)

print(f"JavaScript libraries data dictionary saved to js_libraries_data.json")

average_scores_per_province = {}
for province, scores in province_scores.items():
    # Filter out None values before calculating sum and length
    performance_scores = [score for score in scores["performance"] if score is not None]
    accessibility_scores = [score for score in scores["accessibility"] if score is not None]
    best_practices_scores = [score for score in scores["best_practices"] if score is not None]
    seo_scores = [score for score in scores["seo"] if score is not None]
    pwa_scores = [score for score in scores["pwa"] if score is not None]

    # Calculate averages
    average_scores_per_province[province] = {
        "performance": sum(performance_scores) / len(performance_scores) if performance_scores else None,
        "accessibility": sum(accessibility_scores) / len(accessibility_scores) if accessibility_scores else None,
        "best_practices": sum(best_practices_scores) / len(best_practices_scores) if best_practices_scores else None,
        "seo": sum(seo_scores) / len(seo_scores) if seo_scores else None,
        "pwa": sum(pwa_scores) / len(pwa_scores) if pwa_scores else None
    }

# {'上海市': {'performance': 0.48218750000000005, 'accessibility': 0.5957812499999998, 'best_practices': 0.6613846153846155, 'seo': 0.770461538461538, 'pwa': 0.35046153846153844}, '中医药管理局': {'performance': None, 'accessibility': None, 'best_practices': None, 'seo': None, 'pwa': None}, '中科院': {'performance': 0.6257142857142856, 'accessibility': 0.6773076923076926, 'best_practices': 0.6939285714285716, 'seo': 0.8150000000000002, 'pwa': 0.3435714285714287}, '乡村振兴局': {'performance': 0.38, 'accessibility': 0.89, 'best_practices': 0.59, 'seo': 0.9, 'pwa': 0.38}, '云南省': {'performance': 0.5417898832684829, 'accessibility': 0.5816475095785442, 'best_practices': 0.5678966789667899, 'seo': 0.6443749999999999, 'pwa': 0.16702205882352966}, '交通运输部': {'performance': 0.5241176470588236, 'accessibility': 0.5956250000000002, 'best_practices': 0.6982352941176471, 'seo': 0.7147058823529413, 'pwa': 0.2752941176470588}, '人力资源社会保障部': {'performance': 0.6255555555555555, 'accessibility': 0.6588888888888887, 'best_practices': 0.5977777777777777, 'seo': 0.6455555555555557, 'pwa': 0.12666666666666668}, '人民银行': {'performance': 0.385, 'accessibility': 0.825, 'best_practices': 0.64, 'seo': 0.605, 'pwa': 0.125}, '住房城乡建设部': {'performance': 0.54, 'accessibility': 0.58, 'best_practices': 0.64, 'seo': 0.82, 'pwa': 0.38}, '体育总局': {'performance': 0.65, 'accessibility': 0.62, 'best_practices': 0.64, 'seo': 0.5, 'pwa': 0.0}, '信访局': {'performance': 0.71, 'accessibility': 0.56, 'best_practices': 0.68, 'seo': 0.5, 'pwa': 0.0}, '公安部': {'performance': 0.6775, 'accessibility': 0.6749999999999999, 'best_practices': 0.6475000000000001, 'seo': 0.655, 'pwa': 0.125}, '内蒙古自治区': {'performance': 0.533619402985075, 'accessibility': 0.6191170825335893, 'best_practices': 0.5112500000000004, 'seo': 0.6719925512104281, 'pwa': 0.22698324022346283}, '农业农村部': {'performance': 0.69, 'accessibility': 0.54, 'best_practices': 0.55, 'seo': 0.74, 'pwa': 0.38}, '北京市': {'performance': 0.574933333333333, 'accessibility': 0.5683783783783783, 'best_practices': 0.621866666666667, 'seo': 0.7055999999999998, 'pwa': 0.3090666666666666}, '医保局': {'performance': 0.54, 'accessibility': 0.46, 'best_practices': 0.68, 'seo': 0.74, 'pwa': 0.38}, '卫生健康委': {'performance': 0.73, 'accessibility': 0.49, 'best_practices': 0.64, 'seo': 0.5, 'pwa': 0.0}, '参事室': {'performance': 0.88, 'accessibility': 0.6, 'best_practices': 0.68, 'seo': 0.58, 'pwa': 0.0}, '发展改革委': {'performance': 0.4775, 'accessibility': 0.6775, 'best_practices': 0.5475000000000001, 'seo': 0.6375, 'pwa': 0.19}, '发展研究中心': {'performance': 0.62, 'accessibility': 0.6, 'best_practices': 0.59, 'seo': 0.46, 'pwa': 0.0}, '司法部': {'performance': 0.635, 'accessibility': 0.55, 'best_practices': 0.59, 'seo': 0.6599999999999999, 'pwa': 0.125}, '吉林省': {'performance': 0.5785084745762715, 'accessibility': 0.5477777777777773, 'best_practices': 0.5470134228187926, 'seo': 0.5849328859060405, 'pwa': 0.10147651006711401}, '商务部': {'performance': 0.56, 'accessibility': 0.8, 'best_practices': 0.73, 'seo': 0.83, 'pwa': 0.38}, '四川省': {'performance': 0.5720378457059684, 'accessibility': 0.6025997045790252, 'best_practices': 0.5932369942196528, 'seo': 0.6848843930635841, 'pwa': 0.2142774566473979}, '国务院部门所属网站': {'performance': 0.5501196172248807, 'accessibility': 0.5755025125628136, 'best_practices': 0.6321957040572793, 'seo': 0.6815238095238101, 'pwa': 0.2235714285714282}, '国家民委': {'performance': 0.52, 'accessibility': 0.54, 'best_practices': 0.59, 'seo': 0.76, 'pwa': 0.38}, '国管局': {'performance': 0.58, 'accessibility': 0.56, 'best_practices': 0.6533333333333333, 'seo': 0.6699999999999999, 'pwa': 0.21}, '国资委': {'performance': 0.59, 'accessibility': 0.44, 'best_practices': 0.59, 'seo': 0.83, 'pwa': 0.38}, '国防科工局': {'performance': 0.2733333333333334, 'accessibility': 0.6033333333333334, 'best_practices': 0.6066666666666668, 'seo': 0.7666666666666666, 'pwa': 0.38000000000000006}, '国际发展合作署': {'performance': 0.7, 'accessibility': 0.42, 'best_practices': 0.73, 'seo': 0.83, 'pwa': 0.38}, '地震局': {'performance': 0.5316666666666666, 'accessibility': 0.5651724137931035, 'best_practices': 0.5946666666666667, 'seo': 0.6763333333333332, 'pwa': 0.20666666666666664}, '外交部': {'performance': 0.6166666666666667, 'accessibility': 0.56, 'best_practices': 0.38999999999999996, 'seo': 0.5800000000000001, 'pwa': 0.25333333333333335}, '外汇局': {'performance': 0.68, 'accessibility': 0.4, 'best_practices': 0.68, 'seo': 0.38, 'pwa': 0.0}, '天津市': {'performance': 0.4203488372093025, 'accessibility': 0.6259302325581395, 'best_practices': 0.5622093023255819, 'seo': 0.6765116279069766, 'pwa': 0.26058139534883723}, '宁夏回族自治区': {'performance': 0.5407608695652173, 'accessibility': 0.648241758241758, 'best_practices': 0.5656521739130438, 'seo': 0.6897826086956517, 'pwa': 0.14652173913043487}, '安全部': {'performance': 0.98, 'accessibility': 0.57, 'best_practices': 0.73, 'seo': 0.71, 'pwa': 0.38}, '安徽省': {'performance': 0.39369593709043266, 'accessibility': 0.6670079787234056, 'best_practices': 0.6500131061598914, 'seo': 0.764136125654451, 'pwa': 0.28825916230366283}, '审计署': {'performance': 0.15, 'accessibility': 0.55, 'best_practices': 0.64, 'seo': 0.73, 'pwa': 0.38}, '山东省': {'performance': 0.5739447236180902, 'accessibility': 0.55174358974359, 'best_practices': 0.5147198007471973, 'seo': 0.6025, 'pwa': 0.12203980099502465}, '山西省': {'performance': 0.6116585365853657, 'accessibility': 0.5658750000000006, 'best_practices': 0.5762469733656179, 'seo': 0.6013317191283308, 'pwa': 0.08138014527845033}, '工业和信息化部': {'performance': 0.3714814814814815, 'accessibility': 0.4448387096774194, 'best_practices': 0.7967741935483871, 'seo': 0.7383870967741933, 'pwa': 0.37580645161290344}, '工程院': {'performance': 0.7, 'accessibility': 0.46, 'best_practices': 0.55, 'seo': 0.5, 'pwa': 0.0}, '市场监管总局': {'performance': 0.5366666666666667, 'accessibility': 0.4966666666666666, 'best_practices': 0.62, 'seo': 0.5833333333333334, 'pwa': 0.12666666666666668}, '广东省': {'performance': 0.5659793814432995, 'accessibility': 0.5720588235294113, 'best_practices': 0.6123975409836059, 'seo': 0.7409016393442622, 'pwa': 0.2766871165644159}, '广电总局': {'performance': 0.31, 'accessibility': 0.4, 'best_practices': 0.77, 'seo': 0.68, 'pwa': 0.38}, '广西壮族自治区': {'performance': 0.5899793388429746, 'accessibility': 0.5698136645962751, 'best_practices': 0.5675502008032145, 'seo': 0.743755020080321, 'pwa': 0.20839679358717406}, '应急管理部': {'performance': 0.645, 'accessibility': 0.615, 'best_practices': 0.55, 'seo': 0.5, 'pwa': 0.0}, '教育部': {'performance': 0.53, 'accessibility': 0.6266666666666666, 'best_practices': 0.4675, 'seo': 0.63, 'pwa': 0.1575}, '文化和旅游部': {'performance': 0.255, 'accessibility': 0.64, 'best_practices': 0.565, 'seo': 0.915, 'pwa': 0.38}, '文物局': {'performance': 0.64, 'accessibility': 0.37, 'best_practices': 0.59, 'seo': 0.5, 'pwa': 0.0}, '新疆生产建设兵团': {'performance': 0.4378048780487804, 'accessibility': 0.6070000000000001, 'best_practices': 0.5902439024390245, 'seo': 0.6963414634146342, 'pwa': 0.32756097560975633}, '新疆维吾尔自治区': {'performance': 0.5749358974358975, 'accessibility': 0.5640127388535033, 'best_practices': 0.5701898734177219, 'seo': 0.7140506329113916, 'pwa': 0.26477987421383675}, '林草局': {'performance': 0.29, 'accessibility': 0.46, 'best_practices': 0.59, 'seo': 0.74, 'pwa': 0.38}, '民政部': {'performance': 0.63, 'accessibility': 0.49, 'best_practices': 0.68, 'seo': 0.83, 'pwa': 0.38}, '民航局': {'performance': 0.70375, 'accessibility': 0.43000000000000005, 'best_practices': 0.6287499999999999, 'seo': 0.53, 'pwa': 0.0475}, '气象局': {'performance': 0.41531250000000003, 'accessibility': 0.5587499999999999, 'best_practices': 0.5753125, 'seo': 0.6421875000000001, 'pwa': 0.20937499999999998}, '水利部': {'performance': 0.5733333333333334, 'accessibility': 0.5733333333333334, 'best_practices': 0.581111111111111, 'seo': 0.6455555555555555, 'pwa': 0.16777777777777775}, '江苏省': {'performance': 0.5177004538577911, 'accessibility': 0.5713888888888895, 'best_practices': 0.5308928571428583, 'seo': 0.6712500000000001, 'pwa': 0.21967261904761795}, '江西省': {'performance': 0.4892621359223304, 'accessibility': 0.545158562367865, 'best_practices': 0.5884261036468328, 'seo': 0.6686948176583511, 'pwa': 0.25377394636015205}, '河北省': {'performance': 0.600373280943026, 'accessibility': 0.549329140461216, 'best_practices': 0.5821568627450987, 'seo': 0.6342270058708417, 'pwa': 0.12845401174168325}, '河南省': {'performance': 0.577289603960397, 'accessibility': 0.576418663303908, 'best_practices': 0.591552567237164, 'seo': 0.6846943765281185, 'pwa': 0.18786063569682063}, '浙江省': {'performance': 0.5984615384615385, 'accessibility': 0.5610457516339867, 'best_practices': 0.5591666666666669, 'seo': 0.707884615384615, 'pwa': 0.3117307692307698}, '海关总署': {'performance': 0.74, 'accessibility': 0.71, 'best_practices': 0.41, 'seo': 0.58, 'pwa': 0.0}, '海南省': {'performance': 0.4159130434782609, 'accessibility': 0.5362745098039216, 'best_practices': 0.5696551724137929, 'seo': 0.662068965517241, 'pwa': 0.19853448275862068}, '港澳办': {'performance': 0.58, 'accessibility': 0.64, 'best_practices': 0.64, 'seo': 0.75, 'pwa': 0.38}, '湖北省': {'performance': 0.5139766081871345, 'accessibility': 0.6040310077519381, 'best_practices': 0.5316988416988425, 'seo': 0.6919961612284076, 'pwa': 0.21917624521072726}, '湖南省': {'performance': 0.5264572425828971, 'accessibility': 0.6047627416520194, 'best_practices': 0.597339130434782, 'seo': 0.7244173913043495, 'pwa': 0.2962260869565201}, '烟草局': {'performance': 0.5664000000000001, 'accessibility': 0.5449999999999999, 'best_practices': 0.6428, 'seo': 0.682, 'pwa': 0.22279999999999997}, '甘肃省': {'performance': 0.5196913580246916, 'accessibility': 0.551881188118812, 'best_practices': 0.5299384615384626, 'seo': 0.6481230769230776, 'pwa': 0.18726153846153895}, '生态环境部': {'performance': 0.5861904761904762, 'accessibility': 0.5153846153846153, 'best_practices': 0.6128571428571428, 'seo': 0.54, 'pwa': 0.03619047619047619}, '省级门户': {'performance': 0.41645161290322585, 'accessibility': 0.5796774193548387, 'best_practices': 0.5851612903225807, 'seo': 0.7461290322580644, 'pwa': 0.32258064516129037}, '知识产权局': {'performance': 0.6000000000000001, 'accessibility': 0.525, 'best_practices': 0.7050000000000001, 'seo': 0.615, 'pwa': 0.19}, '矿山安监局': {'performance': 0.6217391304347826, 'accessibility': 0.5821739130434781, 'best_practices': 0.6578260869565218, 'seo': 0.6404347826086958, 'pwa': 0.12652173913043477}, '社科院': {'performance': 0.355, 'accessibility': 0.49, 'best_practices': 0.5700000000000001, 'seo': 0.5, 'pwa': 0.0}, '福建省': {'performance': 0.4383484162895928, 'accessibility': 0.5435550458715597, 'best_practices': 0.6202702702702696, 'seo': 0.7079504504504498, 'pwa': 0.277117117117116}, '科技部': {'performance': 0.44499999999999995, 'accessibility': 0.625, 'best_practices': 0.5, 'seo': 0.6875, 'pwa': 0.2525}, '移民局': {'performance': 0.7250000000000001, 'accessibility': 0.67, 'best_practices': 0.7250000000000001, 'seo': 0.8300000000000001, 'pwa': 0.38}, '税务总局': {'performance': 0.5948387096774193, 'accessibility': 0.5719354838709677, 'best_practices': 0.5712903225806452, 'seo': 0.7393548387096773, 'pwa': 0.37580645161290344}, '粮食和物资储备局': {'performance': 0.21, 'accessibility': 0.86, 'best_practices': 0.68, 'seo': 0.67, 'pwa': 0.38}, '统计局': {'performance': 0.6421428571428571, 'accessibility': 0.6025, 'best_practices': 0.595, 'seo': 0.7085714285714285, 'pwa': 0.2614285714285714}, '能源局': {'performance': 0.6031578947368421, 'accessibility': 0.5463157894736841, 'best_practices': 0.6252631578947367, 'seo': 0.5821052631578948, 'pwa': 0.060000000000000005}, '自然基金会': {'performance': 0.36, 'accessibility': 0.63, 'best_practices': 0.5, 'seo': 0.67, 'pwa': 0.0}, '自然资源部': {'performance': 0.472, 'accessibility': 0.5444444444444445, 'best_practices': 0.5409999999999999, 'seo': 0.637, 'pwa': 0.177}, '药监局': {'performance': None, 'accessibility': None, 'best_practices': None, 'seo': None, 'pwa': None}, '西藏自治区': {'performance': 0.5407260726072605, 'accessibility': 0.629429530201342, 'best_practices': 0.5932786885245918, 'seo': 0.7479411764705882, 'pwa': 0.2957189542483657}, '证监会': {'performance': 0.09, 'accessibility': 0.7, 'best_practices': 0.59, 'seo': 0.75, 'pwa': 0.38}, '财政部': {'performance': 0.5666666666666667, 'accessibility': 0.5433333333333333, 'best_practices': 0.62, 'seo': 0.5666666666666668, 'pwa': 0.0}, '贵州省': {'performance': 0.5368844221105529, 'accessibility': 0.5684237726098194, 'best_practices': 0.5303015075376893, 'seo': 0.6673115577889448, 'pwa': 0.15741206030150787}, '辽宁省': {'performance': 0.5079962894248613, 'accessibility': 0.5655179282868523, 'best_practices': 0.5761070110701108, 'seo': 0.6265867158671589, 'pwa': 0.17577490774907717}, '退役军人事务部': {'performance': 0.46, 'accessibility': 0.72, 'best_practices': 0.59, 'seo': 0.5, 'pwa': 0.0}, '邮政局': {'performance': 0.3141379310344828, 'accessibility': 0.6978571428571426, 'best_practices': 0.6270370370370372, 'seo': 0.7670370370370369, 'pwa': 0.2548148148148148}, '部委门户': {'performance': 0.4986206896551724, 'accessibility': 0.5796363636363636, 'best_practices': 0.6024137931034483, 'seo': 0.6915517241379309, 'pwa': 0.2486206896551726}, '重庆市': {'performance': 0.4735632183908046, 'accessibility': 0.6751190476190477, 'best_practices': 0.6513793103448274, 'seo': 0.7328735632183903, 'pwa': 0.3682758620689652}, '铁路局': {'performance': 0.57, 'accessibility': 0.59, 'best_practices': 0.55, 'seo': 0.73, 'pwa': 0.25}, '银保监会': {'performance': 0.37, 'accessibility': 0.57, 'best_practices': 0.36, 'seo': 0.82, 'pwa': 0.25}, '陕西省': {'performance': 0.5077256317689531, 'accessibility': 0.5845353159851299, 'best_practices': 0.6175276752767515, 'seo': 0.7332110091743125, 'pwa': 0.259926605504586}, '青海省': {'performance': 0.4242635658914727, 'accessibility': 0.608139534883721, 'best_practices': 0.6111363636363638, 'seo': 0.6974999999999997, 'pwa': 0.1832575757575757}, '黑龙江省': {'performance': 0.5356862745098038, 'accessibility': 0.579267015706806, 'best_practices': 0.5537745098039222, 'seo': 0.6690196078431372, 'pwa': 0.23877450980392195}}
