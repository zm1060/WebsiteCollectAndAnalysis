import json
import sys
from fuzzywuzzy import fuzz
from math import radians, sin, cos, sqrt, atan2
import seaborn as sns

from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

from ip_location import awdb

from aiohttp.helpers import is_ipv4_address


def my_ip_query(ip):
    ip_info = dict()

    filename = r'../ip_location/IP_city_single_WGS84.awdb'
    # filename = os.path.dirname(__file__) + os.sep + 'IP_city_single_WGS84.awdb' #使用绝对路径
    reader = awdb.open_database(filename)
    try:
        (record, prefix_len) = reader.get_with_prefix_len(ip)

        continent = record.get("continent", b'').decode("utf-8")  # 大州
        owner = record.get("owner", b'').decode("utf-8")
        country = record.get("country", b'').decode("utf-8")  # 国家
        province = record.get("province", b'').decode("utf-8")  # 省份
        city = record.get("city", b'').decode("utf-8")  # 城市
        isp = record.get("isp", b'').decode("utf-8")  # 提供商，运营商
        asnumber = record.get("asnumber", b'').decode("utf-8")  # AS编号
        latwgs = record.get("latwgs", b'').decode("utf-8") if sys.version_info[0] == 3 else record.get("latwgs", '')
        lngwgs = record.get("lngwgs", b'').decode("utf-8") if sys.version_info[0] == 3 else record.get("lngwgs", '')
        radius = record.get("radius", b'').decode("utf-8") if sys.version_info[0] == 3 else record.get("radius", '')
        ip_info = {
            'continent': continent,
            'owner': owner,
            'country': country,
            'country_prov_city': '_'.join([country, province, city]),
            'isp': isp,
            'asn': asnumber,
            'latwgs': latwgs,
            'lngwgs': lngwgs,
            'radius': radius,
            'prefix_len': str(prefix_len)
        }

        return ip_info
    except Exception as e:
        return ip_info


def generate_ip_info():
    # Load namerserver_ip.json
    with open('namerserver_ip.json', 'r', encoding='utf-8') as f:
        domin_ips = json.load(f)
    # Initialize a dictionary to store aggregated IP information for each domain
    domain_ip_info_dict = {}

    # Iterate through each record in domin_ips
    for record in domin_ips:
        nameserver_domain = record['nameserver_domain']
        ips = record['ips']

        # Initialize a list to store IP information for the current domain
        domain_ip_list = []

        # Iterate through each IP for the domain
        for ip in ips:
            if is_ipv4_address(ip):
                ip_info = my_ip_query(ip)

                # Add IP information to the list for the current domain
                domain_ip_list.append({
                    'ip_address': ip,
                    'ip_info': ip_info
                })

        # Add the aggregated IP information for the current domain to the dictionary
        domain_ip_info_dict[nameserver_domain] = domain_ip_list

    # Save the aggregated IP information to result_ip_info.json
    with open('result_ip_info.json', 'w', encoding='utf-8') as result_file:
        json.dump(domain_ip_info_dict, result_file, indent=2, ensure_ascii=False)

    print("Aggregated IP information saved to result_ip_info.json.")


# Function to calculate Haversine distance between two lat-lng points
def haversine_distance(lat_lng1, lat_lng2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lng1 = map(radians, lat_lng1)
    lat2, lng2 = map(radians, lat_lng2)

    # Calculate differences
    dlat = lat2 - lat1
    dlng = lng2 - lng1

    # Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in kilometers
    distance = R * c

    return distance


# Function to check if a new 'lat_lng' is similar to existing ones based on distance
def is_similar_lat_lng(new_lat_lng, existing_lat_lngs, distance_threshold):
    if len(existing_lat_lngs) == 0:
        return False
    return all(haversine_distance(new_lat_lng, existing_lat_lng) < distance_threshold for existing_lat_lng in
               existing_lat_lngs)


# Function to check if a new 'country_prov_city' is similar to existing ones
def is_similar_to_existing(new_value, existing_values):
    if len(existing_values) == 0:
        return False
    # 定义相似度阈值（根据需要调整）
    similarity_threshold = 80
    # 使用fuzzywuzzy库的ratio函数计算相似度
    similarities = [fuzz.ratio(new_value, existing_value) for existing_value in existing_values]
    # 如果任何一个相似度超过阈值，返回True
    return any(similarity > similarity_threshold for similarity in similarities)


def calculate_diversity_score(ip_entries):
    # Track unique values for diversity calculation
    unique_asns = set()
    unique_isps = set()
    unique_lat_lng = set()
    unique_country_prov_city = set()

    if len(ip_entries) == 0:
        return {
            'overall_diversity_score': -1,
            'asn_diversity_score': -1,
            'isp_diversity_score': -1,
            'lat_lng_diversity_score': -1,
            'country_prov_city_score': -1,
            'ip_address_score': -1,
            'unique_country_prov_city': [],
            'unique_asns': [],
            'unique_isps': [],
            'unique_lat_lng': [],
            'unique_ips': [],
        }  # Avoid division by zero

    # Iterate through each IP entry
    for entry in ip_entries:
        ip_info = entry['ip_info']

        # Geographic Distribution Score based on 'country_prov_city'
        country_prov_city = ip_info['country_prov_city']

        # Check similarity to existing values
        if not is_similar_to_existing(country_prov_city, unique_country_prov_city):
            unique_country_prov_city.add(country_prov_city)

        # ASN Diversity Score (Proportion of unique ASNs)
        unique_asns.add(ip_info['asn'])

        # ISP Diversity Score (Proportion of unique ISPs)
        unique_isps.add(ip_info['isp'])
        distance_threshold = 500
        # Lat-Lng Diversity Score (Proportion of unique lat-lng combinations based on distance)
        lat_str = ip_info.get('latwgs', '')
        lng_str = ip_info.get('lngwgs', '')

        if lat_str and lng_str:
            lat_lng = (float(lat_str), float(lng_str))
        else:
            # 处理缺失经纬度的情况，例如将 lat_lng 设置为默认值或者抛出异常等
            lat_lng = (0.0, 0.0)  # 默认值示例
        if not is_similar_lat_lng(lat_lng, unique_lat_lng, distance_threshold):
            unique_lat_lng.add(lat_lng)

    # Calculate normalized diversity scores
    asn_diversity_score = len(unique_asns)
    isp_diversity_score = len(unique_isps)
    lat_lng_diversity_score = len(unique_lat_lng)
    print(unique_lat_lng)
    print(lat_lng_diversity_score)
    country_prov_city_score = len(unique_country_prov_city)
    print(unique_country_prov_city)
    print(country_prov_city_score)
    ip_address_score = len(ip_entries)
    # Calculate overall diversity score
    overall_diversity_score = (
                                      asn_diversity_score +
                                      isp_diversity_score +
                                      lat_lng_diversity_score +
                                      country_prov_city_score +
                                      ip_address_score
                              ) / 5.0

    caculated_result = {
        'overall_diversity_score': overall_diversity_score,
        'asn_diversity_score': asn_diversity_score,
        'isp_diversity_score': isp_diversity_score,
        'lat_lng_diversity_score': lat_lng_diversity_score,
        'country_prov_city_score': country_prov_city_score,
        'ip_address_score': ip_address_score,
        'unique_country_prov_city': list(unique_country_prov_city),
        'unique_asns': list(unique_asns),
        'unique_isps': list(unique_isps),
        'unique_lat_lng': list(unique_lat_lng),
        'unique_ips': list(ip_entries),
    }
    return caculated_result


def analyze_isp_distribution(ip_entries):
    isp_distribution = {}

    for entry in ip_entries:
        isp = entry['ip_info']['isp']
        isp_distribution[isp] = isp_distribution.get(isp, 0) + 1

    return isp_distribution


def analyze_asn_distribution(ip_entries):
    asn_distribution = {}

    for entry in ip_entries:
        asn = entry['ip_info']['asn']
        asn_distribution[asn] = asn_distribution.get(asn, 0) + 1

    return asn_distribution


def analyze_ip_info():
    with open('result_ip_info.json', 'r', encoding='utf-8') as f:
        ip_info = json.load(f)

    domain_results = []  # List to store results for each domain

    for domain, ip_entries in ip_info.items():
        print(f"\nDomain: {domain}")
        if len(ip_entries) == 0:
            print("No IP entries found for this domain")
            continue
        # Calculate diversity score for the given data
        caculated_results = calculate_diversity_score(ip_entries)

        diversity_score = caculated_results['overall_diversity_score']
        asn_diversity_score = caculated_results['asn_diversity_score']
        isp_diversity_score = caculated_results['isp_diversity_score']
        lat_lng_diversity_score = caculated_results['lat_lng_diversity_score']
        country_prov_city_score = caculated_results['country_prov_city_score']
        ip_address_score = caculated_results['ip_address_score']
        unique_asns = caculated_results['unique_asns']
        unique_isps = caculated_results['unique_isps']
        unique_lat_lng = caculated_results['unique_lat_lng']
        unique_country_prov_city = caculated_results['unique_country_prov_city']

        print(f"Diversity Score: {diversity_score}")

        # Analyze ISP Distribution
        isp_distribution = analyze_isp_distribution(ip_entries)
        print("ISP Distribution:")
        for isp, count in isp_distribution.items():
            print(f"{isp}: {count}")

        # Analyze ASN Distribution
        asn_distribution = analyze_asn_distribution(ip_entries)
        print("\nASN Distribution:")
        for asn, count in asn_distribution.items():
            print(f"{asn}: {count}")

        # Store results for the current domain
        domain_results.append({
            'domain': domain,
            'diversity_score': diversity_score,
            'isp_distribution': isp_distribution,
            'asn_distribution': asn_distribution,
            'unique_asns': unique_asns,
            'unique_isps': unique_isps,
            'unique_lat_lng': unique_lat_lng,
            'unique_country_prov_city': unique_country_prov_city,
            'ip_address_score': ip_address_score,
            'asn_diversity_score': asn_diversity_score,
            'isp_diversity_score': isp_diversity_score,
            'lat_lng_diversity_score': lat_lng_diversity_score,
            'country_prov_city_score': country_prov_city_score,
        })
    print(domain_results)
    # Save all results to a file (e.g., analysis_results.json)
    with open('nameserver_ip_analysis_results.json', 'w', encoding='utf-8') as results_file:
        json.dump(domain_results, results_file, ensure_ascii=False, indent=2)


def plot_figure():
    # Specify the font properties with SimHei
    font_properties = FontProperties(fname="../SimHei.ttf")

    with open('nameserver_ip_analysis_results.json', 'r', encoding='utf-8') as f:
        domain_results = json.load(f)

    # Aggregate overall statistics
    overall_diversity_scores = []
    overall_ip_address_scores = []  # To store ip_address_score values
    overall_unique_lat_lng_sizes = []  # To store sizes of unique_lat_lng sets
    overall_unique_country_prov_city_sizes = []  # To store sizes of unique_country_prov_city sets

    overall_isp_distribution = {}
    overall_asn_distribution = {}

    for result in domain_results:
        overall_diversity_scores.append(result['diversity_score'])

        # Aggregate ISP distribution
        for isp, count in result['isp_distribution'].items():
            overall_isp_distribution[isp] = overall_isp_distribution.get(isp, 0) + count

        # Aggregate ASN distribution
        for asn, count in result['asn_distribution'].items():
            overall_asn_distribution[asn] = overall_asn_distribution.get(asn, 0) + count

        # Aggregate ip_address_score values
        overall_ip_address_scores.append(result['ip_address_score'])

        # Aggregate sizes of unique_lat_lng and unique_country_prov_city sets
        overall_unique_lat_lng_sizes.append(len(result['unique_lat_lng']))
        overall_unique_country_prov_city_sizes.append(len(result['unique_country_prov_city']))
    print(overall_isp_distribution)
    data_en = {'Alibaba Cloud': 374, 'China Telecom': 321, 'China Mobile': 156, 'Tencent': 183, 'China Unicom': 261, 'CERNET': 8,
               'Zenlayer Inc': 14, 'GUANGDONG WEIYI NETWORK TECHNOLOGY CO., LTD.': 14, 'CSTNET': 9, 'China Internet Network Information Center': 4,
               'China National Network Exchange Center': 22, 'Huawei': 13, '': 10, 'ZDNS': 4,
               'Ningxia West Cloud Valley Technology Co., Ltd.': 2, 'QUANTIL NETWORKS INC': 2, 'State Information Center': 2, 'Baidu': 4,
               'China E-Government Network': 6, 'National Bureau of Statistics Data Management Center': 4, 'UCLOUD INFORMATION TECHNOLOGY (HK) LIMITED': 1,
               'Dr Peng': 5, 'Ministry of Science and Technology': 2, 'CIECC': 2, 'Amazon': 2, 'OCN': 1,
               'Guoyan Technology Group Co., Ltd.': 1, 'CASS': 2, 'Wasu Media Holding Co., Ltd.': 1, 'Beijing Fortune Public Information Platform': 2, 'Shenzhen Information Network Center': 2,
               'Limestone Networks, Inc.': 1}


    # Plot overall ISP distribution for the top 10 ISPs
    top_isps = dict(sorted(data_en.items(), key=lambda x: x[1], reverse=True)[:10])
    top_asns = dict(sorted(overall_asn_distribution.items(), key=lambda x: x[1], reverse=True)[:10])

    # Function to convert counts to percentages
    def counts_to_percentages(counts):
        total = sum(counts.values())
        percentages = {key: (value / total) * 100 for key, value in counts.items()}
        return percentages

    def counts_to_percentage(top_counts, overall_counts):
        total_top = sum(top_counts.values())
        total_overall = sum(overall_counts.values())

        percentages = {key: (value / total_overall) * 100 for key, value in top_counts.items()}
        return percentages

    # Set DPI to 500
    plt.rcParams['figure.dpi'] = 500

    # Use Seaborn's color palette with lower saturation
    sns.set_palette("muted")

    # Define the provided color palette
    custom_colors = ["#2878b5", "#9ac9db", "#f8ac8c", "#c82423", "#ff8884", "#8ECFC9", "#FFBE7A",
                     "#FA7F6F", "#82B0D2", "#BEB8DC", "#E7DAD2", "#F27970", "#BB9727", "#54B345",
                     "#32B897", "#05B9E2", "#8983BF", "#C76DA2", "#A1A9D0", "#F0988C", "#B883D4",
                     "#9E9E9E", "#CFEAF1", "#C4A5DE", "#F6CAE5", "#96CCCB"]

    # Use a more diverse color palette
    sns.set_palette(custom_colors)

    # Plot histogram of overall diversity scores with multiple colors
    plt.figure(figsize=(10, 6), dpi=500)
    hist, bins, _ = plt.hist(overall_diversity_scores, bins=20, edgecolor='black', density=False)
    # Iterate through bars and assign different colors
    for i, patch in enumerate(plt.gca().patches):
        plt.setp(patch, 'facecolor', custom_colors[(i + 1) % len(custom_colors)])

    plt.xlabel('Diversity Score', fontproperties=font_properties)
    plt.ylabel('Percentage', fontproperties=font_properties)
    plt.xticks(bins)  # Set the x-axis ticks to match the bin edges
    # Adding specific value labels
    total = 0
    for i, number in enumerate(hist):
        total += number
    print(total)
    for i, percent in enumerate(hist):
        plt.text(bins[i] + 0.5 * (bins[1] - bins[0]), percent, f'{(percent / total) * 100:.2f}%', ha='center',
                 va='bottom')

    plt.tight_layout()
    plt.show()

    # Plot histogram of ip_address_score values with percentages
    plt.figure(figsize=(10, 6), dpi=500)
    hist, bins, _ = plt.hist(overall_ip_address_scores, bins=20, edgecolor='black',
                             density=False)
    for i, patch in enumerate(plt.gca().patches):
        plt.setp(patch, 'facecolor', custom_colors[(i + 2) % len(custom_colors)])
    plt.xlabel('IP Address Score', fontproperties=font_properties)
    plt.ylabel('Percentage', fontproperties=font_properties)
    plt.xticks(bins)  # Set the x-axis ticks to match the bin edges
    total = 0
    for i, number in enumerate(hist):
        total += number
    print(total)
    # Adding specific value labels
    for i, percent in enumerate(hist):
        plt.text(bins[i] + 0.5 * (bins[1] - bins[0]), percent, f'{(percent / total) * 100:.2f}%', ha='center',
                 va='bottom')

    plt.tight_layout()
    plt.show()

    # For the histogram of sizes of unique_lat_lng sets
    plt.figure(figsize=(10, 6), dpi=500)
    unique_lat_lng_sizes_int = [int(size) for size in overall_unique_lat_lng_sizes]
    unique_lat_lng_counts = {size: unique_lat_lng_sizes_int.count(size) for size in set(unique_lat_lng_sizes_int)}
    percentages = counts_to_percentages(unique_lat_lng_counts)
    plt.bar(percentages.keys(), percentages.values(), edgecolor='black')
    plt.xlabel('The number of geographical locations of the name server', fontproperties=font_properties)
    plt.ylabel('Percentage', fontproperties=font_properties)

    # Set explicit x-axis ticks based on your data range
    plt.xticks(range(min(percentages.keys()), max(percentages.keys()) + 1))

    for i, patch in enumerate(plt.gca().patches):
        plt.setp(patch, 'facecolor', custom_colors[(i + 3) % len(custom_colors)])

    # Adding specific value labels
    for size, percent in percentages.items():
        plt.text(size, percent, f'{percent:.2f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    # For the histogram of sizes of unique_country_prov_city sets
    plt.figure(figsize=(10, 6), dpi=500)
    unique_country_prov_city_sizes_int = [int(size) for size in overall_unique_country_prov_city_sizes]
    unique_country_prov_city_counts = {size: unique_country_prov_city_sizes_int.count(size) for size in
                                       set(unique_country_prov_city_sizes_int)}
    percentages_country_prov_city = counts_to_percentages(unique_country_prov_city_counts)
    plt.bar(percentages_country_prov_city.keys(), percentages_country_prov_city.values(), edgecolor='black')
    plt.xlabel('Number of different cities where the name server is deployed', fontproperties=font_properties)
    plt.ylabel('Percentage', fontproperties=font_properties)

    # Set explicit x-axis ticks based on your data range
    plt.xticks(range(min(percentages_country_prov_city.keys()), max(percentages_country_prov_city.keys()) + 1))

    for i, patch in enumerate(plt.gca().patches):
        plt.setp(patch, 'facecolor', custom_colors[(i + 4) % len(custom_colors)])

    # Adding specific value labels
    for size, percent in percentages_country_prov_city.items():
        plt.text(size, percent, f'{percent:.2f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    # Plot top 10 ISPs in Overall Distribution with percentages
    plt.figure(figsize=(12, 6), dpi=500)
    percentages_top_isps = counts_to_percentage(top_isps, overall_isp_distribution)
    plt.bar(percentages_top_isps.keys(), percentages_top_isps.values())
    plt.xlabel('Name Server ISP', fontproperties=font_properties)
    plt.ylabel('Percentage', fontproperties=font_properties)
    plt.xticks(rotation=45, fontproperties=font_properties)
    for i, patch in enumerate(plt.gca().patches):
        plt.setp(patch, 'facecolor', custom_colors[(i + 3) % len(custom_colors)])
    # Add values on top of the bars
    for isp, percent in percentages_top_isps.items():
        plt.text(isp, percent, f'{percent:.2f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    # Plot top 10 ASNs in Overall Distribution with percentages
    plt.figure(figsize=(12, 6), dpi=500)
    percentages_top_asns = counts_to_percentage(top_asns, overall_asn_distribution)
    plt.bar(percentages_top_asns.keys(), percentages_top_asns.values())
    plt.xlabel('Name Server ASN', fontproperties=font_properties)
    plt.ylabel('Percentage', fontproperties=font_properties)
    plt.xticks(rotation=45, fontproperties=font_properties)
    for i, patch in enumerate(plt.gca().patches):
        plt.setp(patch, 'facecolor', custom_colors[(i + 2) % len(custom_colors)])
    # Add values on top of the bars
    for asn, percent in percentages_top_asns.items():
        plt.text(asn, percent, f'{percent:.2f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # generate_ip_info()
    # analyze_ip_info()
    plot_figure()
